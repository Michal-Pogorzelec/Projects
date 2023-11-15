//
// Created by Paweł on 2021-12-14.
//

#include "package.hpp"
std::set<ElementID> Package::assigned_IDs = {};
std::set<ElementID> Package::freed_IDs = {};

Package::Package() {
    if(!freed_IDs.empty()) {
        ID_ = *freed_IDs.begin(); //przypisuje minimalny element
        freed_IDs.erase(ID_);
        assigned_IDs.insert(ID_); // aktualizuje assigned
    }
    else if(!assigned_IDs.empty()) {
        ID_ = *assigned_IDs.rbegin() + 1; //przypisuje maksymalny element + 1
        assigned_IDs.insert(ID_);
    }
    else {
        ID_ = 1;
        assigned_IDs.insert(ID_);
    }
}


Package::Package(ElementID id): ID_(id) {
    assigned_IDs.insert(ID_);
}

Package::~Package(){
    assigned_IDs.erase(ID_);
    freed_IDs.insert(ID_);
}
