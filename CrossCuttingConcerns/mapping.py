from mqtt import connect_mqtt, broker, port
from sub_mqtt import mqtt_sub


class Node:
    def __init__(self, id):
        self.id = id
        self.adjacents = {}

    def get_id(self):
        return self.id

    def add_adjacent(self, adjacent, weight=0):
        self.adjacents[adjacent] = weight

    def get_connections(self):
        return self.adjacents.keys()

    def get_weight(self, adjacent_id):
        return self.adjacents[adjacent_id]


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = 0
        self.num_of_nodes = 0

    def add_node(self, id):
        self.num_of_nodes += 1
        new_node = Node(id)
        self.nodes[id] = new_node
        return new_node

    def add_edge(self, id, to_id, weight):
        if id not in self.nodes:
            self.add_node(id)
        if to_id not in self.nodes:
            self.add_node(to_id)
        self.nodes[id].add_adjacent(self.nodes[to_id], weight)
        self.edges += 1

    def get_node(self, id):
        return self.nodes[id]

    def get_nodes(self):
        return self.nodes.keys()


old_posx = 0
old_posy = 0
old_value = "S"
g = Graph()


def callback(client, userdata, msg):
    global old_value
    global old_posx
    global old_posy
    qr = msg.payload.decode('utf-8')
    print("Received MQTT message: ", qr)
    partsOfQr = qr.split(";")

    value = partsOfQr[0]
    posx = int(float(partsOfQr[1]))
    posy = int(float(partsOfQr[2]))
    if (posy == old_posy):
        weight = posx - old_posx
    if (posx == old_posx):
        weight = posy - old_posy

    g.add_edge(old_value, value, weight)

    old_value = value
    old_posx = posx
    old_posy = posy

    for node_id in g.get_nodes():  # tüm düğümleri döngüye al
        node = g.get_node(node_id)  # düğümü al
        neighbors = node.get_connections()  # düğümün komşularını al
        for neighbor in neighbors:
            print(f"{node_id}: {neighbor.get_id()} {node.get_weight(neighbor)}")


mqtt_sub(broker, "qr", callback)





