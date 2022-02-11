# Gra w zycie - symulacja komorek
import numpy as np
import random

# -----wprowadzenie danych wejsciowych-----
board_size = int(input("Wprowadź rozmiar planszy do symulacji (nxn). Maksymalny rozmiar to 10: "))
# ograniczenie rozmiaru 10x10 można zmienić ale wydaję mi się, że wtedy plansza jest trochę za duża i wprowadzanie
# ręcznych zmian, na planszy mogłoby być problematyczne
if board_size <= 0 or board_size > 10:
    raise Exception("Błędny rozmiar planszy do symulacji")
live_cell_number = int(input("Wprowadz ile komorek na start chciałbyś umieścić na planszy.\n"
                            f"Zostaną one rozmieszczone losowo. Liczba dostępnych komórek to {board_size ** 2}. "))
if live_cell_number < 0 or live_cell_number > board_size**2:
    raise Exception("Błędny liczba żywych komórek")
# stworzenie planszy
board = np.zeros((board_size, board_size), dtype=int)


# -----losowe rozmieszczenie komórek-----
counter = 0
while counter < live_cell_number:
    random_x = random.randint(0, board_size - 1)
    random_y = random.randint(0, board_size - 1)
    if board[random_x][random_y] == 0:
        board[random_x][random_y] = 1
        counter += 1


# -----funkcjonalnosci-----

# funkcja zwracająca wszystkich sąsiadów komórki o współrzednych x, y
neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x < board_size and
                                   -1 < y < board_size and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 < board_size) and
                                   (0 <= y2 < board_size))]

# funkcja określające co się stanie z komórkami po rundzie symulacji - uwzględnia podane zasady
def should_survive():
    should_be_live = {}
    for i in range(len(board)):
        for j in range(len(board)):
            should_be_live[(i, j)] = False
            cell_neighbours = neighbors(i, j)
            living_neigbours = 0
            for x, y in cell_neighbours:
                if board[x][y] == 1:
                    living_neigbours += 1
            if board[i][j] == 0 and living_neigbours == 3:
                should_be_live[(i, j)] = True
            elif board[i][j] == 1 and living_neigbours in [2, 3]:
                should_be_live[(i, j)] = True
            elif board[i][j] == 1 and (living_neigbours < 2 or living_neigbours >= 4):
                should_be_live[(i, j)] = False
    return should_be_live


# następna runda
def next_round():
    should_be_live = should_survive()
    for key, val in should_be_live.items():
        board[key[0]][key[1]] = val # przypisuje wartość val ze słownika, ponieważ True to 1 False to 0


# ożyw komórkę
def ressurect_cell(x: int, y: int):
    board[y][x] = 1


# uśmierć komórkę
def kill_cell(x: int, y: int):
    board[y][x] = 0


# raport
def report(n_sim: int, n_kills: int, n_ress: int):
    num_of_live_cell = 0
    for line in board:
        num_of_live_cell += sum(line)
    print("Raport\n"
          f"Symulacja skończyła się po {n_sim} rundach\n"
          f"Symulacja zaczęła się z {live_cell_number} żywymi komórkami.\n"
          f"Liczba komórek, które zostały przy życiu to: {num_of_live_cell}\n"
          f"Liczba komórek ożywionych przez użytkownika: {n_ress}, uśmierconych: {n_kills}.")

# do wyświetlania planszy
def print_board(n_sim):
    print(f"\nTo {n_sim} runda symulacji.")
    print("-----PLANSZA-----")
    zywa_emotka = "✅"
    niezywa_emotka = "❎"
    for i in range(board_size+1):
        if i == 0:
            line = " |"
        else:
            line = f"{i-1}|"
        for j in range(board_size):
            if i == 0:
                line += f"{j} |"
            elif i >= 1:
                if board[i-1][j] == 1:
                    line += f"{zywa_emotka}|"
                else:
                    line += f"{niezywa_emotka}|"
        print(line)


# ----- Symulacja -----

choice = 0
num_of_sim = 0
num_of_kills = 0
num_of_resurrection = 0
while choice != 4:
    print_board(num_of_sim)
    print("\n-----MENU-----\n"
          "1. Przeprowadź kolejną rundę symulacji.\n"
          "2. Ożyw komórkę ręcznie.\n"
          "3. Uśmierć komórkę ręcznie.\n"
          "4. Zakończ symulację i wyświetl raport.")
    choice = int(input("Wybór: "))
    if choice not in [1, 2, 3, 4]:
        print("\nBłędny wybór!")
        continue

    if choice == 1:
        next_round()
    if choice == 2:
        try:
            x = int(input("Wprowadź współrzędną x komórki: "))
            y = int(input("Wprowadź współrzędną y komórki: "))
            if 0 <= x < board_size and 0 <= y < board_size:
                ressurect_cell(x, y)
                num_of_resurrection += 1
            else:
                print("\nWartości spoza zakresu planszy")
        except ValueError:
            print("\nZły typ współrzędnych")
            continue

    if choice == 3:
        try:
            x = int(input("Wprowadź współrzędną x komórki: "))
            y = int(input("Wprowadź współrzędną y komórki: "))

            if 0 <= x < board_size and 0 <= y < board_size:
                kill_cell(x, y)
                num_of_kills += 1
            else:
                print("\nWartości spoza zakresu planszy")
        except ValueError:
            print("\nZły typ współrzędnych")
            continue

    if choice == 4:
        report(num_of_sim, num_of_kills, num_of_resurrection)

    num_of_sim += 1




