from datetime import time

from Services import arduino_manager
from CrossCuttingConcerns import raspi_log
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
        raspi_log.log_process("Finding Path is on processing")
        unchecked_nodes = list(graph.get_nodes())  # Keşfedilmemiş düğümler listesi
        distances = {node: float('inf') for node in graph.nodes}  # Başlangıç mesafeleri sonsuz olarak ayarlanır
        distances[start_node] = 0  # i
        previous_nodes = {}  # a dictionary for previous nodes

        while unchecked_nodes:
            # Keşfedilmemiş düğümler arasından en küçük mesafeye sahip düğümü bul
            current_node = min(unchecked_nodes, key=lambda node: distances[node])

            if current_node == end_node:
                break  # Hedef düğüme ulaşıldıysa döngüyü sonlandır

            unchecked_nodes.remove(current_node)  # Şu anki düğümü keşfedildi olarak işaretle

            # Şu anki düğümün komşularını güncelle
            for adjacent in graph.nodes[current_node]:
                # Başlangıçtan bu komşuya olan yeni mesafeyi hesapla
                distance = distances[current_node] + graph.nodes[current_node][adjacent]
                # Yeni mesafe, daha kısa ise güncelle
                if distance < distances[adjacent]:
                    distances[adjacent] = distance
                    previous_nodes[adjacent] = current_node

        # Hedef düğüme ulaşılamadıysa None döndür
        if end_node not in previous_nodes:
            return None

        # En kısa yolu oluştur
        path = [end_node]
        while path[-1] != start_node:
            path.append(previous_nodes[path[-1]])
        path.reverse()
        raspi_log.log_process("Path is created. Path will be followed.")
        return path
        # path finding algorithm: djikstra or some graph traversal

    def start_follow_path(self, graph, path):
        self.set_is_path_following_flag(True)
        raspi_log.log_process("Path following is started.")
        current_node_index = 0
        direction = self.required_direction(graph,path[current_node_index], path[current_node_index + 1])
        arduino_manager.turn_to_direction(direction)
        arduino_manager.start_autonomous_motion_of_vehicle()


    @staticmethod
    def required_direction(graph, current_node_index, next_node_index):
        #calculates required direction
        current_node = graph.get_node(current_node_index)
        next_node = graph.get_node(next_node_index)

        if current_node.get_pos_x() == next_node.get_pos_x():
            if current_node.get_pos_y() < next_node.get_pos_y():
                return "forward"
            elif current_node.get_pos_y == next_node.get_pos_y():
                return "stop"
            else:
                return "backward"
        else:
            if current_node.get_pos_x < next_node.get_pos_x:
                return "right"
            else:
                return "left"

    def check_if_at_node(self,node):
        if self.current_node != node:
            return False
        else:
            return True