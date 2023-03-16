import json
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub
from Graph import Graph

g = Graph()
pub_topic = "mapping"
sub_corner_topic = "corner"
sub_qr_topic = "qr"
client = connect_mqtt()

old_posx = 0
old_posy = 0
old_value = "S"

g.add_node(old_value, old_posx, old_posy)

direction = "E"


def update_position(qr, corner_type, direction):
    corner_actions = {
        "UPPER_L1": {"E": ("N", -10, 0), "S": ("W", 0, -10)},
        "UPPER_L2": {"W": ("N", 10, 0), "S": ("E", 0, -10)},
        "DOWN_L1": {"N": ("E", 0, 10), "W": ("S", 10, 0)},
        "DOWN_L2": {"N": ("W", 0, 10), "E": ("S", -10, 0)},
        "T": {"N": (None, 0, 10), "E": (None, -10, 0), "W": (None, 10, 0)},
        "DOWN_T": {"S": (None, 0, -10), "E": (None, 10, 0), "W": (None, -10, 0)},
        "RIGHT_T": {"S": (None, 0, 10), "N": (None, 0, -10), "E": (None, -10, 0)},
        "LEFT_T": {"S": (None, 0, 10), "N": (None, 0, -10), "W": (None, 10, 0)}
    }

    if corner_type in corner_actions:
        action = corner_actions[corner_type].get(direction)
        if action:
            direction, dx, dy = action
            posx, posy = qr.get_pos_x() + dx, qr.get_pos_y() + dy
            if direction:
                return posx, posy, direction

    print(f"Failed to read message from topic {sub_corner_topic}")


def callback_for_qr(client, userdata, msg):
    message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
    parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
    g.add_qr(parts[0], parts[1], parts[2])


def callback_for_corner(client, userdata, msg):
    global direction
    message = msg.payload.decode('utf-8')
    corner_type = message
    nodes = list(g.get_nodes())
    node_id = nodes[len(nodes) - 1]  # Listedeki en son node çağırmak
    past_node = g.get_node(node_id)

    qr_keys = list(g.get_qr_list())
    lastQr = qr_keys[len(qr_keys) - 1]  # en son eklenen qr çağırmak
    qr = g.get_qr(lastQr)

    corner = update_position(qr, corner_type, direction)
    posx = corner[0]
    posy = corner[1]
    direction = corner[2]

    new_node = g.add_node(g.num_of_nodes, posx, posy)
    weight = int(new_node.get_pos_x() - past_node.get_pos_x()) + int(new_node.get_pos_y() - past_node.get_pos_y())
    g.add_edge(past_node, new_node, weight)

    send_data(client, convert_json(g), pub_topic)  # Node değerlerini mqtt'ye göndermek


def convert_json(graph):
    nodes = []
    qr_list = []
    for node_id in graph.nodes:
        node = g.get_node(node_id)
        list_adjacents = []
        list_unvisited_directions = []
        x = node.get_pos_x()
        y = node.get_pos_y()
        adjacents = node.get_connections()
        unvisited_directions = node.get_unvisited_directions()
        for unvisited in unvisited_directions:
            list_unvisited_directions.append(unvisited)
        for adjacent in adjacents:
            list_adjacents.append(adjacent.get_id())

        nodes.append({"id": node.get_id(), "pos": {"x": x, "y": y}, "adjacents": list_adjacents,
                      "unvisitedDirections": list_unvisited_directions})

    for qr_id in graph.qr_list:
        qr = g.get_qr(qr_id)
        qr_list.append({"id": qr.get_id(), "pos": {"x": qr.get_pos_x(), "y": qr.get_pos_y()}})

    graphs = {"nodes": nodes, "qr": qr_list}

    converted_json = json.dumps(graphs)
    return converted_json


mqtt_sub(broker, sub_qr_topic, callback_for_qr, sub_corner_topic, callback_for_corner)
