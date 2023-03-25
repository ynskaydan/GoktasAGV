import json
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub
from entities.Graph import Graph
import os

direction = "E"

db_nodes = open("./Database/node_list.txt", "a")
db_qr = open("./Database/qr_list.txt", "a")
db_obstacle = open("./Database/obstacle_list.txt", "a")


def main():
    global direction
    print("Mapping started! parent id:", os.getppid(), " self id:", os.getpid())
    g = Graph()
    pub_topic = "mapping"
    sub_corner_topic = "corner"
    sub_obstacle_topic = "obstacle"
    sub_qr_topic = "qr"
    sub_topics = [sub_qr_topic, sub_corner_topic, sub_obstacle_topic]
    send_client = connect_mqtt()

    old_posx = 0
    old_posy = 0
    old_value = "S"
    start_node_type = "Start"
    unvisited = {}
    g.add_node(old_value, old_posx, old_posy, start_node_type, unvisited)

    def callback_for_obstacle(client, userdata, msg):
        message = msg.payload.decode('utf-8')

        id = str(g.num_of_obstacle)
        nodes = list(g.get_nodes())
        node_id = nodes[len(nodes) - 1]  # Listedeki en son node çağırmak
        last_node = g.get_node(node_id)
        result = g.add_obstacle(id, last_node.get_pos_x(), 80)
        db_obstacle.write(
            "\n" + str({"id": result.get_id(), "pos": {"x": result.get_posx(), "y": result.get_posy()}}) + "\n")
        print("new obstacle added!")

    def callback_for_qr(client, userdata, msg):
        message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
        parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
        result = g.add_qr(parts[0], parts[1], parts[2])
        if result == 0:
            send_data(client, "QR is already in list", sub_qr_topic)
        db_qr.write(
            "\n" + str({"id": result.get_id(), "pos": {"x": result.get_pos_x(), "y": result.get_pos_y()}}) + "\n")
        print("new qr added!")

    def callback_for_corner(client, userdata, msg):
        global direction
        message = msg.payload.decode('utf-8')
        corner_type = message
        nodes = list(g.get_nodes())
        node_id = nodes[len(nodes) - 1]  # Listedeki en son node çağırmak
        past_node = g.get_node(node_id)

        qr_keys = list(g.get_qr_list())
        last_qr = qr_keys[len(qr_keys) - 1]  # en son eklenen qr çağırmak
        qr = g.get_qr(last_qr)

        corner = get_corner_data(corner_type, qr)
        posx = corner[0]
        posy = corner[1]
        direction = corner[2]
        unvisited_directions = corner[3]

        id = str(g.num_of_nodes)
        new_node = g.add_node(id, posx, posy, corner_type, unvisited_directions)
        weight = int(new_node.get_pos_x() - past_node.get_pos_x()) + int(
            new_node.get_pos_y() - past_node.get_pos_y())

        list_adjacents = []
        g.add_edge(past_node, new_node, weight)
        for adjacent in new_node.get_connections():
            list_adjacents.append(adjacent.get_id())

        db_nodes.write(str({"id": new_node.get_id(), "pos": {"x": new_node.get_pos_x(), "y": new_node.get_pos_y()},
                            "type": new_node.get_type(), "adjacents": list_adjacents,
                            "unvisitedDirections": new_node.get_unvisited_directions()}) + "\n")
        print("new node added!")
        send_data(send_client, convert_json(g), pub_topic)  # Node değerlerini mqtt'ye göndermek

    def get_corner_data(corner_type, qr):
        global direction
        corner_actions = {
            "LEFT_L": {
                "N": (0, 10, "E"),
                "E": (-10, 0, "N"),
                "S": (0, -10, "W"),
                "W": (10, 0, "S"),
            },
            "RIGHT_L": {
                "N": (0, 10, "W"),
                "E": (-10, 0, "S"),
                "S": (0, -10, "E"),
                "W": (10, 0, "N"),
            },
            "T": {
                "N": (0, 10, "W", ["E"]),
                "E": (-10, 0, "E", ["S"]),
                "S": (0, -10, "W", ["S"]),
                "W": (10, 0, "W", ["S"]),
            },
            "DOWN_T": {
                "S": (0, -10, "W", ["E"]),
                "E": (-10, 0, "E", ["N"]),
                "W": (10, 0, "W", ["N"]),
            },
            # "SIDEWAYS_T": {
            #     "N": (0, 10, "W", ["N"]),
            #     "E": (-10, 0, "N", ["S"]),
            #     "S": (0, -10, "W", ["S"]),
            #     "W": (10, 0, "N", ["S"]),
            # },
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

    callback_methods = [callback_for_qr, callback_for_corner, callback_for_obstacle]
    mqtt_sub(broker, sub_topics, callback_methods)


def convert_json(graph):
    nodes = []
    qr_list = []
    obstacles = []
    for node_id in graph.nodes:
        node = graph.get_node(node_id)
        list_adjacents = []
        list_unvisited_directions = []
        x = node.get_pos_x()
        y = node.get_pos_y()
        adjacents = node.get_connections()
        unvisited_directions = node.get_unvisited_directions()
        for un_visited in unvisited_directions:
            list_unvisited_directions.append(un_visited)
        for adjacent in adjacents:
            list_adjacents.append(adjacent.get_id())

        nodes.append(
            {"id": node.get_id(), "pos": {"x": x, "y": y}, "type": node.get_type(), "adjacents": list_adjacents,
             "unvisitedDirections": list_unvisited_directions})

    for qr_id in graph.qr_list:
        qr = graph.get_qr(qr_id)
        qr_list.append({"id": qr.get_id(), "pos": {"x": qr.get_pos_x(), "y": qr.get_pos_y()}})

    for obstacle_id in graph.obstacles:
        obstacle = graph.get_obstacle(obstacle_id)
        obstacles.append({"id": obstacle.get_id(), "pos": {"x": obstacle.get_posx(), "y": obstacle.get_posy()}})

    graphs = {"nodes": nodes, "qr": qr_list, "obstacles": obstacles}

    converted_json = json.dumps(graphs)
    return converted_json
