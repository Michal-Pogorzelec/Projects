#include "storage_types.hpp"



void PackageQueue::push(Package&& P) {
    container_.push_back(P);
}

bool PackageQueue::empty() {
    return container_.empty();
}

std::size_t PackageQueue::size() {
    return container_.size();
}

Package PackageQueue::pop() {
    if (packageQueueType == LIFO) {
        auto result = std::move(container_.back());
        container_.pop_back();
        return result;
    }
    else {
        auto result = std::move(container_.front());
        container_.pop_front();
        return result;

    }
}
