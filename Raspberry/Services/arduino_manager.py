
import lifecycle
from Processes import mapping

from CrossCuttingConcerns import mqtt_adapter, raspi_log

sub_intersection_topic = "intersection"
sub_imu_topic = "imu"
pub_topic = "corner"
pub_auto_motion_control = "auto-motion"
pub_load_topic = "load"

def main():
    mqtt_adapter.connect("ard")

def send_arduino_to_decision(corner_type, new_direction):
    prev_direction = mapping.Mapping.get_direction()
    movement_dict = {  # gitmesini istediğim directiona göre vermem gerekiyor?
        ("LEFT_T", "S"): "LEFT",
        ("LEFT_T", "W"): "FORWARD",
        ("LEFT_T", "N"): "LEFT",
        ("LEFT_T", "E"): "FORWARD",
        ("RIGHT_T", "W"): "FORWARD",
        ("RIGHT_T", "N"): "RIGHT",
        ("RIGHT_T", "E"): "FORWARD",
        ("RIGHT_T", "S"): "RIGHT",
        ("T", ("N", "E")): "RIGHT",
        ("T", ("N", "W")): "LEFT",
        ("T", ("S", "E")): "LEFT",
        ("T", ("S", "W")): "RIGHT",
    }

    # Use the dictionary to determine the desired movement action based on the given corner type and direction
    if (corner_type, new_direction) in movement_dict:
        mqtt_adapter.publish(client,movement_dict[(corner_type, new_direction)], pub_auto_motion_control)
        raspi_log.log_process(movement_dict[(corner_type, new_direction)])
    elif corner_type == "T" and (prev_direction, new_direction) in movement_dict:
        mqtt_adapter.publish(client,movement_dict[(corner_type, (prev_direction, new_direction))], pub_auto_motion_control)
        raspi_log.log_process(movement_dict[(corner_type, new_direction)])


def start_obstacle_flow(distance):
    mqtt_adapter.publish(client,"obstacle", pub_auto_motion_control)

def turn_to_direction(direction):
    mqtt_adapter.publish(client,f"TURN TO {direction}",pub_auto_motion_control)

def stop_autonomous_motion_of_vehicle():
    message = "STOP-AUTO-MOTION"
    mqtt_adapter.publish(client,message, pub_auto_motion_control)
    raspi_log.log_process(message)


def start_autonomous_motion_of_vehicle():
    message = "START-AUTO-MOTION"
    mqtt_adapter.publish(client,message, pub_auto_motion_control)
    raspi_log.log_process(message)

def start_load_mode():
    message = "importload"
    mqtt_adapter.publish(client,message, pub_load_topic)


def stop_load_mode():
    message = "exportload"
    mqtt_adapter.publish(client,message, pub_load_topic)
