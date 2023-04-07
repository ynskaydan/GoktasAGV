from CrossCuttingConcerns import mqtt_adapter
from entities.Node import Node
from entities.obstacle import Obstacle
from entities.qr import QR
from graph_converter import convert_json
from mapping import db_graph_a


class Graph:
    def __init__(self):
        self.nodes = {}
        self.qr_list = {}
        self.obstacles = {}
        self.edges = 0
        self.num_of_nodes = 0
        self.num_of_obstacle = 0
        self.num_of_qr = 0

    def add_node(self, pos_x, pos_y, node_type, unvisited, node_id=None):

        node_exists = False
        for node in self.nodes.keys():
            if node.get_pos_x() == pos_x and node.get_pos_y() == pos_y:
                node_exists = True
                break

        if not node_exists:
            self.num_of_nodes += 1
            new_node = Node(pos_x, pos_y, node_type, unvisited, node_id or str(self.num_of_nodes))
            self.nodes[new_node.get_id()] = new_node
            return new_node
        else:
            return None

    def add_qr(self, qr_id, posx, posy):
        self.num_of_qr += 1
        if id not in self.qr_list:
            new_qr = QR(qr_id, posx, posy)
            self.qr_list[id] = new_qr
            return new_qr
        else:
            print(f"QR {qr_id} has already in list")
            return 0

    def add_obstacle(self, pos_x, pos_y):
        for obstacle in self.obstacles.keys():
            if obstacle.get_pos_x() == pos_x:
                return None
        obs_id = str(self.num_of_obstacle)
        new_obstacle = Obstacle(obs_id, pos_x, pos_y)
        self.obstacles[obs_id] = new_obstacle
        self.num_of_obstacle += 1
        return new_obstacle

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

    def get_edge_weight(self, from_id, to_id):
        weight = self.nodes[from_id].adjacents[to_id]
        return weight

    def get_node(self, node_id):
        if node_id in self.nodes.keys():
            return self.nodes[node_id]
        else:
            return 0

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

    def get_last_node(self):
        last_node = self.nodes.get(str(self.num_of_nodes))
        # last_node = nodes[len(self.nodes) - 1]  # Listedeki en son node çağırmak
        return last_node

    def add_new_intersection(self, corner_type, posx, posy, unvisited_directions, node_id=None):
        past_node = self.get_last_node()
        new_node = self.add_node(posx, posy, corner_type, unvisited_directions, node_id)
        if new_node != str(0):
            self.add_edge(past_node, new_node)
            return True
        else:
            return False

    def visit_unvisited_direction(self, node_id):
        node = self.get_node(node_id)
        new_direction = node.del_unvisited_direction()
        return new_direction

    def catch_same_node(self, posx, posy):
        for node_id in self.nodes.keys():
            node = self.get_node(node_id)
            if node.get_pos_x() == int(posx) and node.get_pos_y() == int(posy):
                return node_id
        return None

    def send_graph_status(self, pub_topic):
        json_graph = convert_json(self)
        db_graph_a.write(json_graph + "\n")
        mqtt_adapter.publish(json_graph, pub_topic)

    def get_last_qr(self):
        key_list = list(self.qr_list.keys())
        last_key = key_list[self.num_of_qr - 1]
        last_qr = self.get_qr(last_key)

        return last_qr
