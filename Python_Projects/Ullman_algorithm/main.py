import numpy
import numpy as np

from graphs import *
from typing import Union


def ullman_1_0(used_columns, current_row, G: Union[MatrixGraph, numpy.array], P: Union[MatrixGraph, numpy.array],
           M: Union[MatrixGraph, numpy.array], no_recursion: int=0, no_of_iso: int=0):
    no_recursion += 1
    if current_row == M.shape[0]:
        if (P == M @ (M @ G).T).all():
            no_of_iso += 1
        return no_of_iso, no_recursion

    M_prim = np.copy(M)
    size = M_prim.shape[1]
    for c in range(size):
        if used_columns[c] == 0:
            M_prim[current_row, c] = 1
            for i in range(size):
                if i is not c:
                    M_prim[current_row, i] = 0
            used_columns[c] = 1
            result = ullman_1_0(used_columns, current_row+1, G, P, M_prim)
            no_recursion += result[1]
            no_of_iso += result[0]
            used_columns[c] = 0
    return no_of_iso, no_recursion


def ullman_2_0(used_columns, current_row, G: Union[MatrixGraph, numpy.array], P: Union[MatrixGraph, numpy.array],
           M: Union[MatrixGraph, numpy.array], no_recursion: int=0, no_of_iso: int=0):
    M_0 = np.zeros((P.shape[0], G.shape[1]))
    for i in range(M_0.shape[0]):
        for j in range(M_0.shape[1]):
            n_i = np.count_nonzero(P[i,:])
            n_j = np.count_nonzero(G[j,:])
            if n_i <= n_j:
                M_0[i, j] = 1

    no_recursion += 1
    if current_row == M.shape[0]:
        if (P == M @ (M @ G).T).all():
            no_of_iso += 1
        return no_of_iso, no_recursion

    M_prim = np.copy(M)

    size = M_prim.shape[1]
    for c in range(size):
        if M_0[current_row, c] == 1:
            if used_columns[c] == 0:
                M_prim[current_row, c] = 1
                for i in range(size):
                    if i is not c:
                        M_prim[current_row, i] = 0
                used_columns[c] = 1
                result = ullman_2_0(used_columns, current_row+1, G, P, M_prim)
                no_recursion += result[1]
                no_of_iso += result[0]
                used_columns[c] = 0
    return no_of_iso, no_recursion


def prune(M: Union[MatrixGraph, numpy.array], G: Union[MatrixGraph, numpy.array], P: Union[MatrixGraph, numpy.array], current_row):
    M_has_changed = False

    while not M_has_changed:
        change = False
        for j in range(M.shape[1]):
            for i in range(M.shape[0]):
                if M[i, j] == 1:
                    for x in range(len(P[i])):
                        if P[i, x] == 1:
                            for y in range(len(G[j])):
                                if M[x, y] == 1:
                                    if G[j, y] == 0:
                                        M[i, j] = 0
                                        change = True
        if not change:
            M_has_changed = True
    for i in M[:current_row]:
        if (i == 0).all():
            return False
    return True


def ullman_3_0(used_columns, current_row, G: Union[MatrixGraph, numpy.array], P: Union[MatrixGraph, numpy.array],
           M: Union[MatrixGraph, numpy.array], no_recursion: int=0, no_of_iso: int=0):

    M_0 = np.zeros((P.shape[0], G.shape[1]))
    for i in range(M_0.shape[0]):
        for j in range(M_0.shape[1]):
            n_i = np.count_nonzero(P[i,:])
            n_j = np.count_nonzero(G[j,:])
            if n_i <= n_j:
                M_0[i, j] = 1

    no_recursion += 1
    if current_row == M.shape[0]:
        if (P == M @ (M @ G).T).all():
            no_of_iso += 1
        return no_of_iso, no_recursion

    M_prim = np.copy(M)
    size = M_prim.shape[1]
    prune_result = prune(M_prim, G, P, current_row)
    for c in range(size):
        if prune_result:
            if M_0[current_row, c] == 1:
                if used_columns[c] == 0:
                    M_prim[current_row, c] = 1
                    for i in range(size):
                        if i is not c:
                            M_prim[current_row, i] = 0
                    used_columns[c] = 1
                    result = ullman_3_0(used_columns, current_row+1, G, P, M_prim)
                    no_recursion += result[1]
                    no_of_iso += result[0]
                    used_columns[c] = 0
    return no_of_iso, no_recursion



graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]

G_mat = MatrixGraph()
P_mat = MatrixGraph()
#
for letter in [chr(i) for i in range(65, 70+1)]:
    G_mat.insertVertex(Vertex(key=letter))
    if ord(letter) < 68:
        P_mat.insertVertex(Vertex(key=letter))

for edge in graph_G:
    G_mat.insertEdge(edge[0], edge[1], edge[2])

for edge in graph_P:
    P_mat.insertEdge(edge[0], edge[1], edge[2])

G_numpy = G_mat.convert_to_numpy()
P_numpy = P_mat.convert_to_numpy()

# print(G_numpy, P_numpy, end="\n")

M2 =  np.array([[0., 0., 0., 1., 0., 0.],
 [0., 0., 1., 0., 0., 0.],
 [0., 0., 0., 0., 1., 0.]])
# print(M2)

M = np.zeros((P_numpy.shape[0], G_numpy.shape[1]))

used_columns = [0] * M.shape[1]

print(f"Dla macierzy M: {M}")
print(ullman_1_0(used_columns, 0, G_numpy, P_numpy, M))
print(ullman_2_0(used_columns, 0, G_numpy, P_numpy, M))
print(ullman_3_0(used_columns, 0, G_numpy, P_numpy, M))

print(f"Dla macierzy M2: {M2}")
print(ullman_1_0(used_columns, 0, G_numpy, P_numpy, M2))
print(ullman_2_0(used_columns, 0, G_numpy, P_numpy, M2))
print(ullman_3_0(used_columns, 0, G_numpy, P_numpy, M2))

M3 = np.array( [[0., 0., 0., 1., 0., 0.],
 [0., 0., 0., 0., 1., 0.],
 [0., 0., 0., 0., 0., 1.]])
print(f"Dla macierzy M3: {M3}")
print(ullman_1_0(used_columns, 0, G_numpy, P_numpy, M3))
print(ullman_2_0(used_columns, 0, G_numpy, P_numpy, M3))
print(ullman_3_0(used_columns, 0, G_numpy, P_numpy, M3))