class QR:
    def __init__(self, id, posx, posy):
        self.id = id
        self.posx = posx
        self.posy = posy

    def get_id(self):
        return self.id

    def get_pos_x(self):
        return int(float(self.posx))

    def get_pos_y(self):
        return int(float(self.posy))
