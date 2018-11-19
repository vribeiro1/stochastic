import numpy as np


class Graph:
    def __init__(self, nodes):
        self.graph = {
            node: [] for node in nodes
        }

    def connect(self, *node_pairs, undirected=True):
        for node_1, node_2, weight in node_pairs:
            self.graph[node_1].append((node_2, weight))
            if undirected:
                self.graph[node_2].append((node_1, weight))

    def dijkstra_search(self, origin, dest):
        unvisited = [node for node in self.graph]
        shortest_path_table = {node: (0 if node == origin else np.inf, None)
                               for node in self.graph}

        while unvisited:
            unvisited_table = [item for item in shortest_path_table.items() if item[0] in unvisited]
            current_node, (distance_from_origin, previous_node) = min(unvisited_table,
                                                                      key=lambda node: node[1][0])
            unvisited.remove(current_node)

            neighbouring_nodes = self.graph[current_node]
            for neighbour, weight in neighbouring_nodes:
                neighbour_distance_from_origin = distance_from_origin + weight

                if neighbour_distance_from_origin < shortest_path_table[neighbour][0]:
                    shortest_path_table[neighbour] = neighbour_distance_from_origin, current_node

        reversed_path = []
        previous = dest
        while previous:
            reversed_path.append(previous)
            previous = shortest_path_table[previous][1]

        path = list(reversed(reversed_path))
        return path
