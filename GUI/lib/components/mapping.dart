import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:universal_mqtt_client/universal_mqtt_client.dart';

import '../entity/graph.dart';

var mappingState = false;

var mappingStateTopic = "mappingState";

class MapWidget extends StatefulWidget {
  MapWidget({super.key, required this.nodes});
  List<Node> nodes;
  final client = UniversalMqttClient(
    broker: Uri.parse('ws://localhost:8080'),
    autoReconnect: true,
  );

  void mapping() async {
    await client.connect();
    final subscription =
        client.handleString('mapping', MqttQos.atLeastOnce).listen((message) {
      Graph graph = Graph.fromJson(jsonDecode(message));
      nodes = graph.nodes;
      //List<QR> qrs = graph.qr;
    });
  }

  _MapWidgetState createState() => _MapWidgetState();
}

class _MapWidgetState extends State<MapWidget> {}

class MapPainter extends CustomPainter {
  final List<Node> nodes;

  const MapPainter(this.nodes);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    final radius = 10.0;

    // Draw the nodes
    for (final node in nodes) {
      final type = node.type;
      final pos = node.pos;
      final x = pos['x'] as double;
      final y = pos['y'] as double;

      if (type == 'Start') {
        canvas.drawCircle(Offset(x, y), radius, paint);
      } else if (type == 'LEFT_L') {
        final lineStart = Offset(x - radius, y);
        final lineEnd = Offset(x, y + radius);
        canvas.drawLine(lineStart, lineEnd, paint);
      } else if (type == 'RIGHT_L') {
        final lineStart = Offset(x + radius, y);
        final lineEnd = Offset(x, y + radius);
        canvas.drawLine(lineStart, lineEnd, paint);
      }
    }

    // Draw the connections between the nodes
    for (final node in nodes) {
      final pos = node.pos;
      final x = pos['x'] as double;
      final y = pos['y'] as double;
      final adjacents = node.adjacents;
      for (final adj in adjacents) {
        final adjacentNode = nodes.firstWhere((n) => n.id == adj);
        final adjacentPos = adjacentNode.pos;
        final adjX = adjacentPos['x'] as double;
        final adjY = adjacentPos['y'] as double;

        canvas.drawLine(Offset(x, y), Offset(adjX, adjY), paint);
      }
    }

    // Draw an arrow for the start node
    final startNode = nodes.firstWhere((n) => n.type == 'Start');
    if (startNode != null) {
      final startPos = startNode.pos;
      final start = Offset(startPos['x'] as double, startPos['y'] as double);
      final arrowLength = 20.0;

      canvas.drawLine(start, Offset(start.dx + arrowLength, start.dy), paint);

      final arrowTip = Offset(start.dx + arrowLength - 10, start.dy - 10);
      final arrowBase = Offset(start.dx + arrowLength - 10, start.dy + 10);
      canvas.drawLine(arrowTip, start, paint);
      canvas.drawLine(arrowBase, start, paint);
    }
  }

  @override
  bool shouldRepaint(MapPainter oldDelegate) => false;
}
