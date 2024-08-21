class Scenario:
    def __init__(self, id):
        def __init__(self):
            self.id = id
            self.scenario  = {}
            self.commands = {}
            self.num_of_commands = 0


    def scenarioAccordingToScenarioId(self,id):
        if id == 1:
            self.scenario = {'S1', 'F', 'S2', 'A', 'E', 'S1', 'C', 'D', 'G', 'S1', 'B', 'S2', 'F', 'S1'}
            self.commands = {'right','forward','right','right','right','forward','right','left','left','left','forward','forward','left','left','left','stop'}
            self.num_of_commands = 16




