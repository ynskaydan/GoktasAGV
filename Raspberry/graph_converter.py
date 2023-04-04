import json


def convert_json(graph):
    nodes = []
    qr_list = []
    obstacles = []
    for node_id in graph.nodes:
        node = graph.get_node(node_id)
        list_adjacents = []
        list_unvisited_directions = []

        x = node.get_pos_x()
        y = node.get_pos_y()
        adjacents = node.get_connections()

        unvisited_directions = node.get_unvisited_directions()

        for adjacent in adjacents:
            list_adjacents.append(adjacent.get_id())

        nodes.append(
            {"id": node.get_id(), "pos": {"x": x, "y": y}, "type": node.get_type(), "adjacents": list_adjacents,
             "unvisitedDirections": unvisited_directions})

    for qr_id in graph.qr_list:
        qr = graph.get_qr(qr_id)
        qr_list.append({"id": qr.get_id(), "pos": {"x": qr.get_pos_x(), "y": qr.get_pos_y()}})

    for obstacle_id in graph.obstacles:
        obstacle = graph.get_obstacle(obstacle_id)
        obstacles.append({"id": obstacle.get_id(), "pos": {"x": obstacle.get_posx(), "y": obstacle.get_posy()}})

    graphs = {"nodes": nodes, "qr": qr_list, "obstacles": obstacles}

    converted_json = json.dumps(graphs)
    return converted_json


def read_database(db, graph):
    lines = db.readlines()
    if len(lines) == 0:
        return False
    else:
        json_graph = lines[len(lines) - 1]
        data = json.loads(json_graph)

        nodes = data['nodes']
        qr_codes = data['qr']
        obstacles = data['obstacles']

        for node_data in nodes:
            node_id = node_data['id']
            pos_x = node_data['pos']['x']
            pos_y = node_data['pos']['y']
            node_type = node_data['type']
            adjacents = node_data['adjacents']
            unvisited_directions = node_data['unvisitedDirections']
            node = graph.add_node(node_id, pos_x, pos_y, node_type, unvisited_directions)
            if len(adjacents) > 0:
                for adjacent_id in adjacents:
                    adjacent = graph.get_node(adjacent_id)
                    if adjacent == 0:
                        continue
                    graph.add_edge(node, adjacent)

        for qr_code in qr_codes:
            qr_id = qr_code['id']
            pos_x = qr_code['pos']['x']
            pos_y = qr_code['pos']['y']
            graph.add_qr(qr_id, pos_x, pos_y)

        for obstacle in obstacles:
            obs_id = obstacle['id']
            pos_x = obstacle['pos']['x']
            pos_y = obstacle['pos']['y']
            graph.add_obstacle(obs_id, pos_x, pos_y)
        return True
