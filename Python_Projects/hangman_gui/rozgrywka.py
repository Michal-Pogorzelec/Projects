from baza_graczy import BazaGraczy
import random
from tkinter import messagebox
# klasa z funkcjami dotyczącymi samej rozgrywki


class Gameplay(BazaGraczy):
    def __init__(self):
        super().__init__()
        self.lista_graczy = []
        self.liczba_graczy = 0
        self.aktualny_gracz = ""
        self.counter = 0

# dodawanie gracza z bazy kont do bieżącej rozgrywki
    def dodaj_gracza_do_rozgrywki(self, nick):
        is_nick_in_base = False
        for nickname in self.baza:
            if nick == nickname[0]:
                is_nick_in_base = True
                break
        if is_nick_in_base:
            self.lista_graczy.append([nick, 0]) # dodajemy gracza i punkty które będą się zmieniały podczas rozgrywki
            self.liczba_graczy += 1
            messagebox.showinfo("Information", "Gracz został dodany do rozgrywki")
            return 0
        else:
            messagebox.showwarning("Warning", "Nie ma takiego gracza w bazie. Najpierw dokonaj rejestracji.")
            return 1

# losowanie kolejnosci zgadywania
    def losuj_kolejnosc(self):
        wynik = random.randint(0, self.liczba_graczy-1)
        self.aktualny_gracz = self.lista_graczy[wynik][0]
        return wynik

# przynzawanie punktu za odgadnietą literkę
    def przyznaj_punkt(self):
        for i in range(self.liczba_graczy):
            if self.lista_graczy[i][0] == self.aktualny_gracz:
                self.lista_graczy[i][1] += 1

# przyznawanie punktow za odgadniete haslo
    def punkty_za_zwyciestwo(self, dlugosc_hasla, ilosc_odgadnietych_liter):
        mnoznik = dlugosc_hasla - ilosc_odgadnietych_liter
        for i in range(self.liczba_graczy):
            if self.lista_graczy[i][0] == self.aktualny_gracz:
                self.lista_graczy[i][1] *= mnoznik

    def odejmij_za_nietrfione_haslo(self, dlugosc_hasla, ilosc_odgadnietych_liter):
        kara = dlugosc_hasla - ilosc_odgadnietych_liter
        for i in range(self.liczba_graczy):
            if self.lista_graczy[i][0] == self.aktualny_gracz:
                self.lista_graczy[i][1] -= kara

# funkcja do poruszania kolejki
    def rusz_kolejke(self):
        for i in range(self.liczba_graczy-1):
            if self.lista_graczy[i][0] == self.aktualny_gracz:
                self.counter = i
                break
        if self.counter == self.liczba_graczy-1:
            self.counter = 0
            self.aktualny_gracz = self.lista_graczy[0][0]
        elif self.counter < self.liczba_graczy:
            self.counter += 1
            self.aktualny_gracz = self.lista_graczy[self.counter][0]




