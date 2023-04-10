import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';

import 'package:goktasgui/components/controller.dart';
import 'package:universal_mqtt_client/universal_mqtt_client.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:goktasgui/components/constants.dart';
import 'package:goktasgui/components/constants.dart';

class Controller extends StatefulWidget {
  const Controller({super.key});

  @override
  State<Controller> createState() => _ControllerState();
}

//192.168.1.101:8080
class _ControllerState extends State<Controller> {
  final client = UniversalMqttClient(
    broker: Uri.parse('ws://localhost:8080'),
    autoReconnect: true,
  );
  void initState() {
    connection();
    //setupUpdatesListener();
    super.initState();
  }

  void connection() async {
    print("connection");
    client.status.listen((status) {
      print('Connection Status: $status');
    });

    await client.connect();

    //await subscription.cancel();

    //client.disconnect();
  }

  Color _buttonColor = Colors.red;
  bool _isButtonOn = false;

  int a = 0;
  int b = 0;
  String pubTopic = "move";
  String text = "No Sended Message";

  void _moveForward() {
    if (_isButtonOn) {
      setState(() {
        y++;
        client.publishString(pubTopic, 'w', MqttQos.atLeastOnce);
        print('pos(x,y): (${x.toString()},${y.toString()}) | MOVE FORWARD');
      });
    }
  }

  void _moveBackward() {
    if (_isButtonOn) {
      setState(() {
        y--;
        client.publishString(pubTopic, 's', MqttQos.atLeastOnce);
        print('pos(x,y): (${x.toString()},${y.toString()}) | MOVE BACKWARD');
      });
    }
  }

  void _moveRight() {
    if (_isButtonOn) {
      setState(() {
        x++;
        client.publishString(pubTopic, 'd', MqttQos.atLeastOnce);
        print('pos(x,y): (${x.toString()},${y.toString()}) | MOVE RIGHT');
      });
    }
  }

  void _moveLeft() {
    if (_isButtonOn) {
      setState(() {
        x--;
        print('pos(x,y): (${x.toString()},${y.toString()}) | MOVE LEFT');
      });
      client.publishString(pubTopic, 'a', MqttQos.atLeastOnce);
    }
  }

  void _stopEngine() {
    setState(() {
      client.publishString(pubTopic, 'e', MqttQos.atLeastOnce);
      print('pos(x,y): (${x.toString()},${y.toString()}) | ENGINE STOPPED');
    });
  }

  void _forwardLinearActuator() {
    setState(() {
      client.publishString(pubTopic, 't', MqttQos.atLeastOnce);
      print('LINEAR ACTUATOR FORWARD');
    });
  }

  void _backwardLinearActuator() {
    setState(() {
      client.publishString(pubTopic, 'u', MqttQos.atLeastOnce);
      print('LINEAR ACTUATOR BACKWARD');
    });
  }

