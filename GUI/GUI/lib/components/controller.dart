import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_neumorphic/flutter_neumorphic.dart';
import 'package:goktasgui/components/controller.dart';
import 'package:universal_mqtt_client/universal_mqtt_client.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:goktasgui/components/constants.dart';

class Controller extends StatefulWidget {
  const Controller({super.key});

  @override
  State<Controller> createState() => _ControllerState();
}


class _ControllerState extends State<Controller> {
  final client = UniversalMqttClient(
    //broker: Uri.parse('ws://192.168.1.101:8080'),
    broker: Uri.parse('ws://192.168.1.101:8080'),
    /*  password: "123456",
    username: "goktas", */
    autoReconnect: true,
  );

  @override
  void initState() {
    connection();
    super.initState();
  }

  void connection() async {
    client.status.listen((status) {
      // ignore: avoid_print
      print('Connection Status: $status');
    });
    await client.connect();
  }

  Color _buttonColor = Colors.red;
  bool _isButtonOn = false;
  int a = 0;
  int b = 0;
  String pubTopic = "move";
  String modeTopic = "move";
  String text = "No Sended Message";

  void _moveForward() {
    if (_isButtonOn) {
      setState(() {
        y++;
        client.publishString(pubTopic, 'w', MqttQos.atLeastOnce);
      });
    }
  }

  void _moveBackward() {
    if (_isButtonOn) {
      setState(() {
        y--;
        client.publishString(pubTopic, 's', MqttQos.atLeastOnce);
      });
    }
  }

  void _moveRight() {
    if (_isButtonOn) {
      setState(() {
        x++;
        client.publishString(pubTopic, 'd', MqttQos.atLeastOnce);
      });
    }
  }

  void _moveLeft() {
    if (_isButtonOn) {
      setState(() {
        x--;
      });
      client.publishString(pubTopic, 'a', MqttQos.atLeastOnce);
    }
  }

  void _stopEngine() {
    setState(() {
      client.publishString(pubTopic, 'e', MqttQos.atLeastOnce);
    });
  }

  void _forwardLinearActuator() {
    setState(() {
      client.publishString(pubTopic, 't', MqttQos.atLeastOnce);
    });
  }

  void _backwardLinearActuator() {
    setState(() {
      client.publishString(pubTopic, 'u', MqttQos.atLeastOnce);
    });
  }

  void _stopLinearActuator() {
    setState(() {
      client.publishString(pubTopic, 'y', MqttQos.atLeastOnce);
    });
  }

  void _manuelControl() {
    setState(() {
      client.publishString(modeTopic, 'manual', MqttQos.atLeastOnce);
      print("manuel mesajı gönderiliri");
    });
  }

  void _autonomousControl() {
    setState(() {
      client.publishString(modeTopic, 'autonomous', MqttQos.atLeastOnce);
      print("otonom mesajı gönderildi");
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
                : Colors.black12,
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
                : Colors.black12,
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
    return SizedBox(
      width: MediaQuery.of(context).size.width / 24,
      child: ElevatedButton(
        onPressed: () {
          setState(() {
            _isButtonOn = !_isButtonOn;
            _buttonColor = _isButtonOn ? Colors.green : Colors.red;

            if (_isButtonOn) {
              _manuelControl();
            } else {
              _autonomousControl();
            }
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
            const SizedBox(height: 5),
            Text(
              _isButtonOn ? 'ON' : 'OFF',
              textAlign: TextAlign.center,
              style: const TextStyle(
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
                direction: 4,
                icon: const Icon(Icons.arrow_circle_up_sharp, size: 40)),
            const SizedBox(width: 15),
            linearActuator(
                direction: 5,
                icon: const Icon(Icons.arrow_circle_down_sharp, size: 40)),
            const SizedBox(width: 15),
            linearActuator(
                direction: 6,
                icon: const Icon(Icons.stop_circle_sharp, size: 40)),
          ],
        ),
      ],
    );
  }
}
