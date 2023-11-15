//
// Created by KASIA ŁUSZCZEWSKA on 04.01.2022.
//
#include "nodes.hpp"

using preferences_t = std::map<IPackageReceiver*, double>;
using const_iterator = preferences_t::const_iterator;

Storehouse::Storehouse(ElementID id, std::unique_ptr<IPackageStockpile> d): ID_(id), d_(std::move(d)) {}

void Storehouse::receive_package(Package &&p)
{
    d_->push(std::move(p));
}


preferences_t const& ReceiverPreferences::get_preferences() const
{
    return preferences_;
}



void ReceiverPreferences::add_receiver(IPackageReceiver *r)
{
    preferences_.emplace(r, 1);
    for (auto &elem : preferences_)
    {
        elem.second = 1 / (double)(preferences_.size()); // skaluje prawd. wylosowania odbiorcy, na tym etapie każdy będzie miał to samo prawd.
    }
}

void ReceiverPreferences::remove_receiver(IPackageReceiver *r)
{
    preferences_.erase(r);
    if (!preferences_.empty())
    {
        for (auto &elem: preferences_)
        {
            elem.second = 1 / (double) (preferences_.size());
        }
    }
}
//
IPackageReceiver *ReceiverPreferences::choose_receiver()
{
    double probability = probability_generator();
    double left_lim = 0;
    double right_lim = 0;

    if (!preferences_.empty())
    {
        for (auto &elem: preferences_)
        {
            right_lim += elem.second;
            if (left_lim < probability and probability <= right_lim)
            {
                return elem.first;
            }
            else left_lim += elem.second;
        }
    }
    return nullptr;
}


void PackageSender::push_package(Package &&p)
{
    bufor_.emplace(std::move(p));
}

std::optional<Package> const& PackageSender::get_sending_buffer() const
{
    return bufor_;
}

void PackageSender::send_package()
{
    if(bufor_)
    {
        receiver_preferences_.choose_receiver()->receive_package(bufor_->get_id());
        bufor_.reset();
    }
}



void Ramp::deliver_goods(Time t)
{
    if (t == 1)
    {
        send_package();
    }
    else if ((t-1)%di_ == 0)
    {
        send_package();
    }
}



void Worker::do_work(Time t)
{
    if(!bufor_przetwarzanych_ and queue_) // jeśli bufor jest pusty i jest coś w kolejce
    {
        bufor_przetwarzanych_.emplace(queue_->pop()); // wstaw do bufora
        package_processing_start_time_ = t; // zapamiętaj czas startu przetwarzania
    }
    else if(bufor_przetwarzanych_)
    {
        if (t - package_processing_start_time_ == pd_) // jeśli upłynął czas przetwarzania
        {
            push_package(Package());
            bufor_przetwarzanych_.reset();
        }
    }
}


void Worker::receive_package(Package&& p)
{
    queue_->push(std::move(p));
}

