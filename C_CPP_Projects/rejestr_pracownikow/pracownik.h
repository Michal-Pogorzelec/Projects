#include <iostream>

// typ wyliczeniowy określający na jakiego rodzaju umowie jest pracownik
enum umowa{
    PRACA, DZIELO, ZLECENIE
};


//klasa opisująca pojedynczego pracownika
class Pracownik {
protected:
    std::string nazwa_;
    double zarobki_;
    int ilosc_wypitej_kawy_ = 0;
    int dni_urlopu_ = 20;
    int ilosc_msc_na_L4_ = 0;
    double przepracowane_msc_ = 0;
    umowa typ_umowy_;
    bool praca_zdalna_ = false;
public:
    Pracownik(std::string nazwa, double zarobki, umowa typ_umowy): nazwa_(nazwa), zarobki_(zarobki), typ_umowy_(typ_umowy) {};
    Pracownik(std::string nazwa, double zarobki): nazwa_(nazwa), zarobki_(zarobki) { typ_umowy_ = PRACA;}; //domyślny typ umowy ustawiam na umowę o pracę


    void pracuj(double ilosc_msc)
    {
        przepracowane_msc_ += ilosc_msc;
    }

    bool moze_pracowac_zdalnie() const {return praca_zdalna_;}

    umowa zwroc_typ_umowy() const {return typ_umowy_;}

    void pije_kawe(int liczba_kaw)
    {
        ilosc_wypitej_kawy_ += liczba_kaw;
    }

    std::string zwroc_nazwe() const
    {
        return nazwa_;
    }

    //zrobilem takie warunki na różne liczenie wynagrodzenia w zależności od umowy, ale to można zmienić
    double zwroc_miesieczne_zarobki() const
    {
        if (typ_umowy_ == PRACA) { return zarobki_; }
        else if (typ_umowy_ == DZIELO) { return zarobki_ * 0.9; }
        else { return zarobki_ * 0.8; }
    }

    void wez_L4(int dlugosc)
    {
        ilosc_msc_na_L4_ += dlugosc;
    }

    virtual double premia() const
    {
        if (ilosc_wypitej_kawy_ == 0) { return przepracowane_msc_ * 0.2 * zarobki_; }
        else if(ilosc_wypitej_kawy_ < 40)
        {
            return przepracowane_msc_ * (0.2 - 0.005 * ilosc_wypitej_kawy_) * zarobki_; // przy 40 wypitych kawa premia się zeruje, tą ilość można zmienić, dałem ją losowo
        }
        else { return 0; }
    }

    virtual double zwroc_zarobione_pieniadze() const
    {
        return ilosc_msc_na_L4_ * 0.7 * zwroc_miesieczne_zarobki() + przepracowane_msc_ * zwroc_miesieczne_zarobki() + premia();
    }

    virtual std::string funkcja() const {return "Pracownik" ;}

    virtual ~Pracownik() = default;
};


//Stażyści nie mają premii, ani nie chodzą na urlop
class Stazysta : public Pracownik{
public:
    Stazysta(std::string nazwa, double zarobki, umowa typ_umowy): Pracownik(nazwa, zarobki, typ_umowy) { dni_urlopu_ = 0;};

    double premia() const override { return 0;}

    std::string funkcja() const override
    {
        return "Stazysta";
    }

};

//Administratorzy mają więcej urlopu.
class Administrator : public Pracownik{
public:
    Administrator(std::string nazwa, double zarobki, umowa typ_umowy): Pracownik(nazwa, zarobki, typ_umowy) { dni_urlopu_ = 35;};

    std::string funkcja() const override
    {
        return "Administrator";
    }
};

//Programiści i analitycy mogą pracować zdalnie.
class Programista : public Pracownik{
public:
    Programista(std::string nazwa, double zarobki, umowa typ_umowy): Pracownik(nazwa, zarobki, typ_umowy) { praca_zdalna_ = true;};

    std::string funkcja() const override
    {
        return "Programista";
    }
};

class Analityk : public Pracownik{
public:
    Analityk(std::string nazwa, double zarobki, umowa typ_umowy): Pracownik(nazwa, zarobki, typ_umowy) { praca_zdalna_ = true;};

    std::string funkcja() const override
    {
        return "Analityk";
    }
};

//Księgowi mogą pracować tylko na umowę o pracę
class Ksiegowy : public Pracownik{
public:
    Ksiegowy(std::string nazwa, double zarobki, umowa typ_umowy = PRACA): Pracownik(nazwa, zarobki, typ_umowy) {};

    std::string funkcja() const override
    {
        return "Ksiegowy";
    }
};
