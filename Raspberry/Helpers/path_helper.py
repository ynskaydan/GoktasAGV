import arduino_manager
import mapping
from entities.Node import Node


class PathHelper:
    def __init__(self):
        self.is_path_following = False
        self.target_node = Node(0.0, 0.0, "U", [])
        self.start_node = Node(0.0, 0.0, "U", [])
        self.current_node = Node(0, 0, "U", [])
        self.next_node = Node(0, 0, "U", [])

    def get_next_node(self):
        return self.next_node

    def set_next_node(self, new_node):
        self.next_node = new_node

    def get_is_path_following(self):
        return self.is_path_following

    def get_target_node(self):
        return self.target_node

    def set_is_path_following_flag(self, bool):
        self.is_path_following = bool

    def find_path(self, graph, start_node, end_node):
        self.start_node = start_node
        self.target_node = end_node

        # path finding algorithm: djikstra or some graph traversal
        return [start_node, intermediate_node1, intermediate_node2, end_node]

    def start_follow_path(self, graph, path):
        self.set_is_path_following_flag(True)
        direction = self.required_direction(path[0], path[1])
        turnTo(direction)
        arduino_manager.start_autonomous_motion_of_vehicle()

    def required_direction(self, current_node, next_node):
        return "N"
