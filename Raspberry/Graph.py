from Node import Node


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = 0
        self.num_of_nodes = 0

    def add_node(self, id, posx, posy):
        self.num_of_nodes += 1
        new_node = Node(id, posx, posy)
        self.nodes[id] = new_node
        return new_node

    def add_edge(self, id, old_posx, old_posy, to_id, posx, posy, weight):
        if id not in self.nodes:
            self.add_node(id, old_posx, old_posy)
        if to_id not in self.nodes:
            self.add_node(to_id, posx, posy)
        self.nodes[id].add_adjacent(self.nodes[to_id], weight)
        self.edges += 1

    def get_edge_weight(self, id, to_id):
        weight = self.nodes[id].adjacents[to_id]
        return weight

    def get_node(self, id):
        return self.nodes[id]

    def get_nodes(self):
        return self.nodes.keys()
