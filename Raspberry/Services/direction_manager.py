from CrossCuttingConcerns import raspi_log


class Direction:
    def __init__(self):
        self.currentDirection = "N"

    def get_direction(self):
        raspi_log.log_process(f"Direction is {self.currentDirection}")
        return self.currentDirection
    def set_direction(self,new_direction):
        raspi_log.log_process(f"New direction is {new_direction}")
        self.currentDirection = new_direction
