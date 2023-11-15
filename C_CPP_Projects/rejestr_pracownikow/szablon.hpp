
#ifndef MAIN_CPP_SZABLON_HPP
#define MAIN_CPP_SZABLON_HPP

#include <vector>

template <typename T>
class Container {
private:
    std::vector<T*> container_;
public:
    void push_back(T *elem)
    {
        container_.push_back(elem);
    }

    T remove(long long unsigned int index) // long long unsigned int  ponieważ taki typ zwraca container_.size(), i taki sam typ ustawiamy na index
    {                                      // po to, żeby nie porównywać wartości o różnych typach (pojawiało się wtedy ostrzeżenie)
        if(container_.size() < index + 1 || container_.size() <= 0)
        {
            throw std::range_error("Index out of range");
        }
        else
        {
            T buff = *container_[index];
            delete container_[index];
            container_.erase(container_.begin() + index);
            return buff;
        }
    }

    size_t size() const
    {
        return container_.size();
    }

    //przeładowane operatory []
    const T& operator[](std::size_t pos) const { return *(container_[pos]);}
    T& operator[](std::size_t pos) { return *(container_[pos]); }


};


#endif //MAIN_CPP_SZABLON_HPP
