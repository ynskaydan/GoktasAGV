from entities.Node import Node
from entities.obstacle import Obstacle
from entities.qr import QR


class Graph:
    def __init__(self):
        self.nodes = {}
        self.qr_list = {}
        self.obstacles = {}
        self.edges = 0
        self.num_of_nodes = 0
        self.num_of_obstacle = 0
        self.num_of_qr = 0

    def add_node(self, id, posx, posy, type, unvisited):
        self.num_of_nodes += 1
        new_node = Node(id, posx, posy, type, unvisited)
        self.nodes[id] = new_node
        return new_node

    def add_qr(self, id, posx, posy):
        self.num_of_qr += 1
        if id not in self.qr_list:
            new_qr = QR(id, posx, posy)
            self.qr_list[id] = new_qr
            return new_qr
        else:
            print(f"QR {id} has already in list")
            return 0

    def add_obstacle(self, id, posx, posy):
        self.num_of_obstacle += 1
        for obstacle_id in self.get_obstacles():
            obstacle = self.get_obstacle(obstacle_id)
            if posx == obstacle.get_posx():
                return 0
        new_obstacle = Obstacle(id, posx, posy)
        self.obstacles[id] = new_obstacle
        return new_obstacle

    def get_obstacle(self, id):
        return self.obstacles[id]

    def get_qr(self, id):
        return self.qr_list[id]

    def add_edge(self, from_node, to_node):
        weight = 0
        s_node_pos_x = from_node.get_pos_x()
        s_node_pos_y = from_node.get_pos_y()
        f_node_pos_x = to_node.get_pos_x()
        f_node_pos_y = to_node.get_pos_y()


        if f_node_pos_x - s_node_pos_x == 0:
            weight = abs(f_node_pos_y - s_node_pos_y)
        if f_node_pos_y - s_node_pos_y == 0:
            weight = abs(f_node_pos_x- s_node_pos_x)

        from_node.add_adjacent(to_node, weight)
        to_node.add_adjacent(from_node, weight)
        self.edges += 1

    def get_edge_weight(self, id, to_id):
        weight = self.nodes[id].adjacents[to_id]
        return weight

    def get_node(self, id):
        if id in self.get_nodes():
            return self.nodes[id]
        else:
            return 0

    def get_nodes(self):
        return self.nodes.keys()

    def get_qr_list(self):
        return self.qr_list.keys()

    def get_obstacles(self):
        return self.obstacles.keys()

    def check_node_exist(self, posx, posy):
        exist = "none"
        for node_id in self.nodes:
            node = self.nodes[node_id]
            if node.get_pos_x() == int(posx) and node.get_pos_y() == int(posy):
                exist = node_id
                break
        return exist
    def get_last_node(self):
        last_node = self.nodes.get(str(self.num_of_nodes))
        #last_node = nodes[len(self.nodes) - 1]  # Listedeki en son node çağırmak
        return last_node
    def get_last_qr(self):
        key_list = list(self.get_qr_list())
        last_key = key_list[self.num_of_qr-1]
        last_qr = self.get_qr(last_key)

        return last_qr



