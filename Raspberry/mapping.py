import json
from CrossCuttingConcerns.mqtt import connect_mqtt, send_data, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub
from Graph import Graph


pub_topic = "mapping"
sub_topic = "corners"
client = connect_mqtt()


old_posx = 100
old_posy = 0
old_value = "S"
g = Graph()


def callback(client, userdata, msg):
    global old_value
    global old_posx # bir önceki node değerlerini almak
    global old_posy

    corner = msg.payload.decode('utf-8') # dinlenen veriyi anlamlı hale getirmek

    parts = corner.split(";") # QR etiketinin standart halinde pozisyonu ayrıştırmak
    value = parts[0]
    posx = float(parts[1])
    posy = float(parts[2])
    weight = 0
    if posy == old_posy:
        weight = posx - old_posx
    if posx == old_posx:
        weight = posy - old_posy

    g.add_edge(old_value, old_posx, old_posy, value, posx, posy, weight)

    send_data(client, convert_json(g), pub_topic) # Node değerlerini mqtt'ye göndermek
    print(convert_json(g))

    old_value = value
    old_posx = posx
    old_posy = posy


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
