import json
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub
from Graph import Graph
from Raspberry.qr import QR

pub_topic = "mapping"
sub_topic = "qr"
client = connect_mqtt()

list_qr = []
old_posx = 0
old_posy = 0
old_value = "S"
g = Graph()
nodes = []
old_node = g.add_node(old_value, old_posx, old_posy)
nodes.append(old_node)


def callback(client, userdata, msg):
    global old_node  # bir önceki node değerlerini almak

    message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek

    parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
    qr = QR(parts[0], parts[1], parts[2])
    list_qr.append(qr)
    lenght = len(list_qr)

    if lenght >= 2:
        last = list_qr[lenght - 1]
        past = list_qr[lenght - 2]
        last_value = last.get_id()
        last_posx = last.get_pos_x()
        last_posy = last.get_pos_y()

        past_value = past.get_id()
        past_posx = past.get_pos_x()
        past_posy = past.get_pos_y()

        if last_posx == past_posx or last_posy == past_posy:
            if last_posy == past_posy:
                posx = int((last_posx + past_posx) / 2)
                posy = last_posy
                print("as")
            if last_posx == past_posx:
                posy = int((last_posy + past_posy) / 2)
                posx = last_posx
                print("za")

        else:
            posx = last_posx
            posy = past_posy
            print("sa")


        new_node = g.add_node(g.num_of_nodes, posx, posy)
        past_node = nodes[len(nodes) - 1]
        nodes.append(new_node)
        # weight = int(new_node.get_pos_x() - past_node.get_pos_x()) + int(new_node.get_pos_y() - past_node.get_pos_y())
        g.add_edge(past_node, new_node, 20)

    send_data(client, convert_json(g), pub_topic)  # Node değerlerini mqtt'ye göndermek
    print(convert_json(g))


def convert_json(graph):
    nodes = []
    for node_id in graph.nodes:
        node = g.get_node(node_id)
        pos = []
        list_adjacents = []
        x = node.get_pos_x()
        y = node.get_pos_y()
        pos.append({"x": x, "y": y})
        adjacents = node.get_connections()
        for adjacent in adjacents:
            list_adjacents.append({"id": adjacent.get_id()})
        nodes.append({"id": node.get_id(), "pos": pos, "adjacents": list_adjacents})
    graphs = {"nodes": nodes}

    converted_json = json.dumps(graphs)
    return converted_json


mqtt_sub(broker, sub_topic, callback)
