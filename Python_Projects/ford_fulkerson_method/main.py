from graphs import *

def main():
    # wczytywanie grafu
    def load_graph(graph: list) -> ListGraph:
        G = ListGraph()
        for v1, v2, cap in graph:
            G.insertVertex(Vertex(key=v1))
            G.insertVertex(Vertex(key=v2))
            G.insertEdge(v1, v2, Edge(capacity=cap))
            G.insertEdge(v2, v1, Edge(capacity=0, is_residual=True))
        return G


    def BFS(G: ListGraph, s: int):
        queue = [s]
        visited = [None for _ in range(G.order())]
        visited_kolejnosc = []
        parents = [None for _ in range(G.order())]
        while queue: # not empty list is true
            s = queue.pop(0)
            # if visited[s] is None:  # s not in visited
            visited[s] = 1
            visited_kolejnosc.append(s)
            neighbors_list = G.neighbours(s)
            for u, edge in neighbors_list:
                if (visited[u] is None) and (edge.residual > 0):
                    queue.append(u)
                    visited[u] = 1
                    parents[u] = s
        return visited_kolejnosc, parents


    def minimal_capacity(G: ListGraph, v_init: int, v_end: int, parent: list) -> Union[int, float]:
        temp_idx = v_end
        min_cap = float("inf")
        if parent[v_end] is None:
            return 0
        while temp_idx != v_init:
            temp_parent = parent[temp_idx]
            neighbors = G.neighbours(temp_parent)
            for v0, edge in neighbors:
                if (temp_idx == v0) and (not edge.is_residual):
                    if edge.residual < min_cap:
                        min_cap = edge.residual
            temp_idx = temp_parent
        return min_cap


    def path_augmentating(G: ListGraph, v_init: int, v_end: int, parent: list, min_cap: Union[int, float]) -> None:
        temp_idx = v_end
        if parent[v_end] is None:
            return
        while temp_idx != v_init:
            temp_parent = parent[temp_idx]
            parents_neighbors = G.neighbours(temp_parent)  # krawędzie od rodzica
            v_neighbors = G.neighbours(temp_idx)  # krawędzie od wierzchołka
            for v0, edge in parents_neighbors:
                if (temp_idx == v0) and (not edge.is_residual):
                    edge.flow += min_cap
                    edge.residual -= min_cap
            for v0, edge in v_neighbors:
                if (temp_parent == v0) and (edge.is_residual):
                    edge.residual += min_cap
            temp_idx = temp_parent


    def ford_fulkerson(G: ListGraph):
        v_init = G.dict[G.list[0]]
        for i, vertex in enumerate(G.list):
            if vertex.key == "t":
                v_end = i

        visited, parent = BFS(G, v_init)
        if v_end in visited:
            min_cap = minimal_capacity(G, v_init, v_end, parent)
            flow_sum = min_cap
            while min_cap > 0:
                path_augmentating(G, v_init, v_end, parent, min_cap)
                visited, parent = BFS(G, v_init)
                min_cap = minimal_capacity(G, v_init, v_end, parent)
                flow_sum += min_cap
            return flow_sum
        return None


    graf_0 = [ ('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)]
    graf_1 = [ ('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4) ]
    graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9), ('d', 'a', 1), ]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]

    G0 = load_graph(graf_0)
    # printGraph(G0)
    G1 = load_graph(graf_1)
    # printGraph(G1)
    G2 = load_graph(graf_2)
    # printGraph(G2)
    G3 = load_graph(graf_3)
    # printGraph(G3)

    print(ford_fulkerson(G0))
    G0.print_repr()

    print(ford_fulkerson(G1))
    G0.print_repr()

    print(ford_fulkerson(G2))
    G0.print_repr()

    print(ford_fulkerson(G3))
    G0.print_repr()


main()

