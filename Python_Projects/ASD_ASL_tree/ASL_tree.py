from copy import copy


class Node:

    def __init__(self, key, val):
        self.key = key
        self.value = val
        self.left_child = None
        self.right_child = None
        self.previous = None
        self.weighting = 0

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


class AVL:

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

    def LL_rotate(self, init_node: Node):
        B = init_node.left_child
        parent = init_node.previous
        init_node.left_child = B.right_child
        if init_node.left_child is not None:
            init_node.left_child.previous = init_node
        B.right_child = init_node
        B.previous = parent
        init_node.previous = B
        if parent is None:
            self.head = B
        elif parent.left_child is init_node:
            parent.left_child = B
        else:
            parent.right_child = B
        if B.weighting == 1:
            init_node.weighting = 0
            B.weighting = 0
        else:
            init_node.weighting = 1
            B.weighting = -1

    def RR_rotate(self, init_node: Node):
        B = init_node.right_child
        parent = init_node.previous
        init_node.right_child = B.left_child
        if init_node.right_child is not None:
            init_node.right_child.previous = init_node
        B.left_child = init_node
        B.previous = parent
        init_node.previous = B
        if parent is None:
            self.head = B
        elif parent.left_child is init_node:
            parent.left_child = B
        else:
            parent.right_child = B
        if B.weighting == -1:
            init_node.weighting = 0
            B.weighting = 0
        else:
            init_node.weighting = -1
            B.weighting = 1

    def RL_rotate(self, init_node: Node):
        B = init_node.right_child
        C = B.left_child
        parent = init_node.previous
        B.left_child = C.right_child
        if B.left_child is not None:
            B.left_child.previous = B
        init_node.right_child = C.left_child
        if init_node.right_child is not None:
            init_node.right_child.previous = init_node
        C.left_child = init_node
        C.right_child = B
        init_node.previous = C
        B.previous = C
        C.previous = parent
        if parent is None:
            self.head = C
        elif parent.left_child is init_node:
            parent.left_child = C
        else:
            parent.right_child = C
        if C.weighting == -1:
            init_node.weighting = 1
        else:
            init_node.weighting = 0
        if C.weighting == 1:
            B.weighting = -1
        else:
            B.weighting = 0
        C.weighting = 0

    def LR_rotate(self, init_node: Node):
        B = init_node.left_child
        C = B.right_child
        parent = init_node.previous
        B.right_child = C.left_child
        if B.right_child is not None:
            B.right_child.previous = B
        init_node.left_child = C.right_child
        if init_node.left_child is not None:
            init_node.left_child.previous = init_node
        C.right_child = init_node
        C.left_child = B
        init_node.previous = C
        B.previous = C
        C.previous = parent
        if parent is None:
            self.head = C
        elif parent.left_child is init_node:
            parent.left_child = C
        else:
            parent.right_child = C
        if C.weighting == 1:
            init_node.weighting = -1
        else:
            init_node.weighting = 0
        if C.weighting == -1:
            B.weighting = 1
        else:
            B.weighting = 0
        C.weighting = 0

    def get_balance(self, node: Node):
        if node is None:
            return 0
        return self.height(node.left_child) - self.height(node.right_child)

    def balance(self, current: Node):
        if current is None:
            return current
        leftH = self.height(current.left_child)
        rightH = self.height(current.right_child)

        if leftH > rightH + 1:
            leftleftH = self.height(current.left_child.left_child)
            leftrightH = self.height(current.left_child.left_child)

            if leftleftH >= leftrightH:
                return self.RR_rotate(current)
            else:
                return self.LR_rotate(current)

        if rightH > leftH + 1:
            rightleftH = self.height(current.right_child.left_child)
            rightrightH = self.height(current.right_child.right_child)

            if rightrightH >= rightleftH:
                return self.LL_rotate(current)
            else:
                return self.RL_rotate(current)


    def insert(self, elem: Node):
        if self.head is None:
            self.head = elem
        else:
            temp = self.head
            while 1:
                if elem.key < temp.key:
                    # wstawianie do lewej gałęzi
                    if temp.left_child is None:
                        elem.previous = temp
                        temp.left_child = elem
                        break
                    else:
                        temp = temp.left_child
                        continue
                elif elem.key > temp.key:
                    # wstawianie do prawej gałęzi
                    if temp.right_child is None:
                        elem.previous = temp
                        temp.right_child = elem
                        break
                    else:
                        temp = temp.right_child
                        continue
                else:
                    temp.value = elem.value
                    break

            # uaktualnienie wag
            if temp.weighting != 0:
                temp.weighting = 0
            else:
                if temp.left_child is elem:
                    temp.weighting = 1
                else:
                    temp.weighting = -1

            # sprawdzenie balansu poprzednikow i zmiana wag poprzednikow
            temp = elem
            temp2 = temp.previous
            while temp2.previous is not None:
                if temp2.weighting != 0:
                    if temp2.weighting == -1:
                        if temp2.left_child is temp:
                            temp2.weighting = 0
                    if temp2.weighting == 1:
                        if temp2.right_child is temp:
                            temp2.weighting = 0
                if temp2.left_child is temp:
                    temp2.weighting += 1
                else:
                    temp2.weighting += -1
                self.balance(temp2)
                temp = temp2
                temp2 = temp2.previous

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


avl = AVL()
avl.insert(Node(1, 1))
avl.insert(Node(3, 3))
avl.insert(Node(2, 2))
avl.insert(Node(4, 2))
avl.print_tree()
# avl.LL_rotate(avl.search2(3))
avl.print_tree()