import os
from graph_converter import convert_json
import imu_manager
from CrossCuttingConcerns import mqtt_adapter, raspi_log
from Helpers import path_helper
from entities.Graph import Graph
from graph_converter import read_database
import arduino_manager


db_graph_a = open("./Database/db_graph.txt", "a")
db_graph_r = open("./Database/db_graph.txt", "r")

new_direction = ""
isPathFollowing = False
pub_topic = "mapping"
sub_qr_topic = "qr"


class Mapping:
    def __init__(self, finish_callback):
        self.finish_callback = finish_callback
        raspi_log.log_process(str(f"Mapping started! parent id: {os.getppid()},  self id: {os.getpid()}"))
        self.graph_map = Graph()
        self.PathHelper = path_helper.PathHelper()
        check_database_update_graph = read_database(db_graph_r, self.graph_map)
        if not check_database_update_graph:
            self.graph_map.add_new_intersection("Start", 0, 0, {}, "S")
        if check_database_update_graph:
            raspi_log.log_process(str("Past data write on graph object"))

    def callback_for_obstacle(self, msg):
        message = msg.payload.decode('utf-8')
        last_node = self.graph_map.get_last_node()
        result_add_obstacle = self.graph_map.add_obstacle(last_node.get_pos_x(), 80)
        if result_add_obstacle == 0:
            raspi_log.log_process(str("Obstacle already in list"))
        else:
            self.send_graph_status(pub_topic)

    def callback_for_qr(self, msg):
        message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
        parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
        result_add_qr = self.graph_map.add_qr(parts[0], parts[1], parts[2])
        if result_add_qr == 0:
            mqtt_adapter.publish("QR is already in list", sub_qr_topic)
        else:
            self.send_graph_status(pub_topic)

    def callback_for_corner(self, msg):
        global new_direction, isPathFollowing
        message = msg.payload.decode('utf-8')
        corner_type = message
        last_qr = self.graph_map.get_last_qr()
        corner = self.get_corner_data(corner_type, last_qr)
        posx = corner[0]
        posy = corner[1]
        new_direction = corner[2]
        unvisited_directions = corner[3]

        if self.PathHelper.get_is_path_following():
            current_node = self.graph_map.already_visited_node(posx, posy)
            # find position of current node from qrs
            if posx == self.PathHelper.get_target_node().get_pos_x() and posy == self.PathHelper.get_target_node().get_pos_y():
                # path following finished
                self.PathHelper.set_is_path_following_flag(False)
                # after following path, the vehichle is on nodeWithUnvisited

                unvisited_direction = self.graph_map.visit_unvisited_direction(current_node) #Visit unvisited means turns unvisited direction to visited
                arduino_manager.send_arduino_to_decision(corner_type,unvisited_direction) # Turn to unvisited direction
                #turnToUnvisitedDirectionOfTheNodeWithUnvisited()
                arduino_manager.stop_autonomous_motion_of_vehicle()
            elif corner_type == "T" or corner_type == "LEFT_T" or corner_type == "RIGHT_T":
                direction = self.PathHelper.required_direction(current_node,self.PathHelper.get_next_node())
                arduino_manager.send_arduino_to_decision(corner_type,direction)
            return

        check_node_exist = self.graph_map.check_node_already_exist(posx, posy)

        if check_node_exist:
            already_visited_node = self.graph_map.already_visited_node(posx, posy)
            arduino_manager.stop_autonomous_motion_of_vehicle()
            nodes_with_unvisited = self.graph_map.nodes_having_unvisited_direction()
            if nodes_with_unvisited.count == 0:
                # finished mapping
                self.finish_callback()
                return
            node_with_unvisited = self.graph_map.get_node(nodes_with_unvisited[0])
            path = self.PathHelper.find_path(already_visited_node, node_with_unvisited)
            self.PathHelper.start_follow_path(path)
        else:
            self.graph_map.add_new_intersection(corner_type, posx, posy, unvisited_directions)

        self.send_graph_status(pub_topic)

    @staticmethod
    def get_corner_data(corner_type, qr):
        direction = imu_manager.get_direction()
        corner_actions = {
            "LEFT_L": {
                "N": (0, 10, "W"),
                "E": (-10, 0, "N"),
                "S": (0, -10, "E"),
                "W": (10, 0, "S"),
            },
            "RIGHT_L": {
                "N": (0, 10, "E"),
                "E": (-10, 0, "S"),
                "S": (0, -10, "W"),
                "W": (-10, 0, "N"),
            },
            "T": {
                "N": (0, 10, "W", ["E"]),
                "E": (-10, 0, "E", ["S"]),
                "S": (0, -10, "W", ["S"]),
                "W": (10, 0, "W", ["S"]),
            },
            "RIGHT_T": {
                "E": (-10, 0, "E", ["S"]),
                "W": (10, 0, "W", ["N"]),
            },
            "LEFT_T": {
                "E": (-10, 0, "E", ["N"]),
                "W": (10, 0, "W", ["S"]),
            },
        }

        unvisited_directions = []
        posx = qr.get_pos_x()
        posy = qr.get_pos_y()
        new_direction = ""
        if corner_type in corner_actions:
            if direction in corner_actions[corner_type]:
                action = corner_actions[corner_type][direction]
                posx += action[0]
                posy += action[1]
                new_direction = action[2]
                if len(action) > 3:
                    unvisited_directions = action[3]

        return posx, posy, new_direction, unvisited_directions

    @staticmethod
    def get_new_direction():
        global new_direction
        return new_direction

    def send_graph_status(self,graph):
        json_graph = convert_json(graph)
        db_graph_a.write(json_graph + "\n")
        mqtt_adapter.publish(json_graph, pub_topic)
