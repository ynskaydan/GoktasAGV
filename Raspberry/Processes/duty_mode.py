from Services import arduino_manager


class Duty:
    def __init__(self,finish_callback):
        self.finish_callback = finish_callback


    @staticmethod
    def stop_in_point():
        arduino_manager.stop_autonomous_motion_of_vehicle()

    def import_load(self):
        arduino_manager.start_load_mode()
    def export_load(self):
        arduino_manager.stop_load_mode()

