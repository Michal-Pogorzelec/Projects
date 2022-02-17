# klasa do obsługi kont graczy i bazy kont
import json
from tkinter import messagebox


class BazaGraczy:
    def __init__(self):
        self.baza = self.wczytaj_baze()

    # funkcja dodająca nowych graczy do bazy kont
    def rejestracja(self, nick: str, mail: str, plec: str):
        unique_nick = True
        # sprawdzenie czy dany nick znajduje się w bazie
        for gracz in self.baza:
            if gracz[0] == nick:
                unique_nick = False
                break
        if not unique_nick:
            messagebox.showwarning("Warning", "Podany nick jest zajęty spróbuj ponownie.")

        if unique_nick:
            unique_mail = True
            # sprawdzenie czy mail znajduje się w bazie
            for gracz in self.baza:
                if gracz[1] == mail:
                    unique_mail = False
                    break
            if not unique_mail:
                messagebox.showwarning("Warning", "Podany mail jest zajęty spróbuj ponownie.")

            # otwieranie pliku
            if unique_mail:
                with open("baza_kont.txt", "a") as baza_plik:
                    # zapisanie nowego gracza do bazy
                    baza_plik.write(f"\n{nick} {mail} {plec}")
                    # dodaję też od razu nick gracza do bazy wyników
                    self.dodaj_do_bazy_wynikow(nick)
                    messagebox.showinfo("Information", "Poprawnie dodano gracza.")

# funckja dodająca nowego gracza do bazy wyników
    def dodaj_do_bazy_wynikow(self, nick):
        with open("wyniki.json", "r") as wyniki_odczyt:
            dane = json.loads(wyniki_odczyt.read())
            dane[nick] = []
        with open("wyniki.json", "w") as wyniki_zapis:
            json.dump(dane, wyniki_zapis)

# funkcja dodające wynik z konretnej rozgrywki do bazy wyników
    # baza wyników wygląda tak, że mamy nick gracza i w liście wypisane wyniki z poprzednich gier
    def dodaj_wynik_do_bazy(self, nick: str, wynik: int):
        with open("wyniki.json", "r") as wyniki_odczyt:
            dane = json.loads(wyniki_odczyt.read())
            nowy_zapis = dane[nick] + [wynik]
            dane[nick] = nowy_zapis
        with open("wyniki.json", "w") as wyniki_zapis:
            json.dump(dane, wyniki_zapis)

# wczytywanie bazy kont do listy
    def wczytaj_baze(self):
        with open("baza_kont.txt", "r") as baza_plik:
            content = baza_plik.readlines()
            baza = []
            for line in content:
                baza.append(line.split(" "))
        return baza

# sprawdzenie czy gracz o danym nicku jest już w bazie
    def sprawdz_czy_w_bazie(self, nick):
        w_bazie = False
        for gracz in self.baza:
            if nick == gracz[0]:
                w_bazie = True
        return w_bazie

