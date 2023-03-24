class Node {
  final String id;
  final Map<String, double> pos;
  final String type;
  final List<dynamic> adjacents;
  final List<dynamic> unvisitedDirections;

  Node(
      {required this.id,
      required this.pos,
      required this.type,
      required this.adjacents,
      required this.unvisitedDirections});

  factory Node.fromJson(Map<String, dynamic> json) {
    return Node(
      id: json['id'] as String,
      pos: Map<String, double>.from(json['pos'] as Map<String, dynamic>)
          .map((key, value) => MapEntry(key, value as double)),
      type: json['type'] as String,
      adjacents: json['adjacents'] as List<dynamic>,
      unvisitedDirections: json['unvisitedDirections'] as List<dynamic>,
    );
  }
}

class QR {
  final String id;
  final Map<String, double> pos;

  QR({required this.id, required this.pos});

  factory QR.fromJson(Map<String, dynamic> json) {
    return QR(
      id: json['id'] as String,
      pos: Map<String, double>.from(json['pos'] as Map<String, dynamic>)
          .map((key, value) => MapEntry(key, value as double)),
    );
  }
}

class Graph {
  final List<Node> nodes;
  final List<QR> qr;

  Graph({
    required this.nodes,
    required this.qr,
  });

  factory Graph.fromJson(Map<String, dynamic> json) {
    return Graph(
      nodes: List<Node>.from(json['nodes'].map((x) => Node.fromJson(x))),
      qr: List<QR>.from(json['qr'].map((x) => QR.fromJson(x))),
    );
  }
}

  Graph({
    required this.nodes,
    required this.qr,
  });

  factory Graph.fromJson(Map<String, dynamic> json) {
    return Graph(
      nodes: List<Node>.from(json['nodes'].map((x) => Node.fromJson(x))),
      qr: List<QR>.from(json['qr'].map((x) => QR.fromJson(x))),
    );
  }
}
