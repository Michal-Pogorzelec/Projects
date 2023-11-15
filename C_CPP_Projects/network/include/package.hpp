//
// Created by Paweł on 2021-12-14.
//

#ifndef SIEC_PACKAGE_HPP
#define SIEC_PACKAGE_HPP

#include <set>
#include "types.hpp"


class Package {
private:
    static std::set<ElementID> assigned_IDs; // przechowuje przydzielone obecnie id
    static std::set<ElementID> freed_IDs; // przechowuje wartości użytych kiedyś, ale zwolnionych id
    ElementID ID_;
public:
    Package();
    Package(ElementID id);
    Package(const Package& P) = default;
    Package(Package&& P) = default;
    ElementID get_id() const {return ID_;}
    ~Package();
    Package& operator=(Package&&) noexcept = default;
};


#endif //SIEC_PACKAGE_HPP
