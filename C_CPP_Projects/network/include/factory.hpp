//
// Created by KASIA ŁUSZCZEWSKA on 04.01.2022.
//

#ifndef NETWORK_FACTORY_HPP
#define NETWORK_FACTORY_HPP
#include "storage_types.hpp"
#include "nodes.hpp"
#include <list>


template <class Node>
class NodeCollection {
public:
    using container_t = typename std::list<Node>;
    using iterator = typename container_t::iterator;
    using const_iterator = typename container_t::const_iterator;
private:
    container_t container;
public:

    NodeCollection<Node>::iterator find_by_id(ElementID id);
    NodeCollection<Node>::const_iterator find_by_id(ElementID id) const;
    NodeCollection<Node>::const_iterator cbegin() const{return container.cbegin();};
    NodeCollection<Node>::const_iterator cend() const{return container.cend();};
    NodeCollection<Node>::iterator begin() {return container.begin();};
    NodeCollection<Node>::iterator end() {return container.end();};

    void add(Node&& node);
    void remove_by_id(ElementID id);
};


class Factory {
private:
    NodeCollection<Ramp> ramp_container;
    NodeCollection<Worker> worker_container;
    NodeCollection<Storehouse> storehouse_container;
public:
    void add_ramp(Ramp&& r){ramp_container.add(std::move(r));};
    void remove_ramp(ElementID id) {ramp_container.remove_by_id(id);};
    NodeCollection<Ramp>::iterator find_ramp_by_id(ElementID id) {return ramp_container.find_by_id(id);};
    NodeCollection<Ramp>::const_iterator find_ramp_by_id(ElementID id) const {return ramp_container.find_by_id(id);};
    NodeCollection<Ramp>::const_iterator ramp_cbegin() const{return ramp_container.cbegin();};
    NodeCollection<Ramp>::const_iterator  ramp_cend() const{return ramp_container.cend();};

    void add_worker(Worker&& w){worker_container.add(std::move(w));};
    void remove_worker(ElementID id){worker_container.remove_by_id(id);};
    NodeCollection<Worker>::iterator find_worker_by_id(ElementID id) {return worker_container.find_by_id(id);};
    NodeCollection<Worker>::const_iterator find_worker_by_id(ElementID id) const {return worker_container.find_by_id(id);};
    NodeCollection<Worker>::const_iterator worker_cbegin() const {return worker_container.cbegin();};
    NodeCollection<Worker>::const_iterator  worker_cend() const {return worker_container.cend();};
//
    void add_storehouse(Storehouse&& s) {storehouse_container.add(std::move(s));};
    void remove_storehouse(ElementID id){storehouse_container.remove_by_id(id);};
    NodeCollection<Storehouse>::iterator find_storehouse_by_id(ElementID id) {return storehouse_container.find_by_id(id);};
    NodeCollection<Storehouse>::const_iterator find_storehouse_by_id(ElementID id) const {return storehouse_container.find_by_id(id);};
    NodeCollection<Storehouse>::const_iterator storehouse_cbegin() const {return storehouse_container.cbegin();};
    NodeCollection<Storehouse>::const_iterator  storehouse_cend() const {return storehouse_container.cend();};

    bool is_consistent();
    void do_deliveries(Time);
    void do_package_passing();
    void do_work(Time);
};



#endif //NETWORK_FACTORY_HPP
