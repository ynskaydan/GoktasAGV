import os
import threading

import imu_manager
from CrossCuttingConcerns import mqtt_adapter
from entities.Graph import Graph
from graph_converter import read_database

db_graph_a = open("./Database/db_graph.txt", "a")
db_graph_r = open("./Database/db_graph.txt", "r")

sub_corner_topic = "intersection"
sub_obstacle_topic = "obstacle"
sub_qr_topic = "qr"
pub_topic = "mapping"
new_direction = ""

lifecycle_pub_topic = "mode"


def main():
    print("Mapping started! parent id:", os.getppid(), " self id:", os.getpid())
    graph_map = Graph()
    mqtt_adapter.connect("graph_map")
    result = read_database(db_graph_r, graph_map)
    if not result:
        graph_map.add_new_intersection("Start", 0, 0, {}, "S")
    if result:
        print("Past data write on graph object")

    def callback_for_obstacle(client, userdata, msg):
        last_node = graph_map.get_last_node()
        result_add_obstacle = graph_map.add_obstacle(last_node.get_pos_x(), 80)
        if result_add_obstacle == 0:
            print("Obstacle already in list")
        else:
            graph_map.send_graph_status(pub_topic)

    def callback_for_qr(client, userdata, msg):
        message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
        parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
        result_add_qr = graph_map.add_qr(parts[0], parts[1], parts[2])
        if result_add_qr == 0:
            mqtt_adapter.publish("QR is already in list", sub_qr_topic)
        else:
            graph_map.send_graph_status(pub_topic)

    def callback_for_corner(client, userdata, msg):
        global new_direction
        message = msg.payload.decode('utf-8')
        corner_type = message
        last_qr = graph_map.get_last_qr()
        corner = get_corner_data(corner_type, last_qr)
        posx = corner[0]
        posy = corner[1]
        new_direction = corner[2]
        unvisited_directions = corner[3]
        result_add_node = graph_map.add_new_intersection(corner_type, posx, posy, unvisited_directions)
        if not result_add_node:
            same_node_id = graph_map.catch_same_node(posx, posy)
            new_direction = graph_map.visit_unvisited_direction(same_node_id)

        #######
        #######
        # if isThereUnvisitedAnymore == False:
        mqtt_adapter.publish("mapping",
                             lifecycle_pub_topic)  ## For the stop mapping state check how it is stop mapping state on lifecycle.py.run_mapping_mode()
        graph_map.send_graph_status(pub_topic)

    mqtt_adapter.subscribe(sub_qr_topic, callback_for_qr)
    mqtt_adapter.subscribe(sub_corner_topic, callback_for_corner)
    mqtt_adapter.subscribe(sub_obstacle_topic, callback_for_obstacle)
    mqtt_adapter.loop_forever()


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


def get_new_direction():
    global new_direction
    return new_direction


class Mapping:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(main())
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()
