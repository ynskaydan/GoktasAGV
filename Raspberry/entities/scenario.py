class Scenario:
    def __init__(self, id, name, nodeList):
        self.id = id
        self.name = name
        self.nodeList = nodeList

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_nodes(self):
        return self.nodeList
