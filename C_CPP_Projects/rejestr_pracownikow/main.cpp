#include <iostream>
#include "operacje.h"


int main(int argc, char *argv[]) { // pozwala na pobrania argumentow konsoli (cmd)
    // jak to zrobić?  w folderze z naszym projektem, w pliku cmake-build-debug otwieramy konsolę (cmd), i w wierszu poleceń wpisujemy plik .exe naszego projektu i po spacji plik z którego chcemy wczytywać dane
    // w tym przypadku PajorMagdalena-etap1.exe stdin1.txt, klikamy enter i wykonuje się program wczytując po kolei dane z pliku


    // utworzenie kontenera na firmy
    // przechowujemy informacje o firmach w formacie <nazwa, firma>, przy wykonywaniu działań, wybieramy firmę z jakiej chcemy skorzystać
    // i na niej wykonujemy wszystkie operacje
    std::vector<std::pair<std::string, Firma>> zbior_firm;
    // tworzymy domyślną firmę
    zbior_firm.push_back(std::make_pair(std::string("Firma_1"), Firma()));
    // zmienna, mówiąca na firmie i jakim indeksie obecnie działamy
    size_t wybrana_firma = 0;


    // instruckje niezbędne do tego, aby można było uruchomić program z wierszem poleceń
    std::istream *input = &std::cin; // stworzenie domyślnego inputa, ustawiamy go na konsolę
    std::ifstream plik; // zmienna do otworzenia pliku
    if (argc == 2) { // argc to liczba argumentow argv,
        // argv[0] sciezka uruchomieniowa pliku (tutaj PajorMagdalena-etap1.exe), argv[1] to plik z wierszem poleceń, który podajemy w konsoli
        plik.open(argv[1], std::ios::in); // otworzenie pliku w trybie do odczytu
        input = &plik; // zamiana domyślnego wejścia na plik
    }


    bool dzialanie = true;

    while (dzialanie)
    {
        std::cout << "Wybrana firma: " << zbior_firm[wybrana_firma].first << std::endl;
        std::cout
                << "1.Utworz nowa firme\n2.Dodaj pracownika\n3.Usun pracownika\n4.Wypisz spis pracownikow\n5.Symuluj prace\n"
                   "6.Wczytaj spis z pliku\n7.Zapisz spis do pliku\n8.Wyslij pracownika na L4\n"
                   "9.Symuluj picie kawy\n10.Zmien firme na ktorej wykonujesz operacje\n11.Zakoncz dzialanie\n\n";
        int wybor;
        *input >> wybor;
        std::cout << std::endl;

        switch (wybor)
        {
            case 1:
            {
                std::string nazwa;
                std::cout << "Podaj nazwe nowej firmy(nazwa nie moze zawierac spacji): " << std::endl;
                *input >> nazwa;
                zbior_firm.push_back(std::make_pair(nazwa, Firma()));
                break;
            }
            case 2:
            {
                std::string nazwa;
                std::string zarobki_string;
                int typ_umowy_int;
                umowa typ_umowy;
                double zarobki;
                std::cout << "Podaj dane (imie i nazwisko) pracownika: ";

//                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');//za pomocą biblioteki limits ignoruje mi spacje pomiedzy imieniem a nazwiskiem, bez tego program mi świrował, wyczytałam że kiedy pobieramy string w switchu za pomocą std::cin to jest takie zachowanie, to co dodałam pozwala tego uniknąć, nie wiem czy to błąd ale działa
                // dodatkowy getline pełni funkcję cin.ignore, usuwa jednego endline'a
                getline(*input, nazwa);
                getline(*input, nazwa);
                std::cout << std::endl;
                std::cout << "Podaj zarobki pracownika: ";
                *input >> zarobki_string; // wszędzie w miejsce std::cin wstawiłem *input - pozwala to na wczytywanie z konsoli lub z pliku, w zależności od tego jak uruchomimy program
                std::cout << "Podaj typ umowy (0 - PRACA, 1 - DZIELO, 2 - ZLECENIE): " << std::endl;
                *input >> typ_umowy_int;
                if (typ_umowy_int == 0) typ_umowy = PRACA;
                else if (typ_umowy_int == 1) typ_umowy = DZIELO;
                else typ_umowy = ZLECENIE;
                zarobki = std::atof(zarobki_string.c_str());

                if (zarobki > 0)
                {
                    int stanowisko;
                    std::cout<< "Wybierz stanowisko: \n1.Stazysta\n2.Administrator\n3.Programista\n4.Analityk\n5.Ksiegowy" << std::endl;
                    *input >> stanowisko;
                    switch (stanowisko)
                    {
                        case 1:
                        {
                            zbior_firm[wybrana_firma].second.dodaj_pracownika(new Stazysta(nazwa, zarobki, typ_umowy));
                            break;
                        }
                        case 2:
                        {
                            zbior_firm[wybrana_firma].second.dodaj_pracownika(new Administrator(nazwa, zarobki, typ_umowy));
                            break;
                        }
                        case 3:
                        {
                            zbior_firm[wybrana_firma].second.dodaj_pracownika(new Programista(nazwa, zarobki, typ_umowy));
                            break;
                        }
                        case 4:
                        {
                            zbior_firm[wybrana_firma].second.dodaj_pracownika(new Analityk(nazwa, zarobki, typ_umowy));
                            break;
                        }
                        case 5:
                        {
                            if (typ_umowy != PRACA)
                            {
                                std::cout << "Ksiegowy moze byc zatrudniony tylko na umowe o prace. Sprobuj ponownie."
                                          << std::endl;
                            } else zbior_firm[wybrana_firma].second.dodaj_pracownika(new Ksiegowy(nazwa, zarobki, typ_umowy));
                            break;
                        }
                        default:
                        {
                            std::cout << "Bledny wybor" << std::endl;
                            break;
                        }
                    }
                } else
                {
                    std::cout << "Zarobki musza byc wieksze od 0" << std::endl;
                }
                std::cout << std::endl;
                break;
            }
            case 3:
                //usun pracownika
            {
                long long unsigned int index; // wyjaśnienie dlaczego taki typ znajduje się w szablon.hpp, funkcja remove
                std::cout << "Podaj index pracownika, ktorego chcesz usunac: ";
                *input >> index;
                std::cout << std::endl;
                zbior_firm[wybrana_firma].second.zwolnij_pracownika(index);
                break;
            }
            case 4:
            {
                std::cout << zbior_firm[wybrana_firma].second << std::endl;
                break;
            }
            case 5:
            {
                double ilosc_msc;
                std::cout << "Ilosc miesiecy do symulacji: " << std::endl;
                *input >> ilosc_msc;
                for (std::size_t i = 0; i < zbior_firm[wybrana_firma].second.size(); i++)
                {
                    zbior_firm[wybrana_firma].second[i].pracuj(ilosc_msc);
                }
                break;
            }
            case 6:
            {
                //wczytaj z plikuAIL
                std::string nazwa_pliku;
                std::cout << "Podaj adres pliku: ";
                *input >> nazwa_pliku;
                std::cout << std::endl;
                try { wczytywanie_z_pliku(zbior_firm[wybrana_firma].second, nazwa_pliku); }
                catch (std::exception &exception)
                {
                    std::cout << exception.what() << std::endl;
                }
                break;
            }
            case 7:
            {
                //zapisz spis do pliku
                std::string nazwa_pliku;
                std::cout << "Podaj adres pliku: ";
                *input >> nazwa_pliku;
                std::cout << std::endl;
                std::vector<Pracownik> spis;
                zapis_do_pliku(zbior_firm[wybrana_firma].second, nazwa_pliku);
                break;
            }
            case 8:
            {
                size_t index;
                int l_msc;
                std::cout << "Podaj indeks pracownika, ktorego chcesz wyslac na L4: ";
                *input >> index;
                if (index < zbior_firm[wybrana_firma].second.size())
                {
                    std::cout << std::endl;
                    std::cout << "Podaj liczbe miesiecy: ";
                    *input >> l_msc;
                    zbior_firm[wybrana_firma].second[index].wez_L4(l_msc);
                }
                else std::cout << "Brak pracownika o podanym indeksie!" << std::endl;
                break;
            }
            case 9:
            {
                size_t index;
                int l_kaw;
                std::cout << "Podaj indeks pracownika, ktorego ilosc wypitych kaw chcesz zaktualizowac: ";
                *input >> index;
                if (index < zbior_firm[wybrana_firma].second.size())
                {
                    std::cout << std::endl;
                    std::cout << "Podaj ilosc wypitych kaw: ";
                    *input >> l_kaw;
                    zbior_firm[wybrana_firma].second[index].pije_kawe(l_kaw);
                }
                else std::cout << "Brak pracownika o podanym indeksie!" << std::endl;
                break;
            }
            case 10:
            {
                size_t numer;
                size_t i = 0;
                std::cout << "Zbior wszystkich firm: " << std::endl;
                for (const auto& elem : zbior_firm)
                {
                    std::cout << i << ". " << elem.first << std::endl;
                    i++;
                }
                std::cout << "Wybierz numer firmy, ktora chcesz wybrac: " << std::endl;
                *input >> numer;
                if(numer < zbior_firm.size())
                    wybrana_firma = numer;
                else std::cout << "Brak wybranej firmy!" << std::endl;
                break;
            }
            case 11:
            {
                dzialanie = false;
                break;
            }
            default:
            {
                std::cout << "Bledny wybor" << std::endl;
                break;
            }
        }
    }


    plik.close();

    return 0;
}
