import numpy as np
from typing import Union


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
    def __init__(self, weight):
        self.weight = weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight


# macierz sąsiedztwa
class MatrixGraph:

    def __init__(self):
        self.list = []
        self.dict = {}
        self.matrix = []
        self._size = 0

    def insertVertex(self, vertex: Vertex):
        self.list.append(vertex)
        self.dict[vertex] = len(self.list) - 1
        self.matrix.append(([None]*len(self.list)))
        for i in range(len(self.matrix)-1):
            self.matrix[i].append(None)

    def insertEdge(self, vertex1: Union[Vertex, str], vertex2: Union[Vertex, str], edge: Union[Edge, int]=Edge(1)):
        if type(vertex1) == Vertex and type(vertex2) == Vertex:
            idx1 = self.dict[vertex1]
            idx2 = self.dict[vertex2]
            # self.matrix[idx1][idx2] = edge.weight
            # self.matrix[idx2][idx1] = edge.weight # można odkomentować/zakomentować zależy chce chcemy graf skierowany czy nie
            # self._size += 1
            # distance = edge.weight
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
            # distance = np.floor(np.sqrt(np.square(np.abs(x1-x2)) + np.square(np.abs(y1-y2))))
        if isinstance(edge, Edge):
            distance = edge.weight
        else:
            distance = edge
        self.matrix[idx1][idx2] = distance
        self.matrix[idx2][idx1] = distance
        self._size += 1

    def deleteVertex(self, vertex: Vertex):
        self.list.remove(vertex)
        idx = self.dict[vertex]
        del self.dict[vertex]
        i = 0
        for key, val in self.dict.items(): # przesunięcie słownika
            if i >= idx:
                self.dict[key] -= 1
            i += 1
        # usuwanie wszystkich krawędzi z jakimi był połączony vertex
        del self.matrix[idx]
        for mat in self.matrix:
            del mat[idx]

    def deleteEdge(self, vertex1: Vertex, vertex2: Vertex):
        idx1 = self.dict[vertex1]
        idx2 = self.dict[vertex2]
        self.matrix[idx1][idx2] = None
        self.matrix[idx2][idx1] = None # odkomentować gdy to samo zrobimy w insertEdge
        self._size -= 1

    def getVertexIdx(self, vertex: Vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx: int):
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx: int):
        neighbours = []
        i = 0
        for edge in self.matrix[vertex_idx]:
            if edge is not None:
                neighbours.append(i)
            i += 1
        return neighbours

    def order(self):
        return len(self.list)

    def size(self):
        return self._size

    def edges(self):
        edges = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] is not None:
                    edges.append((self.list[i].key, self.list[j].key, self.matrix[i][j]))
        return edges

    def convert_to_numpy(self):
        shape = self.order(), self.size()
        result = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if self.matrix[i][j] is None:
                    result[i][j] = 0
                else:
                    result[i][j] = 1
        return result

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

    def print_matrix(self):
        res = ""
        for i in range(0, len(self.matrix)):
            res += f"{i}: "
            for j in range(0, len(self.matrix[i])):
                res += f"{self.matrix[i][j]} "
            res += "\n"
        print(res)
