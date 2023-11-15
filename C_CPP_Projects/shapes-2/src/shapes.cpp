#include "shapes.hpp"
#include <algorithm>
#include <iterator>
#include <memory>
#include <numeric>

double calculate_total_area(const std::vector<Shape*>& shapes){
    return std::accumulate( std::begin(shapes), std::end(shapes),0.0,
                            [] (double acc, const auto& shape_2) {return acc + shape_2->area();});
}