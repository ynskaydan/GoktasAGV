import imu_manager
import lifecycle
import mapping

from CrossCuttingConcerns import mqtt_adapter, raspi_log

sub_intersection_topic = "intersection"
sub_imu_topic = "imu"
pub_topic = "corner"
pub_auto_motion_control = "auto-motion"


def main():
    mqtt_adapter.connect("ard")
    mqtt_adapter.subscribe(sub_intersection_topic, callback_for_intersection())


def callback_for_intersection(client, userdata, msg):
    message = msg.payload.decode('utf-8')  # takes LEFT_T,LEFT_L,RIGHT_L etc
    new_direction = ""
    if lifecycle.get_last_state() == "explore":
        new_direction = mapping.get_new_direction()
    send_arduino_to_decision(message, new_direction)


def send_arduino_to_decision(corner_type, new_direction):
    prev_direction = imu_manager.get_direction()
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
        mqtt_adapter.publish(movement_dict[(corner_type, new_direction)], sub_intersection_topic)
    elif corner_type == "T" and (prev_direction, new_direction) in movement_dict:
        mqtt_adapter.publish(movement_dict[(corner_type, (prev_direction, new_direction))], sub_intersection_topic)


def stop_autonomous_motion_of_vehicle():
    message = "STOP-AUTO-MOTION"
    mqtt_adapter.publish(message, pub_auto_motion_control)
    raspi_log.log_process(message)

def start_autonomous_motion_of_vehicle():
    message = "START-AUTO-MOTION"
    mqtt_adapter.publish(message,pub_auto_motion_control)
    raspi_log.log_process(message)
