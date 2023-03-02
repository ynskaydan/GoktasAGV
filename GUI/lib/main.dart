import 'package:flutter/material.dart';
import 'package:goktasgui/MqttClientManager.dart';

import 'package:mqtt_client/mqtt_client.dart';


void main() {
  runApp(const MyApp());
}


class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Goktas AGV Control Panel',
      theme: ThemeData(
        backgroundColor: Colors.blueGrey,
        primarySwatch: Colors.lime,
      ),
      home: MyHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  
 MQTTClientManager mqttClientManager = MQTTClientManager();
 
  @override
  void initState() {
    setupMqttClient();
    //setupUpdatesListener();
    super.initState();
  }

   void _moveForward() {
    setState(() {
      x++;
      mqttClientManager.publishMessage(
          pubTopic, "posy: ${y.toString()} move forward");
    });
  }
    void _moveBackward() {
    setState(() {
      y--;
      mqttClientManager.publishMessage(
          pubTopic, "posy: ${y.toString()} move backward");
    });
  }
    void _moveRight() {
    setState(() {
      x++;
      mqttClientManager.publishMessage(
          pubTopic, "posx: ${x.toString()} move right");
    });
  }
    void _moveLeft() {
    setState(() {
      x--;
      mqttClientManager.publishMessage(
          pubTopic, "posx: ${x.toString()} move left");
    });
  }
  final String pubTopic = "yunus";
  int x = 0;
  int y = 0;
  String text = "No Sended Message";


  void _sender(int index) {
    setState(() {
      switch (index) {
        case 0:
          _moveForward();
          break;
        case 1:
          _moveBackward();
          break;
        case 2:
          _moveLeft();
          break;
        case 3:
          _moveRight();
          break;
      }
    });
  }
    Future<void> setupMqttClient() async {
    await mqttClientManager.connect();
    //mqttClientManager.subscribe(pubTopic);
  }
/*
  void setupUpdatesListener() {
    mqttClientManager
        .getMessagesStream()!
        .listen((List<MqttReceivedMessage<MqttMessage?>>? c) {
      final recMess = c![0].payload as MqttPublishMessage;
      final pt =
          MqttPublishPayload.bytesToStringAsString(recMess.payload.message);
      print('MQTTClient::Message received on topic: <${c[0].topic}> is $pt\n');
    });
  }*/

  @override
  void dispose() {
    mqttClientManager.disconnect();
    super.dispose();
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              "GOKTAS AGV CONTROL PANEL",
              style: TextStyle(color: Colors.lime, fontSize: 50),
              textAlign: TextAlign.center,
            ),
            const SizedBox(
              height: 20,
            ),
            Container(
              width: MediaQuery.of(context).size.width,
              alignment: Alignment.center,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Container(
                    decoration: BoxDecoration(
                        border: Border.all(),
                        borderRadius: BorderRadius.circular(5)),
                    child: IconButton(
                      onPressed: () => {_sender(0)},
                      icon: const Icon(Icons.arrow_upward),
                    ),
                  ),
                  const SizedBox(
                    width: 15,
                  ),
                  Container(
                    decoration: BoxDecoration(
                        border: Border.all(),
                        borderRadius: BorderRadius.circular(5)),
                    child: IconButton(
                      onPressed: () => {_sender(1)},
                      icon: const Icon(Icons.arrow_downward),
                    ),
                  ),
                  const SizedBox(
                    width: 15,
                  ),
                  Container(
                    decoration: BoxDecoration(
                        border: Border.all(),
                        borderRadius: BorderRadius.circular(5)),
                    child: IconButton(
                      onPressed: () => {_sender(2)},
                      icon: const Icon(Icons.arrow_back),
                    ),
                  ),
                  const SizedBox(
                    width: 15,
                  ),
                  Container(
                    decoration: BoxDecoration(
                        border: Border.all(),
                        borderRadius: BorderRadius.circular(5)),
                    child: IconButton(
                      onPressed: () => {_sender(3)},
                      icon: const Icon(Icons.arrow_forward),
                    ),
                  ),
                ],
              ),
            ),
            Container(
              alignment: Alignment.center,
              child: Text("Position: $x,$y",
                  style: const TextStyle(color: Colors.blue, fontSize: 45)),
            ),
    
        
          ],
        ),
      ),
    );
  }
}

