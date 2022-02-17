#!/usr/bin/env python
# -*- coding: utf-8 -*-

# zasada działania programu
# 1.jeśli chcemy rejestrujemy nowych graczy do bazy
# 2.dodajemy graczy do bieżącej rozgrywki
# 3.losujemy kolejnosc grania
# 4.po kolei wpisujemy literki lub cale haslo
# 5.gdy wygramy lub przegramy możemy albo zapisać wyniki i wyjsc, albo dac nową gre wtedy odnawiają nam się życia ale punktacja zostaje


# zaimportowanie bibliotek
from tkinter import messagebox

from pytania import BazaPytan
from baza_graczy import BazaGraczy
from rozgrywka import Gameplay
from tkinter import *

# -------- Setup ----------
# tworzenie instancji podstawowych klas służących do pełnej rozgrywki i utworzenie paru zmiennych/struktur pomocniczych
# takich jak tablica do wyświetlania, nieodgadnionego hasła, lista z odgadniętymi literami czy ilość żyć
baza_pytan = BazaPytan()
kategoria, haslo = baza_pytan.losuj_haslo()
# print(haslo)

display = []
guessed = []
for i in range(0, len(haslo)):
    display.append("_")

baza_graczy = BazaGraczy()

game = Gameplay()
lives = 9

# ------- Timer -----------
timer = None
czas_trwania_rundy = 20  # sekund


# funkcja do resetowania licznika
def reset_timer() -> None:
    global timer
    window.after_cancel(timer)
    global czas_trwania_rundy
    if len(str(czas_trwania_rundy)) < 2:
        czas_trwania_rundy = "0" + str(czas_trwania_rundy)
    timer_label.config(text=f"00:{czas_trwania_rundy}")


