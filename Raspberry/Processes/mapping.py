import os
from Helpers.graph_converter import convert_json
from Services import arduino_manager, direction_manager
from CrossCuttingConcerns import mqtt_adapter, raspi_log
from Helpers import path_helper
from entities.Graph import Graph
from Helpers.graph_converter import read_database

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(dir_path), 'Database', 'db_graph.txt')
try:
    db_graph = open(file_path,"a")
except FileNotFoundError:
    raspi_log.log_process("No graph history found")
    db_graph = open(file_path, "w")
direction = ""
isPathFollowing = False
pub_topic = "mapping"
sub_qr_topic = "qr"


class Mapping:
    def __init__(self, finish_callback):
        self.finish_callback = finish_callback
        raspi_log.log_process(str(f"Mapping started! parent id: {os.getppid()},  self id: {os.getpid()}"))
        self.graph_map = Graph()
        self.direction_controller = direction_manager.Direction()
        self.PathHelper = path_helper.PathHelper()


    def callback_for_obstacle(self, msg):
        last_node_id = self.graph_map.get_last_node_id()
        last_node = self.graph_map.get_node(last_node_id)
        result_add_obstacle = self.graph_map.add_obstacle(last_node.get_pos_x(), 80)
        if result_add_obstacle == 0:
            raspi_log.log_process(str("Obstacle already in list"))
        else:
            self.send_graph_status(self.graph_map)

    def callback_for_direction(self,msg):

        direction_parts = msg.split(";")
        self.direction_controller.set_direction(direction_parts[0])
        check_database_update_graph = read_database(self.graph_map)
        if not check_database_update_graph:
            if direction_parts[1] == "S1":
                self.graph_map.add_new_intersection("Start", 8000, 12500,{},"S2")
            elif direction_parts[1] == "S2":
                self.graph_map.add_new_intersection("Start", 8000, 0,{},"S1")

            message = str(f"There was not a saved map to be found. Initial steps were executed to generate the map.")
            raspi_log.log_process(message)
        if check_database_update_graph:
            raspi_log.log_process(str("Past data write on graph object"))

    def callback_for_qr(self, msg):
        message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
        parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
        result_add_qr = self.graph_map.add_qr(parts[0], parts[1], parts[2])
        if result_add_qr == 0:
            mqtt_adapter.publish("QR is already in list", sub_qr_topic)
        else:
            self.send_graph_status(self.graph_map)

    def callback_for_corner(self, msg):
        global new_direction, direction
        corner_type = msg
        last_qr = self.graph_map.get_last_qr()
        corner = self.get_corner_data(corner_type, last_qr)
        posx = corner[0]
        posy = corner[1]
        new_direction = corner[2]
        unvisited_directions = corner[3]
        print("posx : " + corner[0] + " posy: " + corner[1] + " new direction: " + new_direction + " "  + unvisited_directions)

        check_node_exist = self.graph_map.check_node_already_exist(posx, posy)

        if check_node_exist:
            raspi_log.log_process("A faced with already visited intersection")
            raspi_log.log_process("Mapping finished!")
            self.finish_callback()
            # already_visited_node = self.graph_map.already_visited_node(posx, posy)
            # arduino_manager.stop_autonomous_motion_of_vehicle()
            # nodes_with_unvisited = self.graph_map.nodes_having_unvisited_direction()
            # if len(nodes_with_unvisited) == 0:
            #     # finished mapping
            #     self.finish_callback()
            #     return
            # node_with_unvisited = nodes_with_unvisited[0]
            # path = self.PathHelper.find_path(already_visited_node, node_with_unvisited)
            # self.PathHelper.start_follow_path(path)
        else:
            self.graph_map.add_new_intersection(corner_type, posx, posy, unvisited_directions,str(self.graph_map.num_of_nodes))
            if corner_type == "T" or corner_type == "LEFT_T" or corner_type == "RIGHT_T":
                arduino_manager.send_arduino_to_decision(corner_type,new_direction)

        self.send_graph_status(self.graph_map)
        self.direction_controller.set_direction(new_direction)
        direction = self.direction_controller.get_direction()

    def get_corner_data(self,corner_type, qr):
        global direction
        direction = self.direction_controller.get_direction()
        corner_actions = {
            "LEFT_L": {
                "N": (0, 1000, "W"),
                "E": (-1000, 0, "N"),
                "S": (0, -1000, "E"),
                "W": (1000, 0, "S"),
            },
            "RIGHT_L": {
                "N": (0, 1000, "E"),
                "E": (-1000, 0, "S"),
                "S": (0, -1000, "W"),
                "W": (-1000, 0, "N"),
            },
            "T": {
                "N": (0, 1000, "W", ["E"]),
                "E": (-1000, 0, "E", ["S"]),
                "S": (0, -1000, "W", ["S"]),
                "W": (1000, 0, "W", ["S"]),
            },
            "RIGHT_T": {
                "E": (-1000, 0, "E", ["S"]),
                "W": (1000, 0, "W", ["N"]),
            },
            "LEFT_T": {
                "E": (-1000, 0, "E", ["N"]),
                "W": (1000, 0, "W", ["S"]),
            },
        }

        unvisited_directions = []
        posx = qr.get_pos_x()
        posy = qr.get_pos_y()
        direction_new = ""
        if corner_type in corner_actions:
            if direction in corner_actions[corner_type]:
                action = corner_actions[corner_type][direction]
                posx += action[0]
                posy += action[1]
                direction_new = action[2]
                if len(action) > 3:
                    unvisited_directions = action[3]

        return posx, posy, direction_new, unvisited_directions


    @staticmethod
    def get_direction():
        global direction
        return direction
    @staticmethod
    def send_graph_status(graph):
        json_graph = convert_json(graph)
        db_graph.write(json_graph + "\n")
        mqtt_adapter.publish(json_graph, pub_topic)
