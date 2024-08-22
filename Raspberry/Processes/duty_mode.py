from Services import arduino_manager

import os
from Helpers.graph_converter import convert_json
from Services import arduino_manager, direction_manager
from CrossCuttingConcerns import mqtt_adapter, raspi_log
from Helpers import path_helper
from entities.Graph import Graph
from Helpers.graph_converter import read_database
from entities.Scenario import Scenario

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(dir_path), 'Database', 'db_scenario.txt')
try:
    db_scenario = open(file_path, "a")
except FileNotFoundError:
    raspi_log.log_process("No scenario history found")
    db_graph = open(file_path, "w")
direction = ""
isPathFollowing = False
pub_topic = "decision"
sub_corner_topic = "intersection"


class Duty:
    def __init__(self,finish_callback,scenarioId):
        self.finish_callback = finish_callback
        raspi_log.log_process(str(f"Duty started! parent id: {os.getppid()},  self id: {os.getpid()}"))
        self.scenario = Scenario(scenarioId)
        self.direction_controller = direction_manager.Direction()


    @staticmethod
    def stop_in_point():
        arduino_manager.stop_autonomous_motion_of_vehicle()

    def import_load(self):
        arduino_manager.start_load_mode()
    def export_load(self):
        arduino_manager.stop_load_mode()







    @staticmethod
    def get_direction():
        global direction
        return direction
    @staticmethod
    def send_graph_status(graph):
        json_graph = convert_json(graph)
        db_graph.write(json_graph + "\n")
        mqtt_adapter.publish(json_graph, pub_topic)


