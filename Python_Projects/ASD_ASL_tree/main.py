# skończone
from copy import copy


class Node:

    def __init__(self, key, val):
        self.key = key
        self.value = val
        self.left_child = None
        self.right_child = None
        self.previous = None

    def __str__(self):
        if self.left_child is None:
            left_side = ""
        else:
            left_side = str(self.left_child)
        if self.right_child is None:
            right_side = ""
        else:
            right_side = str(self.right_child)

        return left_side + f"{self.key}: {self.value}, " + right_side


class RootNode:

    def __init__(self):
        self.head = None

    def search(self, key):
        if self.head is None:
            return None
        else:
            temp = self.head
            while 1:
                if temp is None:
                    return None
                if key < temp.key:
                    temp = temp.left_child
                elif key > temp.key:
                    temp = temp.right_child
                else:
                    return temp.value

# pomocnicza funkcja która zwraca cały węzeł od danego klucza
    def search2(self, key):
        if self.head is None:
            return None
        else:
            temp = self.head
            while 1:
                if temp is None:
                    return None
                if key < temp.key:
                    temp = temp.left_child
                elif key > temp.key:
                    temp = temp.right_child
                else:
                    return temp

    def insert(self, elem: Node):
        if self.head is None:
            self.head = elem
        else:
            temp = self.head
            while 1:
                if elem.key < temp.key:
                    if temp.left_child is None:
                        elem.previous = temp
                        temp.left_child = elem
                        return elem
                    else:
                        temp = temp.left_child
                        continue
                elif elem.key > temp.key:
                    if temp.right_child is None:
                        elem.previous = temp
                        temp.right_child = elem
                        return elem
                    else:
                        temp = temp.right_child
                        continue
                else:
                    temp.value = elem.value
                    return elem

    def delete(self, key):
        if self.head is None:
            return None
        temp = self.head
        while 1:
            if key < temp.key:
                temp = temp.left_child
            elif key > temp.key:
                temp = temp.right_child
            else: # trafiliśmy na szukany klucz
                if temp.right_child is None and temp.left_child is None: # przypadek gdy węzeł nie posiada węzłów dzieci
                    temp2 = temp.previous
                    if temp2.right_child is not None and temp2.right_child.key == key:
                        temp2.right_child = None
                        return
                    if temp2.left_child is not None and temp2.left_child.key == key:
                        temp2.left_child = None
                        return
                    # przypadek gdy węzeł ma tylko jeden węzeł dziecko
                if (temp.right_child is None and temp.left_child is not None) or (temp.right_child is not None and temp.left_child is None):
                    if temp.right_child is None:
                        temp2 = temp.previous
                        if temp2.right_child.key == key:
                            temp2.right_child = temp.left_child
                            temp.left_child.previous = temp2
                            del temp
                            return
                        if temp2.left_child.key == key:
                            temp2.left_child = temp.left_child
                            temp.left_child.previous = temp2
                            del temp
                            return
                    if temp.left_child is None:
                        temp2 = temp.previous
                        if temp2.right_child.key == key:
                            temp2.right_child = temp.right_child
                            temp.right_child.previous = temp2
                            del temp
                            return
                        if temp2.left_child.key == key:
                            temp2.left_child = temp.right_child
                            temp.right_child.previous = temp2
                            del temp
                            return

                if temp.right_child is not None and temp.left_child is not None: # przypadek gdy węzeł ma 2 węzły dzieci
                    min_key_node = copy(temp.right_child)
                    while min_key_node.left_child is not None:
                        min_key_node = min_key_node.left_child
                    self.delete(min_key_node.key)
                    temp.key = min_key_node.key
                    temp.value = min_key_node.value
                    return

    def height(self, start_node: Node="root"):
        if start_node == "root":
            start_node = self.head
        if self.head is None:
            return 0
        if start_node is None:
            return 0
        left_height = self.height(start_node.left_child)
        right_height = self.height(start_node.right_child)
        return max(left_height, right_height) + 1

    def _print_tree(self, node: Node, lvl):
        if node is not None:
            self._print_tree(node.right_child, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self._print_tree(node.left_child, lvl + 5)

    def print_tree(self):
        print("==============")
        self._print_tree(self.head, 0)
        print("==============")

    def __str__(self):
        return "{ " + str(self.head)[:-2] + "}"




elems = {50:'A', 15:'B', 62:'C', 5:'D', 20:'E', 58:'F', 91:'G', 3:'H', 8:'I', 37:'J', 60:'K', 24:'L'}

bst_tree = RootNode()

for k, v in elems.items():
    bst_tree.insert(Node(k, v))

bst_tree.print_tree()
print(bst_tree)
print(bst_tree.search(24))
bst_tree.insert(Node(20, "AA"))
bst_tree.insert(Node(6, "M"))
bst_tree.delete(62)
bst_tree.insert(Node(59, "N"))
bst_tree.insert(Node(100, "P"))
bst_tree.delete(8)
bst_tree.delete(15)
bst_tree.insert(Node(55, "R"))
bst_tree.delete(50)
bst_tree.delete(5)
bst_tree.delete(24)
print(bst_tree.height())
print(bst_tree)
bst_tree.print_tree()
