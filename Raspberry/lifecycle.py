import os

import mapping
from CrossCuttingConcerns import mqtt_adapter, raspi_log

db_state_a = open("./Database/db_state.txt", "a")
db_state_r = open("./Database/db_state.txt", "r")
last_state = ""
topic = "mode"
sub_corner_topic = "intersection"
sub_obstacle_topic = "obstacle"
sub_qr_topic = "qr"
pub_topic = "mapping"

IDLE_STATE = "IDLE_STATE"
MAPPING_STATE = "MAPPING_STATE"
DUTY_STATE = "DUTY_STATE"
INIT_STATE = "INIT_STATE"

state = IDLE_STATE


def callback_for_qr(client, userdata, msg):
    mapping_mode.callback_for_qr(msg)


def callback_for_corner(client, userdata, msg):
    mapping_mode.callback_for_corner(msg)


def callback_for_obstacle(client, userdata, msg):
    mapping_mode.callback_for_obstacle(msg)


def main():
    global mapping_mode
    global state
    raspi_log.log_process(str(f"Lifecycle started! parent id:, {os.getppid()},  self id:, {os.getpid()}"))
    mqtt_adapter.connect("lifecycle-main")
    lines = db_state_r.readlines()
    if len(lines) > 0:
        state = str(lines[len(lines) - 1])
        raspi_log.log_process(state)
    else:
        state = IDLE_STATE  # idle

    # mapping_mode = mapping.Mapping(finish_callback)

    mqtt_adapter.subscribe(topic, on_message)
    mqtt_adapter.subscribe(sub_qr_topic, callback_for_qr)
    mqtt_adapter.subscribe(sub_corner_topic, callback_for_corner)
    mqtt_adapter.subscribe(sub_obstacle_topic, callback_for_obstacle)
    process_state(state)
    mqtt_adapter.loop_forever()


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    process_state(message)


def finish_callback():
    global state
    topic_stat = "stateStatus"
    mqtt_adapter.publish(state, topic_stat)
    message = str(f"Mapping is finished. New state is {state}")
    state = INIT_STATE
    raspi_log.log_process(message)
    process_state(state)
    # change state to idle
    # inform gui


def run_explore_mode():
    global state
    global mapping_mode
    # mapping_mode = mapping.Mapping()
    if state == IDLE_STATE:
        state = MAPPING_STATE
        raspi_log.log_process("Mapping state active!")
        save_last_state()
        mapping_mode = mapping.Mapping(finish_callback)


def run_duty_mode():
    global state
    if state == INIT_STATE:
        state = DUTY_STATE
        # import_load.start()
        raspi_log.log_process("Duty Active")
        save_last_state()


def run_idle_mode():
    global state
    state = IDLE_STATE
    raspi_log.log_process("Idle mode active. Waiting for followings orders")
    save_last_state()


def run_init_mode():
    global state
    raspi_log.log_process("Init mode active. Waiting for followings duties")
    save_last_state()


state_functions = {
    IDLE_STATE: run_idle_mode,
    MAPPING_STATE: run_explore_mode,
    INIT_STATE: run_init_mode,
    DUTY_STATE: run_duty_mode,
}


def process_state(message):
    if message in state_functions:
        state_functions[message]()


def save_last_state():
    global state
    db_state_a.write("\n" + state)


def get_last_state():
    return state
