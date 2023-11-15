//
// Created by KASIA ŁUSZCZEWSKA on 04.01.2022.
//

#include "factory.hpp"

enum NodeColor {NONVISITED, VISITED, VERIFIED};

template<class Node>
void NodeCollection<Node>::add(Node &&node) {
    container.push_back(std::move(node));
}

template<class Node>
void NodeCollection<Node>::remove_by_id(ElementID id) {
    container.erase(find_by_id(id));

}

template<class Node>
typename std::list<Node>::iterator NodeCollection<Node>::find_by_id(ElementID id) {
    for(auto i = container.begin();i!=container.end();i++){
        if((*i).get_id()==id)
            return i;
    }
    return container.begin();
}

template<class Node>
typename std::list<Node>::const_iterator NodeCollection<Node>::find_by_id(ElementID id) const {
    for(auto i = container.cbegin();i!=container.cend();i++){
        if((*i).get_id()==id)
            return i;
    }
    return container.cbegin();
}

//void remove_receiver(NodeCollection<Ramp>::const_iterator& collection, ElementID id) { //:((
//}

bool has_reachable_storehouse(const PackageSender* sender, std::map<const PackageSender*, NodeColor>& node_colors){
    if (node_colors[sender]==VERIFIED)
        return true;
    node_colors[sender]=VISITED;
    if(sender->receiver_preferences_.get_preferences().empty())
        throw std::logic_error("non defined receivers");
    bool czy_nadawca_ma_choc_jednego_odbiorce_innego_niz_siebie_samego = false;
    auto a=sender->receiver_preferences_.get_preferences();
    for(auto const &i:a){
        if(i.first->get_receiver_type()==STOREHOUSE){
            czy_nadawca_ma_choc_jednego_odbiorce_innego_niz_siebie_samego = true;
        }else
        {
            auto worker=(Worker*)i.first;
            if(sender==worker){
                continue;
            }else
            {
                czy_nadawca_ma_choc_jednego_odbiorce_innego_niz_siebie_samego = true;
            }
            if(node_colors[worker]==NONVISITED){
                has_reachable_storehouse(worker,node_colors);
            }
        }

    }
    node_colors[sender]=VERIFIED;
    if(czy_nadawca_ma_choc_jednego_odbiorce_innego_niz_siebie_samego){
        return true;
    }
    throw std::logic_error("nie ma zweryfikowanego odbiorcy");
}
bool Factory::is_consistent() {
    std::map<const PackageSender*, NodeColor> node_colors;
    for(auto i = ramp_cbegin();i!=ramp_cend();i++){
        node_colors.insert(std::pair<const PackageSender*, NodeColor>((PackageSender*)(&(*i)),NONVISITED)); //i odzobaczył że wksażniki były dobre
    }
    for(auto i = worker_cbegin();i!=worker_cend();i++){
        node_colors.insert(std::pair<const PackageSender*, NodeColor>((PackageSender*)(&(*i)),NONVISITED));
    }

    try{
        for(auto i = ramp_cbegin();i!=ramp_cend();i++){
            has_reachable_storehouse(&(*i),node_colors);
        }
    } catch (std::logic_error &e){
        throw e;
    }
    return true;
}


void Factory::do_deliveries(Time t) {
    for(auto &ramp : ramp_container){
        ramp.deliver_goods(t);
    }
}

void Factory::do_package_passing() {
    for(auto &ramp : ramp_container){
        ramp.send_package();
    }
    for(auto &ramp : worker_container){
        ramp.send_package();
    }
}

void Factory::do_work(Time t ) {
    for(auto &worker : worker_container)
        worker.do_work(t);
}



