#skonczone
import numpy as np
from typing import Union


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

graf = [ ('A','B',4), ('A','C',1), ('A','D',4),
         ('B','E',9), ('B','F',9), ('B','G',7), ('B','C',5),
         ('C','G',9), ('C','D',3),
         ('D', 'G', 10), ('D', 'J', 18),
         ('E', 'I', 6), ('E', 'H', 4), ('E', 'F', 2),
         ('F', 'H', 2), ('F', 'G', 8),
         ('G', 'H', 9), ('G', 'J', 8),
         ('H', 'I', 3), ('H','J',9),
         ('I', 'J', 9)
        ]

# potrzebne do samego dodania węzłów - w tablicy graf są same krawędzie
letters = [chr(i) for i in range(65, 74+1)]

G = ListGraph()

for letter in letters:
    G.insertVertex(Vertex(key=letter))

for edge in graf:
    G.insertEdge(edge[0], edge[1], Edge(edge[2]))

# G.print_repr()

MST = prim_mst(G)
# MST.print_repr()


def printGraph(g):
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


printGraph(MST)
