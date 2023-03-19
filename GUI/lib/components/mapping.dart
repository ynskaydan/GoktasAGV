import 'dart:convert';
import 'dart:html';
import 'dart:io';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:goktasgui/components/controller.dart';
import 'package:universal_mqtt_client/universal_mqtt_client.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:goktasgui/components/constants.dart';

var mappingStateTopic = "mappingState";
bool mappingState = true;
var nodeId;
var nodeType;

class MyCustomPainter extends CustomPainter {
  final List<Offset> points;
  final List<String> id;

  MyCustomPainter(this.points, this.id);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black
      ..strokeWidth = 2;

    final paint2 = Paint()..color = Colors.red;
    final paint3 = Paint()..color = Colors.blue;
    final paint4 = Paint()..color = Colors.green;

    for (var i = 0; i < points.length - 1; i++) {
      canvas.drawLine(points[i], points[i + 1], paint);
    }
    for (var i = 0; i < points.length; i++) {
      var point = points[i];
      var idString = id[i];
      //canvas.drawCircle(point, 5, paint2);
      switch (idString) {
        case "S":
          canvas.drawRect(Rect.fromCenter(center: point, width: 15, height: 15),
              Paint()..color = Colors.black);
          break;
        case "Q3":
          canvas.drawRect(Rect.fromCenter(center: point, width: 15, height: 15),
              Paint()..color = Colors.red);
          break;
        case "Q4":
          canvas.drawRect(Rect.fromCenter(center: point, width: 15, height: 15),
              Paint()..color = Colors.blue);
          break;
        case "Q5":
          canvas.drawRect(Rect.fromCenter(center: point, width: 15, height: 15),
              Paint()..color = Colors.green);
          break;
        default:
          canvas.drawRect(Rect.fromCenter(center: point, width: 15, height: 15),
              Paint()..color = Colors.amber);
          break;
      }
    }
  }

  @override
  bool shouldRepaint(MyCustomPainter oldDelegate) =>
      oldDelegate.points != points;
}

class MappingWidget extends StatefulWidget {
  final List<Offset> points;

  const MappingWidget({super.key, required this.points});

  @override
  State<MappingWidget> createState() => _MappingWidgetState();
}

class _MappingWidgetState extends State<MappingWidget> {
  final client = UniversalMqttClient(
    broker: Uri.parse('ws://localhost:8080'),
    autoReconnect: true,
  );
  List<Offset> points = [];
  List<String> idList = [];
  List<String> typeList = [];
  @override
  void initState() {
    mapping();
    super.initState();
  }

  void mapping() async {
    await client.connect();
    final subscription =
        client.handleString('mapping', MqttQos.atLeastOnce).listen((message) {
      List<double> xList = []; // x pozisyonları
      List<double> yList = []; // y pozisyonları
      List<String> idList = []; // id listesi

      Map<String, dynamic> jsonMap = jsonDecode(message);
      List<dynamic> nodes =
          jsonMap['nodes']; //Json içindeki nodes array parse edilmesi
      for (var node in nodes) {
        nodeId = node['id'];
        //nodeType = node['type'];
        //typeList.add(nodeType);
        idList.add(nodeId);
        Map<String, dynamic> pos = node['pos'] ;
        double x = pos['x'] as double;
        double y = pos['y'] as double;
        xList.add(x);
        yList.add(y);
        print(x);
        print(y);
      }

      setState(() {
        points.clear();
        for (int i = 0; i < xList.length; i++) {
          points.add(Offset(xList[i], yList[i]));
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      child: Column(
        children: [
          CustomPaint(
            painter: MyCustomPainter(points, idList),
          ),
        ],
      ),
    );
  }
}