# funkcja do odliczania sekunda po sekundzie
def count_down(count):
    count_sec = count
    if len(str(count_sec)) < 2:
        count_sec = "0" + str(count_sec)
    timer_label.config(text=f"00:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        reset_timer()
        timer_label.config(text=f"Koniec czasu")
        window.after(2000, reset_timer)
        game.rusz_kolejke()


# ----------Funk. -----------
# funkcje wykorzystywane między innymi w różnych przyciskach

# zwraca stringa z tablicą wyników i pozostałą liczbą prób
def lista_graczy_jako_string():
    wynik = f"Tablica\nLiczba prób: {lives}"
    for gracz in game.lista_graczy:
        wynik += f"\n{gracz[0]} punkty: {gracz[1]}"
    return wynik


lista = lista_graczy_jako_string()


# funkcja sprawdzająca czy wpisana literka zawiera się w haśle
def sprawdz_literke():
    global haslo, lives, lista
    literka = literki_input.get().lower()  # lower() na wypadek gdyby ktoś wpisywał duże litery
    if len(literka) > 1:
        messagebox.showwarning("Warning", "Można zgadywać tylko jedną literkę")
        return
    if literka in haslo and literka not in guessed:
        guessed.append(literka)
        for position in range(len(haslo)):
            if literka == haslo[position]:
                display[position] = literka
                haslo_label.config(text=f"Kategoria: {kategoria} Haslo: {''.join(display)}")
        game.przyznaj_punkt()
        lista = lista_graczy_jako_string()
        tablica.config(text=lista)
    else:
        lives -= 1
        if lives > 0:
            lista = lista_graczy_jako_string()
            tablica.config(text=lista)
            new_image = lista_etapow[9 - lives]
            canvas.itemconfig(image_container, image=new_image)
        elif lives == 0:
            messagebox.showwarning("Porażka", "Skończyły ci się próby. Zapisz wyniki i zacznij od nowa.")
            reset_timer()
    if lives > 0:
        game.rusz_kolejke()
        aktualny_gracz_label.config(text=f"Jest kolejka gracza: {game.aktualny_gracz}")
        reset_timer()
        count_down(czas_trwania_rundy)


def nowa_gra():
    global haslo, kategoria, display, guessed, lives, lista
    lives = 9
    # losowanie nowego hasla i zmiana zmiennych globalnych
    kategoria, haslo = baza_pytan.losuj_haslo()
    display = []
    guessed = []
    for i in range(0, len(haslo)):
        display.append("_")
    haslo_label.config(text=f"Kategoria: {kategoria} Haslo: {''.join(display)}")
    reset_timer()
    lista = lista_graczy_jako_string()
    tablica.config(text=lista)
    new_image = lista_etapow[9 - lives]
    canvas.itemconfig(image_container, image=new_image)


# funkcja sprawdzająca czy wpisane hasło jest poprawne
def sprawdz_haslo():
    global haslo, kategoria, display, guessed, lives, lista
    proba = haslo_input.get().lower()
    if proba == haslo:
        # przyznanie punktów
        game.punkty_za_zwyciestwo(len(haslo), len(guessed))
        # aktualizacja listy
        lista = lista_graczy_jako_string()
        tablica.config(text=lista)
        # aktualizacja zdjęcia
        canvas.itemconfig(image_container, image=win_image)
        messagebox.showinfo("Information", "Hasło zostało odgadnięte!\nLosowanie nowego hasła")
    else:
        lives -= 1
        game.odejmij_za_nietrfione_haslo(len(haslo), len(guessed))
        if lives > 0:
            lista = lista_graczy_jako_string()
            tablica.config(text=lista)
            new_image = lista_etapow[9 - lives]
            canvas.itemconfig(image_container, image=new_image)
        elif lives == 0:
            messagebox.showwarning("Porażka", "Skończyły ci się próby. Zapisz wyniki i zacznij od nowa.")
            reset_timer()
    if lives > 0:
        reset_timer()
        count_down(czas_trwania_rundy)


# funkcja do losowania kolejności gry używana przy wciśnięciu przycisku
def losowanie():
    try:
        game.losuj_kolejnosc()
        aktualny_gracz_label.config(text=f"Jest kolejka gracza: {game.aktualny_gracz}")
        count_down(czas_trwania_rundy)
    except ValueError:
        messagebox.showwarning("Warning", "Nie ma graczy do losowania")


# funkcja wywoływana przy wciśnięciu przycisku rejestracja - tworzy nowe okno służące do rejestracji nowych graczy do bazy danych
# baza danych jest aktualizowana po zamnkięciu programu
def okno_rejestracji():
    new_window = Toplevel(window)
    new_window.title("Okno rejestracji")
    new_window.minsize(width=250, height=250)

    nick_input = Entry(new_window, width=30)
    nick_input.insert(END, string="Nickname")
    # nick_input.pack()
    nick_input.grid(padx=10, pady=10, column=0, row=0)

    mail_input = Entry(new_window, width=30)
    mail_input.insert(END, string="Email")
    mail_input.grid(padx=10, pady=10, column=0, row=1)

    gender_input = Entry(new_window, width=30)
    gender_input.insert(END, string="Plec")
    gender_input.grid(padx=10, pady=10, column=0, row=2)

    # wewnętrzna funkcja pozwalająca na wywołanie funkcji do rejestracji
    def wywolaj_rejestracje():
        nick = nick_input.get()
        mail = mail_input.get()
        gender = gender_input.get()
        baza_graczy.rejestracja(nick, mail, gender)

    confirm_button = Button(new_window, text="Zatwierdz", command=wywolaj_rejestracje)
    confirm_button.grid(padx=10, pady=10, column=0, row=3)


# funkcja służąca aby z bazy danych dodać graczy (po nick'ach) do bieżącej rozgrywki
# wywoływana przy kliknięciu przycisku dodaj graczy
def okno_dodawania_do_rozgrywki():
    new_window = Toplevel(window)
    new_window.title("Okno dodawania graczy")
    new_window.minsize(width=250, height=250)

    nick_input = Entry(new_window, width=30)
    nick_input.insert(END, string="Nickname")
    nick_input.grid(padx=10, pady=10, column=0, row=0)

    # wewnętrzna funkcja pozwalająca na wywołanie funkcji dodawania graczy do rozgrywki
    def wywolaj_dodawanie():
        global lista
        nick = nick_input.get()
        unique_nick = True
        for i in range(game.liczba_graczy):
            if game.lista_graczy[i][0] == nick:
                unique_nick = False
                break
        if unique_nick:
            temp = game.dodaj_gracza_do_rozgrywki(nick)
            # aktualizacja listy i labelu
            lista = lista_graczy_jako_string()
            tablica.config(text=lista)
            if temp == 0:
                przyciski_aktywne()
        else:
            messagebox.showwarning("Warning", "Gracz już uczestniczy w rozgrywce")

    add_button = Button(new_window, text="Dodaj", command=wywolaj_dodawanie)
    add_button.grid(padx=5, pady=5, column=0, row=1)


# funkcja do zapisania wyników wszystkich graczy z bieżącej rozgrywki do bazy wynikow
def zapisywanie_wynikow():
    for gracz in game.lista_graczy:
        game.dodaj_wynik_do_bazy(gracz[0], int(gracz[1]))
    messagebox.showinfo("Information", "Wyniki zostały zapisane")


def przyciski_aktywne():
    zgadnij_button['state'] = NORMAL
    zgadnij_button2['state'] = NORMAL
    zapisz_wyniki['state'] = NORMAL
    nowa_gra_button['state'] = NORMAL


# ---------- UI -------------
GREY = "#D8D8D8"
BLUE = "#81F7F3"

# tworzenie interfejsu graficznego
window = Tk()
window.title("Wisielec")
window.minsize(width=525, height=400)
window.config(padx=25, pady=25, bg=GREY)

# tworze instancje wszystkich obrazow, po to by móc je potem dynamicznie zmieniać
win_image = PhotoImage(file="images/win.png")
img0 = PhotoImage(file="images/szub0.png")
img1 = PhotoImage(file="images/szub1.png")
img2 = PhotoImage(file="images/szub2.png")
img3 = PhotoImage(file="images/szub3.png")
img4 = PhotoImage(file="images/szub4.png")
img5 = PhotoImage(file="images/szub5.png")
img6 = PhotoImage(file="images/szub6.png")
img7 = PhotoImage(file="images/szub7.png")
img8 = PhotoImage(file="images/szub8.png")
img9 = PhotoImage(file="images/szub9.png")

lista_etapow = [img0, img1, img2, img3, img4, img5, img6, img7, img8, img9]

canvas = Canvas(height=200, width=200, bg=GREY, highlightthickness=0)
image = PhotoImage(file=f"images/szub0.png")
image_container = canvas.create_image(100, 100, anchor="center", image=image)
canvas.grid(padx=10, pady=10, column=1, row=1)

haslo_label = Label(text=f"Kategoria: {kategoria} Haslo: {''.join(display)}")
haslo_label.grid(padx=5, pady=5, column=1, row=2)

tablica = Label(text=lista)
tablica.grid(padx=10, pady=10, column=2, row=1)

aktualny_gracz_label = Label(text=f"Jest kolejka gracza: {game.aktualny_gracz}")
aktualny_gracz_label.grid(padx=10, pady=10, column=2, row=2)

timer_label = Label(text="00:00", font=("Arial", 24))
timer_label.grid(padx=5, pady=5, column=0, row=1)

# elementy funkcjonalne

literki_input = Entry(width=20)
literki_input.insert(END, string="Tutaj wpisuj literki")
literki_input.grid(padx=5, pady=5, column=1, row=3)

haslo_input = Entry(width=20)
haslo_input.insert(END, string="Tutaj wpisz haslo")
haslo_input.grid(padx=5, pady=5, column=0, row=3)

zgadnij_button = Button(text="Zgadnij", state=DISABLED, command=sprawdz_literke)
zgadnij_button.grid(padx=5, pady=5, column=1, row=4)

zgadnij_button2 = Button(text="Zgadnij", state=DISABLED, command=sprawdz_haslo)
zgadnij_button2.grid(padx=5, pady=5, column=0, row=4)

reg_button = Button(text="Rejestracja", command=okno_rejestracji)
reg_button.grid(padx=10, pady=10, column=0, row=0)

dodaj_graczy = Button(text="Dodaj graczy", command=okno_dodawania_do_rozgrywki)
dodaj_graczy.grid(padx=10, pady=10, column=1, row=0)

losuj_button = Button(text="Losuj kolejnosc", command=losowanie)
losuj_button.grid(padx=10, pady=10, column=2, row=0)

zapisz_wyniki = Button(text="Zapisz wyniki", state=DISABLED, command=zapisywanie_wynikow)
zapisz_wyniki.grid(padx=5, pady=5, column=2, row=3)

nowa_gra_button = Button(text="Nowa gra", state=DISABLED, command=nowa_gra)
nowa_gra_button.grid(padx=5, pady=5, column=2, row=4)

window.mainloop()
