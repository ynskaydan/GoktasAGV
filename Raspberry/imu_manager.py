from CrossCuttingConcerns import mqtt_adapter

direction = ""
sub_topic = "imu"  # imu manager hem speed hem direction
speed = ""


def main():
    mqtt_adapter.connect()
    mqtt_adapter.subscribe(sub_topic, callback)


def callback(client, userdata, msg):
    global direction, speed
    message = msg.payload.decode('utf-8')
    parts = message.split(";")
    direction = parts[0]
    speed = parts[1]


def get_direction():
    return direction


def get_speed():
    return speed
