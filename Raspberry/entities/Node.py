class Node:
    def __init__(self, pos_x, pos_y, type, unvisiteds, node_id=None):
        self.id = node_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.adjacents = {}
        self.unvisited_directions = []
        for unvisited in unvisiteds:
            self.unvisited_directions.append(unvisited)
        self.type = type

    def get_id(self):
        return self.id

    def add_adjacent(self, adjacent, weight=0):
        self.adjacents[adjacent] = weight

    def get_connections(self):
        return self.adjacents.keys()

    def get_unvisited_directions(self):
        return self.unvisited_directions

    def del_unvisited_direction(self):
        if len(self.unvisited_directions) > 0:
            result = self.unvisited_directions.pop(0)
            return result

    def get_weight(self, adjacent_id):
        return self.adjacents[adjacent_id]

    def get_type(self):
        return self.type

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
