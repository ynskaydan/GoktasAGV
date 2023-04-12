import 'dart:convert';
import 'dart:html';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:goktasgui/components/controller.dart';
import 'package:goktasgui/components/mapping.dart';
import 'package:universal_mqtt_client/universal_mqtt_client.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:goktasgui/components/constants.dart';

var mappingState = true;

class EntrySenario extends StatefulWidget {
  const EntrySenario({super.key});

  @override
  State<EntrySenario> createState() => _EntrySenarioState();
}

class _EntrySenarioState extends State<EntrySenario> {
  final client = UniversalMqttClient(
    broker: Uri.parse('ws://localhost:8080'),
    autoReconnect: true,
  );
  @override
  void initState() {
    connectionSenario();
    super.initState();
  }

  String pubTopic = "scenario";
  String subTopic = "subScenario";
  void connectionSenario() async {
    //print("connection");
    //client.status.listen((status) {
    //  print('Connection Status: $status');
    //});
    await client.connect();

    final subscription =
        client.handleString(subTopic, MqttQos.atLeastOnce).listen((message) {
      print("map durumu -> " + mappingState.toString());
      print(message);
      // obstacles = graph.obstacles;
    });
  }

  void _sendSenario() {
    setState(() {
      client.publishString(
          pubTopic, 'SENARYO: $_enteredText', MqttQos.atLeastOnce);
      print('SENARYO: $_enteredText');
    });
  }

  String _enteredText = "";
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: SizedBox(
            width: 200,
            height: 50,
            child: TextField(
              onChanged: (text) {
                setState(() {
                  _enteredText = text;
                });
              },
              decoration: InputDecoration(
                hintText: 'Bir metin girin',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
        ),
        SizedBox(width: 10),
        ElevatedButton(
          onPressed: mappingState ? _sendSenario : null,
          child: SizedBox(
              height: 50,
              child: Center(
                child: Text(
                  "Gönder",
                  style: const TextStyle(fontSize: 20, color: Colors.white),
                  textAlign: TextAlign.center,
                ),
              )),
        ),
      ],
    );
  }
}

class MainButtons extends StatefulWidget {
  const MainButtons({super.key});

  @override
  State<MainButtons> createState() => _MainButtonsState();
}

class _MainButtonsState extends State<MainButtons> {
  final client = UniversalMqttClient(
    broker: Uri.parse('ws://localhost:8080'),
    autoReconnect: true,
  );

  @override
  void initState() {
    client.connect();
    super.initState();
  }

  void _startTheMapping() {
    setState(() {
      mappingState == true;
      client.publishString(
          mappingStateTopic, 'start the mapping', MqttQos.atLeastOnce);
    });
  }

  void _stopTheMapping() {
    setState(() {
      mappingState == false;
      client.publishString(
          mappingStateTopic, 'stop the mapping', MqttQos.atLeastOnce);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(10),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: Color.fromRGBO(40, 40, 40, 1.0),
        ),
        height: MediaQuery.of(context).size.height / 12,
        width: MediaQuery.of(context).size.width / 1.2 - 20,
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                    onPressed: () {
                      _startTheMapping();
                    },
                    child: Text("Kalibrasyon")),
                SizedBox(
                  width: 20,
                ),
                /* ElevatedButton(
                    onPressed: () {
                      _startTheMapping();
                    },
                    child: Text("Buton")), */
                SizedBox(
                  width: 20,
                ),
                ElevatedButton(
                    onPressed: () {
                      _startTheMapping();
                    },
                    child: Text("Başla!")),
                SizedBox(
                  width: 20,
                ),
                /*   ElevatedButton(
                    onPressed: () {
                      _stopTheMapping();
                    },
                    child: Text("Bitir!")), */
              ],
            ),
          ),
        ),
      ),
    );
  }
}