  void _stopLinearActuator() {
    setState(() {
      client.publishString(pubTopic, 'y', MqttQos.atLeastOnce);
      print('LINEAR ACTUATOR STOPPED');
    });
  }

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
        case 911:
          _stopEngine();
          break;
        case 4:
          _forwardLinearActuator();
          break;
        case 5:
          _backwardLinearActuator();
          break;
        case 6:
          _stopLinearActuator();
          break;
      }
    });
  }

  Widget directions({
    required int direction,
    required String imagePath,
  }) {
    bool isPressed = isPressedMap[direction] ?? false;
    return Container(
      height: 50,
      width: 50,
      decoration: BoxDecoration(
        color: isPressed
            ? Colors.grey
            : _isButtonOn
                ? Constant.directionGrey
                : Colors.black12, // arka plan rengi değiştirildi
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(
            color: isPressed
                ? Colors.white
                : _isButtonOn
                    ? Constant.boxShadowLeft
                    : Colors.transparent,
            offset: isPressed ? Offset(3, 3) : Offset(-3, -3),
            blurRadius: 8,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Center(
          child: GestureDetector(
        onTapDown: (details) {
          setState(() {
            if (_isButtonOn) {
              isPressedMap[direction] = true;
              _sender(direction);
            }
          });
        },
        onTapUp: (details) {
          setState(() {
            if (_isButtonOn) {
              isPressedMap[direction] = false;
              _sender(911);
            }
          });
        },
        onTapCancel: () {
          setState(() {
            if (_isButtonOn) {
              isPressedMap[direction] = false;
              _sender(911);
            }
          });
        },
        child: Image.asset(imagePath, fit: BoxFit.cover),
      )),
    );
  }

  Widget linearActuator({
    required int direction,
    required Icon icon,
  }) {
    bool isPressed = isPressedMap[direction] ?? false;
    return Container(
      height: 50,
      width: 50,
      decoration: BoxDecoration(
        color: isPressed
            ? Colors.grey
            : _isButtonOn
                ? Constant.directionGrey
                : Colors.black12, // arka plan rengi değiştirildi
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(
            color: isPressed
                ? Colors.white
                : _isButtonOn
                    ? Constant.boxShadowLeft
                    : Colors.transparent,
            offset: isPressed ? Offset(3, 3) : Offset(-3, -3),
            blurRadius: 8,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Center(
          child: GestureDetector(
        onTapDown: (details) {
          setState(() {
            if (_isButtonOn) {
              isPressedMap[direction] = true;
              _sender(direction);
            }
          });
        },
        onTapUp: (details) {
          setState(() {
            if (_isButtonOn) {
              isPressedMap[direction] = false;
              _sender(6);
            }
          });
        },
        onTapCancel: () {
          setState(() {
            if (_isButtonOn) {
              isPressedMap[direction] = false;
              _sender(6);
            }
          });
        },
        child: icon,
      )),
    );
  }

  Widget controllerButton() {
    return Container(
      width: MediaQuery.of(context).size.width / 24,
      child: ElevatedButton(
        onPressed: () {
          setState(() {
            _isButtonOn = !_isButtonOn;
            _buttonColor = _isButtonOn ? Colors.green : Colors.red;
            print("Manuel Kontrol Durumu: $_isButtonOn");
          });
        },
        style: ElevatedButton.styleFrom(
          primary: _buttonColor, // Düğmenin arkaplan rengi
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Center(
              child: Icon(
                _isButtonOn
                    ? Icons.power_settings_new
                    : Icons.power_off_rounded,
                size: 30,
                color: Colors.white,
              ),
            ),
            SizedBox(height: 5),
            Text(
              _isButtonOn ? 'ON' : 'OFF',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            controllerButton(),
            const SizedBox(
              width: 15,
            ),
            directions(
              direction: 0,
              imagePath: _isButtonOn
                  ? "assets/images/forward.png"
                  : "assets/images/forward_disable.png",
            ),
            const SizedBox(
              width: 15,
            ),
            directions(
              direction: 1,
              imagePath: _isButtonOn
                  ? "assets/images/back.png"
                  : "assets/images/back_disable.png",
            ),
            const SizedBox(
              width: 15,
            ),
            directions(
              direction: 2,
              imagePath: _isButtonOn
                  ? "assets/images/left.png"
                  : "assets/images/left_disable.png",
            ),
            const SizedBox(
              width: 15,
            ),
            directions(
              direction: 3,
              imagePath: _isButtonOn
                  ? "assets/images/right.png"
                  : "assets/images/right_disable.png",
            ),
            const SizedBox(width: 15),
            linearActuator(
                direction: 4, icon: Icon(Icons.arrow_circle_up_sharp)),
            const SizedBox(width: 15),
            linearActuator(
                direction: 5, icon: Icon(Icons.arrow_circle_down_sharp)),
            const SizedBox(width: 15),
            linearActuator(direction: 6, icon: Icon(Icons.stop_circle_sharp)),
          ],
        ),
      ],
    );
  }
}
