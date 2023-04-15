from CrossCuttingConcerns import raspi_log
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

<<<<<<< HEAD
    def add_node(self, pos_x, pos_y, node_type, unvisited, node_id=None): 
=======
    def add_node(self, pos_x, pos_y, node_type, unvisited, node_id=None):
>>>>>>> main
        self.num_of_nodes += 1
        new_node = Node(pos_x, pos_y, node_type, unvisited, node_id or str(self.num_of_nodes))
        self.nodes[new_node.get_id()] = new_node
        return new_node
<<<<<<< HEAD
   
=======

    def get_edge_weight(self, from_id, to_id):
        weight = self.nodes[from_id].adjacents[to_id]
        return weight
>>>>>>> main

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return Node(self.nodes.get(node_id))
        else:
            return 0

    def get_last_node(self):
        nodes_list = list(self.nodes.keys())
        last_node = self.nodes[nodes_list[len(nodes_list) - 1]]

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
        self.edges += 1

    def add_new_intersection(self, corner_type, pos_x, pos_y, unvisited_directions, node_id=None):
        new_node = self.add_node(pos_x, pos_y, corner_type, unvisited_directions, node_id)
        if len(self.nodes) > 1:
            past_node = self.get_last_node()
            self.add_edge(past_node, new_node)
        message = str(f"New intersection at ({pos_x},{pos_y}) is added to map! ")
        raspi_log.log_process(message)

<<<<<<< HEAD
    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            
            return self.nodes.get(node_id)
=======
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
        if id not in self.qr_list:
            new_qr = QR(qr_id, pos_x, pos_y)
            self.qr_list[id] = new_qr
            message = str(f"New QR at ({pos_x},{pos_y}) is added to map! ")
            raspi_log.log_process(message)
            return new_qr
>>>>>>> main
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
            return self.nodes[qr_id]
        else:
            return 0

<<<<<<< HEAD
    def get_last_node(self):
        last_node = self.nodes.get(str(self.num_of_nodes))
        # last_node = nodes[len(self.nodes) - 1]  # Listedeki en son node çağırmak
        return last_node

    def add_new_intersection(self, corner_type, posx, posy, unvisited_directions, node_id=None):
        past_node = self.get_last_node()
        new_node = self.add_node(posx, posy, corner_type, unvisited_directions, node_id)
        self.add_edge(past_node, new_node)

    def visit_unvisited_direction(self, node_id):
        node = self.get_node(node_id)
        new_direction = node.del_unvisited_direction()
        return new_direction

    def already_visited_node(self, posx, posy):
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if node.get_pos_x() == int(posx) and node.get_pos_y() == int(posy):
                return node
        return None

    def check_node_already_exist(self,pos_x,pos_y):
        node_exists = False
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if node.get_pos_x() == pos_x and node.get_pos_y() == pos_y:
                node_exists = True
                break
        return node_exists

    def get_last_qr(self):
        key_list = list(self.qr_list.keys())
        last_key = key_list[self.num_of_qr - 1]
        last_qr = self.get_qr(last_key)

        return last_qr
    
    def nodes_having_unvisited_direction(self):
        nodes_having_unvisited = []
        for node_id in self.nodes.keys:
            node = self.get_node(node_id)
            if node.get_unvisited_directions() > 0:
                nodes_having_unvisited.append(node_id)
        return nodes_having_unvisited
=======
    def nodes_having_unvisited_direction(self):
        nodes_having_unvisited = []
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if node.get_unvisited_directions() > 0:
                nodes_having_unvisited.append(node_id)
        return nodes_having_unvisited
>>>>>>> main
