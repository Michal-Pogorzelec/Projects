import json
import random


class BazaPytan:
    def __init__(self):
        self.szyfruj_baze_pytan('baza_pytan_nieszyfrowana.json') # można ale nie trzeba wywoływać tej metody za każdym razem
        # ale raczej jest wskazane bo będzie na bieżąco aktualizowac baze hasel
        self.baza = self.stworz_baze()
        pass

    # klasyczne szyfrowanie polegające na przesuwanie znaków o wartość klucza
    def szyfruj(self, txt, KLUCZ=2):
        zaszyfrowny = ""
        for znak in txt:
            if ord(znak) > 122 - KLUCZ:
                zaszyfrowny += chr(ord(znak) + KLUCZ - 26)
            else:
                zaszyfrowny += chr(ord(znak) + KLUCZ)
        return zaszyfrowny

    # odszyfrowywanie tekstu zakodowanego powyższym sposobem
    def deszyfruj(self, tekst, KLUCZ=2):
        odszyfrowany = ""
        KLUCZM = KLUCZ % 26
        for znak in tekst:
            if (ord(znak) - KLUCZM < 97):
                odszyfrowany += chr(ord(znak) - KLUCZM + 26)
            else:
                odszyfrowany += chr(ord(znak) - KLUCZM)
        return odszyfrowany

    # funkcja która szyfruje całą bazę danych, szyfrowanie jest z domyślnym kluczem=2
    def szyfruj_baze_pytan(self, path: str):
        # po kolei otwieramy plik, pobieramy kategorię, szyfrowujemy ją, nastepnie bierzemy wszystkie hasła tej kategorii
        # szyfrowujemy je, do nowego słownika (który jest jak json) wstawiamy jako klucz zaszyfrowaną kategorię i odpowiadające jej zaszyfrowane hasła
        with open(path, "r") as czysta_baza:
            dane = json.loads(czysta_baza.read())
            zaszyfrowane_dane = {}
            for kat in dane:
                szyfr_kat = self.szyfruj(kat)
                zasz_hasla = []
                for haslo in dane[kat]:
                    zasz_hasla.append(self.szyfruj(haslo))
                zaszyfrowane_dane[szyfr_kat] = zasz_hasla
        with open("zaszyfrowana_baza_pytan.json", 'w') as szyf_baza:
            szyf_baza.write(json.dumps(zaszyfrowane_dane))

    def stworz_baze(self):
        # wczytuje i zwraca zaszyfrowaną bazę danych, na której możemy później operować i losować z niej hasła
        with open("zaszyfrowana_baza_pytan.json") as baza_plik:
            baza = json.loads(baza_plik.read())
        return baza

    def losuj_haslo(self):
        # z pola self.baza losujemy kategorię i hasło z tej kategorii, zwracamy odszyfrowane wartości
        kat_index = random.randint(0, len(self.baza)-1)
        kategorie = list(dict(self.baza).keys())
        kategoria = kategorie[kat_index]
        has_index = random.randint(0, len(self.baza[kategoria])-1)
        haslo = self.baza[kategoria][has_index]
        return self.deszyfruj(kategoria), self.deszyfruj(haslo)
