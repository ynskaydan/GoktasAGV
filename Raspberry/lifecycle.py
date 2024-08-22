import os
from Helpers.path_helper import PathHelper
from Processes import mapping, duty_mode
from CrossCuttingConcerns import mqtt_adapter, raspi_log
from Services import direction_manager

last_state = ""
topic = "mode"
sub_corner_topic = "intersection"
sub_obstacle_topic = "obstacle"
sub_qr_topic = "qr"
sub_scenario_topic = "scenario"
sub_direction_topic = "direction"
pub_topic = "mapping"
IDLE_STATE = "IDLE_STATE"
MAPPING_STATE = "MAPPING_STATE"
DUTY_STATE = "DUTY_STATE"
INIT_STATE = "INIT_STATE"

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(dir_path), 'Raspberry', 'Database', 'db_state.txt')
try:
    db_state = open(file_path, "a")
    db_state_r = open(file_path, "r")
except FileNotFoundError:
    raspi_log.log_process("No state found before")
    db_state = open(file_path,"w")


load_points = ["Q33","Q38","Q45","Q50"]
def callback_for_qr(client, userdata, msg):
    message = msg.payload.decode('utf-8')  # dinlenen veriyi anlamlı hale getirmek
    print(message)
    parts = message.split(";")  # QR etiketinin standart halinde pozisyonu ayrıştırmak
    if state == MAPPING_STATE:
        mapping_mode.callback_for_qr(msg)
    if state == DUTY_STATE:
        if parts[0] in load_points:
            duty_mode.Duty.stop_in_point()
            duty_mode.Duty.import_load()

def callback_for_direction(client,userdata,msg):
    global mapping_mode
    if state == MAPPING_STATE:
        message = msg.payload.decode("utf-8")
        mapping_mode.callback_for_direction(message)


def callback_for_corner(client, userdata, msg):
    global mapping_mode
    message = msg.payload.decode('utf-8')
    if state == MAPPING_STATE:
        mapping_mode.callback_for_corner(message)

def callback_for_senario(client,userdata,msg):
    message = msg.payload.decode('utf-8')
    if state == INIT_STATE:
        PathHelper.start_follow_path(message)



def callback_for_obstacle(client, userdata, msg):

    if state == MAPPING_STATE:
        mapping_mode.callback_for_obstacle(msg)
   # if msg == "ENDED_OBSTACLE_FLOW":
        #obstacle_detection.callback_for_end_obstacle()

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(message)
    process_state(message)




def finish_callback():
    global state
    global client
    topic_stat = "stateStatus"
    mqtt_adapter.publish(client,state, topic_stat)
    message = str(f"Mapping is finished. New state is {state}")
    state = INIT_STATE
    raspi_log.log_process(message)
    process_state(state)
    # change state to idle
    # inform gui


def run_explore_mode():
    global state
    global mapping_mode
    mapping_mode = mapping.Mapping(finish_callback)
    # mapping_mode = mapping.Mapping()
    if state == IDLE_STATE:
        state = MAPPING_STATE
        raspi_log.log_process("Mapping state active!")
        save_last_state()



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
    global state, db_state
    db_state.write("\n" + state)


def get_last_state():
    return state


def main():
    global mapping_mode
    global state
    global direction_controller
    global db_state

    state = IDLE_STATE


    raspi_log.log_process(str(f"Lifecycle started! parent id:, {os.getppid()},  self id:, {os.getpid()}"))
    client = mqtt_adapter.connect("lifecycle")
    direction_controller = direction_manager.Direction()
    state = IDLE_STATE
    lines = db_state_r.readlines()
    if len(lines) > 0:
        state = str(lines[len(lines) - 1])
        raspi_log.log_process(state)
    else:
        state = IDLE_STATE  # idle

    # mapping_mode = mapping.Mapping(finish_callback)

    mqtt_adapter.subscribe(client,topic, on_message)
    mqtt_adapter.subscribe(client,sub_scenario_topic, callback_for_senario)
    mqtt_adapter.subscribe(client,sub_direction_topic, callback_for_direction)
    mqtt_adapter.subscribe(client,sub_qr_topic, callback_for_qr)
    mqtt_adapter.subscribe(client,sub_corner_topic, callback_for_corner)
    mqtt_adapter.subscribe(client,sub_obstacle_topic, callback_for_obstacle)
    process_state(state)
    mqtt_adapter.loop_forever(client)

