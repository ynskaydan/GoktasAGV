from CrossCuttingConcerns import raspi_log


class Direction:
    def __int__(self):
        self.direction = ""

    def get_direction(self):
        raspi_log.log_process(f"Direction is {self.direction}")
        return self.direction
    def set_direction(self,new_direction):
        raspi_log.log_process(f"New direction is {new_direction}")
        self.direction = new_direction
