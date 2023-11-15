from collections import deque
from typing import Union
import numpy as np


class Vertex:
    def __init__(self, x=None, y=None, key=None):
        self.x = x
        self.y = y
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.key})"


class Edge:
    def __init__(self, capacity, is_residual=False):
        self.weight = capacity # pojemność
        self.flow = 0 # przepływ
        self.residual = capacity # przepływ resztowy
        self.is_residual = is_residual

    def __eq__(self, other):
        return self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __str__(self):
        return f"Cap: {self.weight} Flow: {self.flow} Res: {self.residual} {self.is_residual}"


# lista sąsiedztwa
class ListGraph:

    def __init__(self):
        self.list = []
        self.dict = {}
        self.repr = []
        self._size = 0

    def insertVertex(self, vertex: Vertex):
        if vertex not in self.list:
            self.list.append(vertex)
            self.dict[vertex] = len(self.list) - 1
            self.repr.append([])

    def insertEdge(self, vertex1: Union[Vertex, str], vertex2: Union[Vertex, str], edge: Edge=Edge(1)):
        if type(vertex1) == Vertex and type(vertex2) == Vertex:
            idx1 = self.dict[vertex1]
            idx2 = self.dict[vertex2]
            self.repr[idx1].append((idx2, edge))
            # self.repr[idx2].append((idx1, edge.weight)) # można odkomentować/zakomentować zależy chce chcemy graf skierowany czy nie
            self._size += 1
        elif type(vertex1) == str and type(vertex2) == str:
            idx1 = None
            idx2 = None
            for i, vert in enumerate(self.list):
                if vert.key == vertex1:
                    idx1 = i
                    x1, y1 = vert.x, vert.y
                elif vert.key == vertex2:
                    idx2 = i
                    x2, y2 = vert.x, vert.y
                if idx1 is not None and idx2 is not None:
                    break
            self.repr[idx1].append((idx2, edge))
            # distance = np.floor(np.sqrt(np.square(np.abs(x1 - x2)) + np.square(np.abs(y1 - y2))))
            # if (idx2, distance) not in self.repr[idx1] and (idx1, distance) not in self.repr[idx2]:
            #     self.repr[idx1].append((idx2, distance))
                # self.repr[idx2].append((idx1, distance))  # można odkomentować/zakomentować zależy chce chcemy graf skierowany czy nie
            self._size += 1

    def deleteVertex(self, vertex: Vertex):
        self.list.remove(vertex)
        idx = self.dict[vertex]
        # przesunięcie indeksów które są już wpisane w reprezentacji jako krawędzie o 1 w dół od numeru idx
        for neighbours in self.repr:
            for edge in neighbours:
                if edge[0] > idx:
                    new_edge = (edge[0]-1, edge[1])
                    neighbours.remove(edge)
                    neighbours.append(new_edge)
        del self.dict[vertex]
        i = 0
        for key, val in self.dict.items(): # przesunięcie słownika
            if i >= idx:
                self.dict[key] -= 1
            i += 1
        neighbours = self.repr[idx]
        for i in neighbours:
            if (idx, i[1]) in self.repr[i[0]]:
                self.repr[i[0]].remove((idx, i[1]))
        self.repr = self.repr[:idx] + self.repr[idx+1:]

    def deleteEdge(self, vertex1: Vertex, vertex2: Vertex):
        idx1 = self.dict[vertex1]
        idx2 = self.dict[vertex2]
        for edge in self.repr[idx1]:
            if edge[0] == idx2:
                self.repr[idx1].remove(edge)
                break
        for edge in self.repr[idx2]:
            if edge[0] == idx1:
                self.repr[idx2].remove(edge)
                break
        self._size -= 1

    def getVertexIdx(self, vertex: Vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx: int):
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx: int):
        neighbours = []
        for edge in self.repr[vertex_idx]:
            neighbours.append(edge)
        return neighbours

    def order(self):
        return len(self.list)

    def size(self):
        return self._size

    def edges(self):
        edges = []
        for i, neighbours in enumerate(self.repr):
            for vert in neighbours:
                edges.append((self.list[i].key, self.list[vert[0]].key, vert[1]))
        return edges

    def print_dict(self):
        res = "{"
        for key, val in self.dict.items():
            res += f"{key}: {val}, "
        res += "}"
        print(res)

    def print_list(self):
        res = "["
        for vertex in self.list:
            res += f"{vertex}, "
        res += "]"
        print(res)

    def print_repr(self):
        res = "["
        for i, lst in enumerate(self.repr):
            res += f"{self.list[i].key}: [" # {lst}\n"
            for elem in lst:
                res += f"({self.list[elem[0]].key}, {elem[1]}), "
            res += "]\n"
        res += "]"
        print(res)


def dfs_iterative(G: ListGraph, s: int):
    stack = deque([s])
    visited = []
    while stack: # not empty list is true
        s = stack.pop()
        if s not in visited:
            visited.append(s)
            neighoburs_list = G.neighbours(s)
            for u in neighoburs_list[::-1]:
                stack.append(u)
    return visited

def bfs_iterative(G: ListGraph, s: int):
    queue = [s]
    visited = [0 for _ in range(G.order())]
    visited_kolejnosc = []
    parents = [0 for _ in range(G.order())]
    while queue: # not empty list is true
        s = queue.pop(0)
        if visited[s] == 0: # s not in visited
            visited[s] = 1
            visited_kolejnosc.append(s)
            neighoburs_list = G.neighbours(s)
            for u, edge in neighoburs_list:
                if (visited[u] == 0) and (edge.residual > 0):
                    queue.append(u)
                    parents[u] = s
    return visited_kolejnosc, parents


def printGraph(g: ListGraph):
    n = g.order()
    print("------GRAPH------",n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end = " -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j), w, end=";")
        print()
    print("-------------------")