#include "vehicles.hpp"

#include <iostream>
#include <sstream>
#include <algorithm>
#include <iomanip>

std::string to_string(const Vehicle& vehicle) {
    std::ostringstream oss;
    oss << vehicle.get_id() << " :  " << vehicle.get_brand();
    return oss.str();
}

std::string to_string(std::vector<Vehicle*>::const_iterator vehicles_begin,
                      std::vector<Vehicle*>::const_iterator vehicles_end) {

    std::string s;
    for (auto it = vehicles_begin; it != vehicles_end; ++it) {
        const auto& vehicle = *(*it);
        s += to_string(vehicle);
        s += "\n";
    }

//  Wersja z użyciem biblioteki standardowej - mniej czytelna...
//  std::string s = std::accumulate(vehicles_begin, vehicles_end, std::string(),
//      [](std::string &s, const Vehicle* vehicle_ptr) -> std::string& {
//    return s += to_string(*vehicle_ptr) + "\n"; });

    return s;
}

double compute_min_travel_duration(double distance, const Vehicle& vehicle) {
    return distance / vehicle.get_max_speed();
}

std::string compute_min_travel_duration_as_string(double distance, const Vehicle& vehicle) {
    std::ostringstream oss;
    oss << std::setprecision(3) << std::fixed
        << compute_min_travel_duration(distance, vehicle) << " h";
    return oss.str();
}

std::vector<Vehicle*> filter_vehicles(
        std::vector<Vehicle*>::const_iterator vehicles_begin,
        std::vector<Vehicle*>::const_iterator vehicles_end,
        std::function<bool(const Vehicle&)> predicate) {

    std::vector<Vehicle*> vehicles_filtered;
    std::copy_if(vehicles_begin, vehicles_end, std::back_inserter(vehicles_filtered),
                 [&predicate](const Vehicle* vehicle_ptr) { return predicate(*vehicle_ptr); });
    return vehicles_filtered;
}

std::string to_string(const Driver& driver) {
    std::string s;

    s = driver.get_name() + " : " + (driver.get_vehicle() == nullptr ? "[no vehicle]" : "[" + to_string(*driver.get_vehicle()) + "]");
    return s;
}

Driver& Driver::operator=(Driver&& driver){
    name_ = driver.name_;
    vehicle_ptr_ = std::move(driver.vehicle_ptr_);

    return (*this);
}

void assign_vehicle_to_driver(std::vector<std::unique_ptr<Vehicle>>& vehicles, Driver& owner) {
        std::unique_ptr<Vehicle> last_vehicle_ptr = (vehicles.size() != 0 ? std::move(vehicles[vehicles.size() - 1]) : nullptr);
        vehicles.pop_back();
        owner.assign_vehicle(std::move(last_vehicle_ptr));

}