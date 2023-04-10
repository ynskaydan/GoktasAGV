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


def main():
    global state
    lines = db_state_r.readlines()
    if len(lines) > 0:
        state = str(lines[len(lines) - 1])
        raspi_log.log_process(state)
    else:
        state = IDLE_STATE  # idle

    mqtt_adapter.connect("md")
    mqtt_adapter.subscribe(topic, on_message)
    process_state(state)
    mqtt_adapter.loop_forever()


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    process_state(message)


def run_explore_mode():
    global state
    mapping_mode = mapping.Mapping()
    if state == IDLE_STATE:
        state = MAPPING_STATE
        raspi_log.log_process("Mapping Active")
        save_last_state()
        mapping_mode = mapping.Mapping()


def run_duty_mode():
    global state
    state = DUTY_STATE
    # import_load.start()
    raspi_log.log_process("Duty Active")
    save_last_state()


def run_idle_mode():
    raspi_log.log_process("Idle mode active. Waiting for followings orders")
    save_last_state()


def run_import_mode():
    save_last_state()
    try:
        raspi_log.log_process("importing")

    except:
        raspi_log.log_process(str(BaseException))


def run_export_mode():
    save_last_state()
    try:
        raspi_log.log_process("exporting")
    except AssertionError:
        raspi_log.log_process(str("Cannot start a process twitce"))


mode_functions = {
    "idle": run_idle_mode,
    "explore": run_explore_mode,
    "import": run_import_mode,
    "export": run_export_mode,
    "duty": run_duty_mode,
}


def process_state(message):
    if message in mode_functions:
        mode_functions[message]()


def save_last_state():
    global state
    db_state_a.write("\n" + state)


def get_last_state():
    return state


mqtt_adapter.subscribe(sub_qr_topic, callback_for_qr)
mqtt_adapter.subscribe(sub_corner_topic, callback_for_corner)
mqtt_adapter.subscribe(sub_obstacle_topic, callback_for_obstacle)
mqtt_adapter.loop_forever()
