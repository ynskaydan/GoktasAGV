from CrossCuttingConcerns import raspi_log
from entities.Node import Node
from entities.obstacle import Obstacle
from entities.qr import QR


class Graph:
    def __init__(self):
        self.nodes = {}
        self.qr_list = {}
        self.obstacles = {}
        self.edges = {}
        self.num_of_nodes = 0
        self.num_of_obstacle = 0
        self.num_of_qr = 0

    def get_nodes(self):
        return self.nodes.keys()

    def add_node(self, pos_x, pos_y, node_type, unvisited, node_id=None):
        self.num_of_nodes += 1
        new_node = Node(pos_x, pos_y, node_type, unvisited, node_id or str(self.num_of_nodes))
        self.nodes[new_node.get_id()] = new_node
        return new_node

    def get_edge_weight(self, from_id, to_id):
        weight = self.nodes[from_id].adjacents[to_id]
        return weight

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return self.nodes.get(node_id)
        else:
            return 0

    def get_last_node(self):
        nodes_list = list(self.nodes.items())
        last_node = nodes_list[len(self.nodes)-1]

        # last_node = nodes[len(self.nodes) - 1]  # Listedeki en son node çağırmak
        return last_node

    def add_edge(self, from_node, to_node):
        weight = 0

        s_node_pos_x = from_node.get_pos_x()
        s_node_pos_y = from_node.get_pos_y()
        f_node_pos_x = to_node.get_pos_x()
        f_node_pos_y = to_node.get_pos_y()

        if f_node_pos_x - s_node_pos_x == 0:
            weight = abs(f_node_pos_y - s_node_pos_y)
        if f_node_pos_y - s_node_pos_y == 0:
            weight = abs(f_node_pos_x - s_node_pos_x)

        from_node.add_adjacent(to_node, weight)
        to_node.add_adjacent(from_node, weight)

        if from_node not in self.edges:
            self.edges[from_node] = []
        if to_node not in self.edges:
            self.edges[to_node] = []
        self.edges[from_node].append((to_node, weight))
        self.edges[to_node].append((from_node, weight))

    def add_new_intersection(self, corner_type, pos_x, pos_y, unvisited_directions, node_id):
        new_node = self.add_node(pos_x, pos_y, corner_type, unvisited_directions, node_id)
        if len(self.nodes) > 1:
            past_node = self.get_last_node()
            self.add_edge(past_node, new_node)
        message = str(f"New intersection at ({pos_x},{pos_y}) is added to map! ")
        raspi_log.log_process(message)

    @staticmethod
    def visit_unvisited_direction(node):
        new_direction = node.del_unvisited_direction()
        return new_direction

    def already_visited_node(self, pos_x, pos_y):
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if node.get_pos_x() == int(pos_x) and node.get_pos_y() == int(pos_y):
                return node
        return None

    def check_node_already_exist(self, pos_x, pos_y):
        node_exists = False
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if node.get_pos_x() == pos_x and node.get_pos_y() == pos_y:
                message = str(f"Faced with already visited intersection at ({pos_x},{pos_y})")
                raspi_log.log_process(message)
                node_exists = True
                break
        return node_exists

    def add_qr(self, qr_id, pos_x, pos_y):
        self.num_of_qr += 1
        if qr_id not in self.qr_list:
            new_qr = QR(qr_id, pos_x, pos_y)
            self.qr_list[id] = new_qr
            message = str(f"New QR at ({pos_x},{pos_y}) is added to map! ")
            raspi_log.log_process(message)
            return new_qr
        else:
            raspi_log.log_process(str(f"QR {qr_id} has already in list"))
            return 0

    def add_obstacle(self, pos_x, pos_y):
        for obstacle in self.obstacles:
            if obstacle.get_pos_x() == pos_x:
                return None
        obs_id = str(self.num_of_obstacle)
        new_obstacle = Obstacle(obs_id, pos_x, pos_y)
        self.obstacles[obs_id] = new_obstacle
        self.num_of_obstacle += 1
        message = str(f"Faced obstacle at ({pos_x},{pos_y}) is added to map!")
        raspi_log.log_process(message)
        return new_obstacle

    def get_last_qr(self):
        key_list = list(self.qr_list.keys())
        last_key = key_list[self.num_of_qr - 1]
        last_qr = self.get_qr(last_key)

        return last_qr

    def get_obstacle(self, obs_id):
        if obs_id in self.obstacles.keys():
            return self.nodes[obs_id]
        else:
            return 0

    def get_qr(self, qr_id):
        if qr_id in self.qr_list.keys():
            return self.qr_list[qr_id]
        else:
            return 0

    def nodes_having_unvisited_direction(self):
        nodes_having_unvisited = []
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if len(node.get_unvisited_directions()) > 0:
                nodes_having_unvisited.append(node_id)
        return nodes_having_unvisited
