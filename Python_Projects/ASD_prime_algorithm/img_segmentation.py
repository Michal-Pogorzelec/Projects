import numpy as np
from typing import Union
import cv2
from matplotlib import pyplot as plt



class Vertex:
    def __init__(self, x=None, y=None, key=None, brightness=None):
        self.x = x
        self.y = y
        self.key = key
        self.brightness = brightness

    def set_brightness(self, new_brightness):
        self.brightness = new_brightness

    def get_brightenss(self):
        return self.brightness

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


# lista sąsiedztwa
class ListGraph:

    def __init__(self):
        self.list = []
        self.dict = {}
        self.repr = []
        self._size = 0

    def insertVertex(self, vertex: Vertex):
        self.list.append(vertex)
        self.dict[vertex] = len(self.list) - 1
        self.repr.append([])

    def insertEdge(self, vertex1: Union[Vertex, str], vertex2: Union[Vertex, str], edge: Edge=Edge(1)):
        if type(vertex1) == Vertex and type(vertex2) == Vertex:
            idx1 = self.dict[vertex1]
            idx2 = self.dict[vertex2]
            self.repr[idx1].append((idx2, edge.weight))
            self.repr[idx2].append((idx1, edge.weight)) # można odkomentować/zakomentować zależy chce chcemy graf skierowany czy nie
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
            self.repr[idx1].append((idx2, edge.weight))
            self.repr[idx2].append((idx1, edge.weight)) # można odkomentować/zakomentować zależy chce chcemy graf skierowany czy nie
            self._size += 1
            # distance = np.floor(np.sqrt(np.square(np.abs(x1 - x2)) + np.square(np.abs(y1 - y2))))
            # if (idx2, distance) not in self.repr[idx1] and (idx1, distance) not in self.repr[idx2]:
            #     self.repr[idx1].append((idx2, distance))
            #     self.repr[idx2].append(
            #         (idx1, distance))  # można odkomentować/zakomentować zależy chce chcemy graf skierowany czy nie
            #     self._size += 1

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

    def getVertex_by_key(self, key):
        for vertex in self.list:
            if vertex.key == str(key):
                return vertex

    def neighbours(self, vertex_idx: int):
        neighbours = []
        for edge in self.repr[vertex_idx]:
            neighbours.append(edge) # edge = (vertex_id, cost)
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
            res += f"{i}: {lst}\n"
        res += "]"
        print(res)


def prim_mst(G: ListGraph):
    MST = ListGraph()
    for vertex in G.list:
        MST.insertVertex(vertex)

    intree = [0 for _ in range(G.size())] # indeksy w grafie idą od 0 do size-1, w liście każdy indeks będzie miał wartość 0-1, żeby przy
    # sprawdzaniu mieć złożoność O(1), zamiast wstawiać kolejne vertexy do listy i mieć większą złożoność przy sprawdzaniu (komentarz zostawiam sam sobie)

    edges = []

    temp_v = G.list[0]
    temp_id = G.getVertexIdx(temp_v)
    parent_id = -1
    intree[temp_id] = 1
    while sum(intree) < G.size():
        distance = float('inf')
        for edge in G.neighbours(temp_id):
            if edge[0] != parent_id: # sprawdzenie by nie zduplikować krawędzi
                edges.append((temp_id, edge)) # dodajemy krotkę (obecny wierzchołek, (sąsiad wierzch., koszt))
                # dlatego, że nie zawsze dodajemy krawędź obecny wierzchołek - sąsiad, tylko czasem niższy koszt ma inna krawędź z listy
                # dlatego zapamiętuje jej oba wierzcholki
        v1 = v2 = min_cost = None
        for edge in edges:
            if edge[1][1] < distance and (intree[edge[1][0]] + intree[edge[0]] < 2): # sprawdzenie w nawiasie zapobiega stworzeniu cyklu
                v1 = edge[0]
                v2, min_cost = edge[1]
                distance = min_cost
        if v1 is not None: # znaczy że została znaleziona odpowiednia krawędź
            MST.insertEdge(G.getVertex(v1), G.getVertex(v2), Edge(min_cost))
            edges.remove((v1, (v2, min_cost))) # wyrzucamy krawędź którą już wybraliśmy
            intree[v2] = 1
            parent_id = v1
            temp_id = v2
            # temp_v = G.getVertex(temp_id)
            continue
        else: # w przypadku gdy krawędź nie została znaleziona, tzn. skończyły się mozliwości
            return MST
    return MST


def bfs_iterative(G: ListGraph, s: int):
    queue = [s]
    visited = []
    while queue: # not empty list is true
        s = queue.pop(0)
        if s not in visited:
            visited.append(s)
            neighoburs_list = G.neighbours(s)
            for u in neighoburs_list:
                queue.append(u[0])
    return visited


img = cv2.imread("sample.png", cv2.IMREAD_GRAYSCALE)
img = img.astype(np.int16)
graf = ListGraph()
values = []

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        values.append(img[i, j])
        graf.insertVertex(Vertex(x=i, y=j, key=str((img.shape[0]*j)+i), brightness=img[i, j]))


for i in range(1, img.shape[0]-1):
    for j in range(1, img.shape[1]-1):
        for m in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                if (m, n) != (i, j):
                    weight = np.abs(img[m, n] - img[i, j])
                    graf.insertEdge(str((img.shape[0] * j) + i), str((img.shape[0] * n) + m), Edge(weight))
                    graf.insertEdge(str((img.shape[0] * n) + m), str((img.shape[0] * j) + i), Edge(weight))


MST = prim_mst(graf)

edges = MST.edges()

sorted_edges = sorted(edges, key=lambda x: x[2])
to_del_1 = sorted_edges[-1]
to_del_2 = sorted_edges[-2]

v1 = MST.getVertex_by_key(to_del_1[0])
v2 = MST.getVertex_by_key(to_del_2[0])
v1_idx = MST.getVertexIdx(v1)
v2_idx = MST.getVertexIdx(v2)
MST.deleteEdge(v1, v2)
MST.deleteEdge(v2, v1)

IS = np.zeros((img.shape), dtype='uint8')

visited_1 = bfs_iterative(MST, v1_idx)
visited_2 = bfs_iterative(MST, v2_idx)


for pixel in visited_1:
    v = MST.getVertex_by_key(pixel)
    IS[v.x, v.y] = 50

for pixel in visited_2:
    v = MST.getVertex_by_key(str(pixel))
    IS[v.x, v.y] = 250

plt.imshow(IS, cmap="gray")
plt.show()