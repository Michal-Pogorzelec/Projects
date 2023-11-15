#include <iostream>
#include "package.hpp"
#include "storage_types.hpp"
#include "nodes.hpp"


int main() {

    Package p1;
    Package p2;
    Package p3(3);

    std::cout << p1.get_id() << p2.get_id() << p3.get_id() << std::endl;
    PackageQueue L1(LIFO);
    std::cout << L1.empty() << std::endl;
    L1.push(std::move(p1));
    L1.push(std::move(p2));
    L1.push(std::move(p3));
    std::cout << L1.empty() << std::endl;

    std::cout << L1.size() << std::endl;

    for(auto it = L1.begin(); it != L1.end(); it++)
    {
        std::cout << it->get_id() << std::endl;
    }
    std::cout << L1.pop().get_id();

    std::vector<Worker> w1;

    return 0;
}
