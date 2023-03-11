from mqtt import connect_mqtt, sendData

topic = "hearbeat"
client = connect_mqtt()
def send_heartbeat():
    while True:
        send_data(client, "heartbeat", heartbeat_topic)
        time.sleep(5)  # 5 saniye beklemeP
        
    
# Kullanım örneği ekte gösterilmiştir.
#  from heartbeat import send_heartbeat
#  if __name__ == '__main__':
#      send_heartbeat()#
