from Node import Node
from Raspberry.qr import QR


class Graph:
    def __init__(self):
        self.nodes = {}
        self.qr_list = {}
        self.edges = 0
        self.num_of_nodes = 0
        self.num_of_qr = 0

    def add_node(self, id, posx, posy):
        self.num_of_nodes += 1
        new_node = Node(id, posx, posy)
        self.nodes[id] = new_node
        return new_node

    def add_qr(self, id, posx, posy):
        self.num_of_qr += 1
        new_qr = QR(id, posx, posy)
        self.qr_list[id] = new_qr
        return new_qr

    def get_qr(self, id):
        return self.qr_list[id]

    def add_edge(self, from_node, to_node, weight):
        from_node.add_adjacent(to_node, weight)
        to_node.add_adjacent(from_node, weight)
        self.edges += 1

    def get_edge_weight(self, id, to_id):
        weight = self.nodes[id].adjacents[to_id]
        return weight

    def get_node(self, id):
        return self.nodes[id]

    def get_nodes(self):
        return self.nodes.keys()

    def get_qr_list(self):
        return self.qr_list.keys()
