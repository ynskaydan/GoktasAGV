class Obstacle:
    def __init__(self, id, posx, posy):
        self.id = id
        self.posx = posx
        self.posy = posy

    def get_id(self):
        return self.id

    def get_posx(self):
        return self.posx

    def get_posy(self):
        return self.posy
