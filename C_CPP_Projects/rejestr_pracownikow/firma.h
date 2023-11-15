#include <utility>
#include <vector>
#include "pracownik.h"
#include "szablon.hpp"

using SpisPracownikow = Container<Pracownik>;
// SpisPracownikow to alias na Container<Pracownik>, żeby było wygodniej przy zapisie

class Firma{
public:
    
    Firma(SpisPracownikow spis): spis_(std::move(spis)) {}
    Firma() = default;

    // funkcja dodająca pracowników
    void dodaj_pracownika(Pracownik *pracownik)
    {
        spis_.push_back(pracownik);
    }

    void zwolnij_pracownika(long long unsigned int index)
    {

        try
        {
            std::cout << "[ " + spis_.remove(index).zwroc_nazwe() + " ]" << " zwolniony." << std::endl << std::endl;
        }
        catch (std::range_error &err)
        {
            std::cout << err.what() << std::endl;
        }

    }

    size_t size() const
    {
        return spis_.size();
    }

    //przeładowane operatory []
    const Pracownik& operator[](std::size_t pos) const { return (spis_[pos]);}
    Pracownik& operator[](std::size_t pos) { return (spis_[pos]); }

private:
    SpisPracownikow spis_;
};