import mapping
from CrossCuttingConcerns.mqtt import connect_mqtt, broker
from CrossCuttingConcerns.sub_mqtt import mqtt_sub

power = ""
sub_mode_topic = "mode"
client = connect_mqtt()
sub_topics = [sub_mode_topic]
mode = ""


def callback_for_mode(client, userdata, msg):
    global mode
    message = msg.payload.decode('utf-8')
    modes = {
        "explore": {run_explore_mode()},
        "import": {run_import_mode()},
        "export": {run_export_mode()}
    }
    if message in modes:
        mode = message
        modes[mode]


def run_explore_mode():
    global mode
    try:
        mapping.main()
    except:
        print("mapping is stopped")


def run_import_mode():
    global mode
    while mode == "import":
        print("Load is importig..")


def run_export_mode():
    global mode
    while mode == "export":
        print("Load is exporting..")


on_message_methods = [callback_for_mode]
mqtt_sub(broker, sub_topics, on_message_methods)
