import json
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub
from Graph import Graph
import paho.mqtt.client as mqtt
from qr import QR
from Raspberry.qr import QR

g = Graph()
pub_topic = "mapping"
sub_corner_topic = "corner"
sub_qr_topic = "qr"
client = connect_mqtt()

old_posx = 0
old_posy = 0
old_value = "S"

g.add_node(old_value, old_posx, old_posy)


# client = mqtt.Client()

def callbackForQR(client, userdata, msg):
    message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
    parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
    g.add_qr(parts[0], parts[1], parts[2])


def callbackForCorner(client, userdata, msg):
    message = msg.payload.decode('utf-8')

    nodes = list(g.get_nodes())
    node_id = nodes[len(nodes) - 1]  # Listedeki en son node çağırmak
    past_node = g.get_node(node_id)

    qr_keys = list(g.get_qr_list())
    lastQr = qr_keys[len(qr_keys) - 1]  # en son eklenen qr çağırmak
    qr = g.get_qr(lastQr)
    ###############################################
    posx = qr.get_pos_x() + 10  # deneme
    posy = qr.get_pos_y()
    ##################################################

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


mqtt_sub(broker, sub_qr_topic, callbackForQR, sub_corner_topic, callbackForCorner)
