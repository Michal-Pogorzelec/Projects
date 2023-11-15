#include <fstream>
#include <limits>
#include <vector>
#include <iomanip>
#include "firma.h"

// przeładowany operator wypisywania na ekran
std::ostream& operator<<(std::ostream& os, const Firma &F){

    std::string typ_umowy_str, praca_zdalna_str;

    for(std::size_t i = 0; i < F.size(); i++)
    {
        if (F[i].zwroc_typ_umowy() == 0) typ_umowy_str = "PRACA";
        else if(F[i].zwroc_typ_umowy() == 1 ) typ_umowy_str = "DZIELO";
        else if (F[i].zwroc_typ_umowy() == 2) typ_umowy_str = "ZLECENIE";

        if(F[i].moze_pracowac_zdalnie()) praca_zdalna_str = "Tak";
        else praca_zdalna_str = "Nie";

        os << i << ". " << F[i].zwroc_nazwe() << ": Miesiecze zarobki: " << std::fixed << std::setprecision(2) <<
        F[i].zwroc_miesieczne_zarobki() <<" zl. Zarobione pieniadze: " << F[i].zwroc_zarobione_pieniadze() << " zl. "
        "Stanowisko: " << F[i].funkcja() << ". Typ umowy: " << typ_umowy_str << ".\n Moze pracowac zdalnie: " << praca_zdalna_str <<std::endl;
    }
    return os;
}

// przeładowany operator zapisywania do pliku
std::ostream& operator>>(std::fstream& fs, const Firma &F){
    for(std::size_t i = 0; i < F.size(); i++)
    {
        fs.clear();
        fs << F[i].zwroc_nazwe() << std::endl << std::to_string(F[i].zwroc_miesieczne_zarobki()) << std::endl << F[i].funkcja() <<std::endl << F[i].zwroc_typ_umowy() <<std::endl;
    }
    return fs;
}

// funkcja potrzebna do wywoływania odpowiednich konstruktorów przy wczytywaniu stanowiska z pliku
Pracownik* fabryka(std::string nazwa, double zarobki, std::string stanowisko, umowa typ_umowy){


    if(stanowisko == "Stazysta")
        return new Stazysta(nazwa, zarobki, typ_umowy);
    if(stanowisko == "Programista")
        return new Programista(nazwa, zarobki, typ_umowy);
    if(stanowisko == "Analityk")
        return new Analityk(nazwa, zarobki, typ_umowy);
    if(stanowisko == "Administrator")
        return new Administrator(nazwa, zarobki, typ_umowy);
    if(stanowisko == "Ksiegowy")
        return new Ksiegowy(nazwa, zarobki, typ_umowy);

    throw std::invalid_argument("Could not find that worker type! " + stanowisko);
}

// przeładowany operator czytania z pliku
std::ostream& operator<<(std::fstream& fs, Firma &f){
    std::string nazwa, zarobki_str, stanowisko, typ_umowy_str;
    int typ_umowy;
    double zarobki;
    while(!fs.eof())
    {
        // pobiera linijkę danych z pliku, zawsze pierwsza jest nazwa pracownika
        std::getline(fs, nazwa);
        if (nazwa == "") break;
        std::getline(fs, zarobki_str); // pobiera zarobki pracownika ale w formacie string
        // konwersja z string na float
        zarobki = std::stod(zarobki_str);
        std::getline(fs, stanowisko);
        std::getline(fs, typ_umowy_str);
        typ_umowy = std::stoi(typ_umowy_str);

        try
        {
            Pracownik* pracownik = fabryka(nazwa, zarobki, stanowisko, static_cast<umowa>(typ_umowy));
            f.dodaj_pracownika(pracownik);
        }
        catch (std::invalid_argument &exception)
        {
            std::cout << exception.what() << std::endl;
        }
    }
    return fs;
}


// funkcja zapisujące dane z spisu do pliku
void zapis_do_pliku(const Firma &F, std::string file)
{
    std::fstream plik;
    plik.open(file, std::ios::out );
    if (plik.good()) // sprawdza czy udało się dobrze otworzyć plik
    {
        //  dane zapisują sie  w formacie imie i nazwisko, pod spodem zarobki, stanowisko, i typ umowy (w formie int czyli 0, 1, 2)
        plik >> F;
    }
    else
    {
        throw std::runtime_error("No such file or directory!\n");
    }
    plik.close();
}

std::vector<Pracownik> wczytywanie_z_pliku(Firma &f, std::string file)
{
    std::vector<Pracownik> spis;
    std::fstream plik;
    plik.open(file, std::ios::in);
    if(plik.good())
    {
        plik << f;
    }
    else
    {
        throw std::runtime_error("No such file or directory!\n");
    }
    return spis;
}

