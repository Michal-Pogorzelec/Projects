//
// Created by KASIA ŁUSZCZEWSKA on 04.01.2022.
//

#ifndef NETWORK_NODES_HPP
#define NETWORK_NODES_HPP

#include "types.hpp"
#include "package.hpp"
#include "storage_types.hpp"
#include "helpers.hpp"
#include <map>
#include <memory>
#include <optional>
#include <utility>

enum ReceiverType {WORKER, STOREHOUSE};

class IPackageReceiver {
public:

    virtual void receive_package(Package&&) = 0;
    virtual ElementID get_id() const = 0;
    virtual ReceiverType get_receiver_type() const = 0;

    virtual IPackageStockpile::const_iterator begin() const = 0;
    virtual IPackageStockpile::const_iterator cbegin() const = 0;
    virtual IPackageStockpile::const_iterator end() const = 0;
    virtual IPackageStockpile::const_iterator cend() const = 0;
    virtual ~IPackageReceiver() = default;
};


class ReceiverPreferences {
public:
    using preferences_t = std::map<IPackageReceiver*, double>;
    using const_iterator = preferences_t::const_iterator;
    using iterator = preferences_t::iterator;

    ReceiverPreferences(ProbabilityGenerator pg = probability_generator): pg_(std::move(pg)) {}
    void add_receiver(IPackageReceiver* r);
    void remove_receiver(IPackageReceiver* r);
    IPackageReceiver* choose_receiver();
    preferences_t const& get_preferences() const;

    iterator begin() { return preferences_.begin(); }
    const_iterator cbegin() const { return preferences_.cbegin(); }
    iterator end() { return preferences_.end(); }
    const_iterator cend() const { return preferences_.cend(); }

    ~ReceiverPreferences() = default;
private:
    preferences_t preferences_;
    ProbabilityGenerator pg_;
};


class PackageSender {
private:
    std::optional<Package> bufor_ = std::nullopt;
public:
    ReceiverPreferences receiver_preferences_;

    PackageSender(): receiver_preferences_(probability_generator) {}
    PackageSender(const PackageSender&) = default;
    PackageSender(PackageSender&& sender) = default;
    void send_package();
    std::optional<Package> const& get_sending_buffer() const;
    ~PackageSender() = default;

protected:
    virtual void push_package(Package&& p);
};


class Ramp : public PackageSender{
private:
    ElementID ID_;
    TimeOffset di_;
public:
    Ramp(ElementID id, TimeOffset di): PackageSender(), ID_(id), di_(di) {};
    //Ramp(const Ramp&) = default;
    Ramp(Ramp&&) = default;
    void deliver_goods(Time t);
    TimeOffset get_deliver_interval() const {return di_;};
    ElementID get_id() const {return ID_;}

    ~Ramp() = default;
};

class Worker : public IPackageReceiver, public PackageSender{
private:
    ElementID ID_;
    std::unique_ptr<IPackageQueue> queue_;
    TimeOffset pd_;
    std::optional<Package> bufor_przetwarzanych_ = std::nullopt;
    Time package_processing_start_time_;

public:
    Worker(ElementID id, TimeOffset pd, std::unique_ptr<IPackageQueue> q): PackageSender(), ID_(id), queue_(std::move(q)), pd_(pd) {}
    Worker(Worker&&) = default;

    void receive_package(Package&&) override;
    void do_work(Time t);
    TimeOffset get_processing_duration() const {return pd_;};
    Time get_package_processing_start_time() const {return package_processing_start_time_;};
    ElementID get_id() const override {return ID_;};
    ReceiverType get_receiver_type() const override {return WORKER;}

    IPackageStockpile::const_iterator begin() const override {return queue_->begin();};
    IPackageStockpile::const_iterator cbegin() const override {return queue_->cbegin();};
    IPackageStockpile::const_iterator end() const override {return queue_->end();};
    IPackageStockpile::const_iterator cend() const override {return queue_->cend();};

    ~Worker() = default;
};


class Storehouse : public IPackageReceiver{
private:
    ElementID ID_;
    std::unique_ptr<IPackageStockpile> d_;
public:
    Storehouse(ElementID id, std::unique_ptr<IPackageStockpile> d = std::make_unique<PackageQueue>(PackageQueue(FIFO)));
//    Storehouse(const Storehouse&) = default;
    Storehouse(Storehouse&&) = default;
    void receive_package(Package&&) override;
    ElementID get_id() const override {return ID_;};
    ReceiverType get_receiver_type() const override {return STOREHOUSE;}

    IPackageStockpile::const_iterator begin() const override {return d_->begin();};
    IPackageStockpile::const_iterator cbegin() const override {return d_->cbegin();};
    IPackageStockpile::const_iterator end() const override {return d_->end();};
    IPackageStockpile::const_iterator cend() const override {return d_->cend();};

    ~Storehouse() = default;
};


#endif //NETWORK_NODES_HPP
