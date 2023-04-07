class Obstacle():
    def __init__(self, id, pos_x, pos_y):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_id(self):
        return self.id

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
