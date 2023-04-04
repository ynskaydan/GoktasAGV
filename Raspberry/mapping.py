from CrossCuttingConcerns import mqtt_adapter
from entities.Graph import Graph
import os

from graph_converter import read_database, convert_json

direction = "E"

db_graph_a = open("./Database/db_graph.txt", "a")
db_graph_r = open("./Database/db_graph.txt", "r")
pub_topic = "mapping"
sub_corner_topic = "corner"
sub_obstacle_topic = "obstacle"
sub_qr_topic = "qr"


def main():
    global g
    global direction
    print("Mapping started! parent id:", os.getppid(), " self id:", os.getpid())
    g = Graph()
    mqtt_adapter.connect("map")
    result = read_database(db_graph_r, g)
    if not result:
        g.add_node("S", 0, 0, "Start", {})
    if result:
        print("Past data write on graph object")

    def callback_for_obstacle(client,userdata,msg):
        obs_id = str(g.num_of_obstacle)
        last_node = g.get_last_node()
        result_add_obstacle = g.add_obstacle(obs_id, last_node.get_pos_x(), 80)
        if result_add_obstacle == 0:
            print("Obstacle already in list")
        else:
            send_graph_status(g)

    def callback_for_qr(client,userdata,msg):
        message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
        parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
        result_add_qr = g.add_qr(parts[0], parts[1], parts[2])
        if result_add_qr == 0:
            mqtt_adapter.publish("QR is already in list", sub_qr_topic)
        else:
            send_graph_status(g)

    def callback_for_corner(client,userdata,msg):
        message = msg.payload.decode('utf-8')
        corner_type = message
        result_add_node = add_node(g, corner_type)

        if result_add_node != str(0):
            node_id = result
            visit_unvisited_direction(node_id)

        send_graph_status(g)  # Node değerlerini mqtt'ye göndermek

    mqtt_adapter.subscribe(sub_qr_topic, callback_for_qr)
    mqtt_adapter.subscribe(sub_corner_topic, callback_for_corner)
    mqtt_adapter.subscribe(sub_obstacle_topic, callback_for_obstacle)
    mqtt_adapter.loop_forever()


def visit_unvisited_direction(node_id):
    global direction
    node = g.get_node(node_id)
    direction = node.del_unvisited_direction()


def send_graph_status(graph):
    json_graph = convert_json(graph)
    db_graph_a.write(json_graph + "\n")
    mqtt_adapter.publish(json_graph, pub_topic)


def add_node(graph, corner_type):
    global direction
    past_node = graph.get_last_node()
    last_qr = graph.get_last_qr()
    corner = get_corner_data(corner_type, last_qr)
    posx = corner[0]
    posy = corner[1]
    direction = corner[2]
    unvisited_directions = corner[3]
    result_check = graph.check_node_exist(posx, posy)
    print(result_check)
    if result_check == "none":
        node_id = str(graph.num_of_nodes)
        new_node = graph.add_node(node_id, posx, posy, corner_type, unvisited_directions)
        graph.add_edge(past_node, new_node)
        print(past_node.get_weight(new_node))
        return str(0)
    else:
        return result_check


def get_corner_data(corner_type, qr):
    global direction
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
