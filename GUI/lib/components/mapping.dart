import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:universal_mqtt_client/universal_mqtt_client.dart';
import 'dart:ui' as ui;

import '../entity/graph.dart';

var mappingStateTopic = "mappingState";
List<Node> nodes = [];
List<QR> qrs = [];
//List<Obstacles> obstacles = [];

class Mapper extends StatefulWidget {
  Mapper({super.key});

  @override
  State<Mapper> createState() => _MapperState();
}

class _MapperState extends State<Mapper> {
  final client = UniversalMqttClient(
    broker: Uri.parse('ws://localhost:8080'),
    autoReconnect: true,
  );

  @override
  void initState() {
    mapping();
    super.initState();
  }

  void mapping() async {
    await client.connect();
    final subscription =
        client.handleString('mapping', MqttQos.atLeastOnce).listen((message) {
      Graph graph = Graph.fromJson(jsonDecode(message));
      nodes = graph.nodes;
      qrs = graph.qr;
      // obstacles = graph.obstacles;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration:
          BoxDecoration(color: Colors.white24, border: Border.all(width: 10)),
      child: SizedBox(
        width: MediaQuery.of(context).size.width / 2,
        height: MediaQuery.of(context).size.height / 2.5 + 40,
        child: CustomPaint(
          size: Size(MediaQuery.of(context).size.width / 3,
              MediaQuery.of(context).size.height / 2.5 + 40),
          painter: MapPainter(
              nodes,
              qrs,
              //obstacles,
              MediaQuery.of(context).size.width / 2,
              MediaQuery.of(context).size.height / 2.5 + 40),
        ),
      ),
    );
  }
}

class MapPainter extends CustomPainter {
  final List<Node> nodes;
  final List<QR> qrs;
  //final List<Obstacles> obstacles;
  final double scaleX;
  final double scaleY;

  const MapPainter(
      this.nodes, this.qrs, /* this.obstacles,*/ this.scaleX, this.scaleY);

  @override
  Future<void> paint(Canvas canvas, Size size) async {
    if (nodes.isEmpty || qrs.isEmpty) return;
    double coefficient = 0;
    coefficient = scaleX / 1600;
    final paint = Paint()
      ..color = Colors.black
      ..strokeWidth = 2
      ..style = PaintingStyle.fill;
    final linePaint = Paint()
      ..color = Colors.yellow
      ..strokeWidth = 2
      ..style = PaintingStyle.fill;

    final qrPaint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    final obstaclePaint = Paint()
      ..color = Colors.red
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke;

    final radius = 10.0;

    // Draw the nodes
    for (final node in nodes) {
      final type = node.type;
      final pos = node.pos;
      final x = pos['x'] as double;
      final y = pos['y'] as double;
      double a = scaleX - (coefficient * x);
      double b = scaleY - (coefficient * y);
      canvas.drawCircle(Offset(a, b), radius, paint);
    }

    for (final qr in qrs) {
      final pos = qr.pos;
      final x = pos['x'] as double;
      final y = pos['y'] as double;
      double a = scaleX - (coefficient * x);
      double b = scaleY - (coefficient * y);
      canvas.drawCircle(Offset(a, b), radius, qrPaint);
    }
    // for (final obs in obstacles) {
    //   final pos = obs.pos;
    //   final x = pos["x"] as double;
    //   final y = pos["y"] as double;
    //   double a = scaleX - (coefficient * x);
    //   double b = scaleY - (coefficient * y);
    //   Rect rect = Rect.fromLTWH(a, b, 3, 12);
    //   canvas.drawRect(rect, obstaclePaint);
    // }
    // Draw the connections between the nodes
    for (final node in nodes) {
      final pos = node.pos;
      final x = pos['x'] as double;
      final y = pos['y'] as double;
      double a = scaleX - (coefficient * x);
      double b = scaleY - (coefficient * y);
      final adjacents = node.adjacents;
      for (final adj in adjacents) {
        final adjacentNode = nodes.firstWhere((n) => n.id == adj);
        final adjacentPos = adjacentNode.pos;
        final adjX = adjacentPos['x'] as double;
        final adjY = adjacentPos['y'] as double;
        double aAdj = scaleX - (coefficient * adjX);
        double bAdj = scaleY - (coefficient * adjY);

        canvas.drawLine(Offset(a, b), Offset(aAdj, bAdj), linePaint);
      }
    }
  }

  @override
  bool shouldRepaint(MapPainter oldDelegate) => false;
}
