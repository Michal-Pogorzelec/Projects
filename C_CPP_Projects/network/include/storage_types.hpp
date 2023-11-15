//
// Created by micha on 14.12.2021.
//

#ifndef SIEC_STORAGE_TYPES_HPP
#define SIEC_STORAGE_TYPES_HPP

#include "package.hpp"
#include <list>

enum PackageQueueType { LIFO, FIFO };


class IPackageStockpile {
public:
    virtual void push(Package&& P) = 0;
    virtual bool empty() = 0;
    virtual std::size_t size() = 0;
    using const_iterator = std::list<Package>::const_iterator;
    using iterator = std::list<Package>::iterator;

    virtual IPackageStockpile::iterator begin() = 0;
    virtual IPackageStockpile::const_iterator cbegin() const = 0;
    virtual IPackageStockpile::iterator end() = 0;
    virtual IPackageStockpile::const_iterator cend() const = 0;

    virtual ~IPackageStockpile() = default;
};


class IPackageQueue : public IPackageStockpile{
public:
    virtual Package pop() = 0;
    virtual PackageQueueType get_queue_type() const = 0 ;

    ~IPackageQueue() override = default;
};


class PackageQueue: public IPackageQueue{
private:
    std::list<Package> container_;
    PackageQueueType packageQueueType;
public:
    PackageQueue(PackageQueueType typ): packageQueueType(typ) {};
    void push(Package&& P) override;
    bool empty() override;
    std::size_t size() override;
    Package pop() override;
    PackageQueueType get_queue_type() const override {return packageQueueType;};
    IPackageStockpile::iterator begin() override {return container_.begin();};
    IPackageStockpile::const_iterator cbegin() const override {return container_.cbegin();};
    IPackageStockpile::iterator end() override {return container_.end();};
    IPackageStockpile::const_iterator cend() const override {return container_.cend();};

    ~PackageQueue() override = default;
};
#endif //SIEC_STORAGE_TYPES_HPP
