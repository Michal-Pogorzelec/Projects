#ifndef VEHICLES_HPP_
#define VEHICLES_HPP_

#include <string>
#include <vector>
#include <functional>
#include <cstdint>
#include <memory>

class Vehicle {
public:
    Vehicle(std::string id, std::string brand) : id_(id), brand_(brand), vin_(next_vin_++) {}

    Vehicle(const Vehicle&) = default;

    static void reset_vin_counter() { next_vin_ = 1; }

    std::int64_t get_vin() const { return vin_; }

    std::string get_id() const { return id_; }

    std::string get_brand() const { return brand_; }

    virtual double get_max_speed() const = 0;

    virtual ~Vehicle() = default;

private:
    std::string id_;
    std::string brand_;
    inline static std::int64_t next_vin_ = 1;
    std::int64_t vin_;
};

std::string to_string(const Vehicle& vehicle);

std::string to_string(std::vector<Vehicle*>::const_iterator vehicles_begin,
                      std::vector<Vehicle*>::const_iterator vehicles_end);

class Car : public Vehicle {
public:
    Car(std::string id, std::string brand, double engine_hp) : Vehicle(id, brand), engine_hp_(engine_hp) {}
    Car(const Car&) = default;

    double get_max_speed() const override { return engine_hp_; }

private:
    double engine_hp_;
};

class Bicycle : public Vehicle {
public:
    Bicycle(std::string id, std::string brand, int n_gears) : Vehicle(id, brand), n_gears_(n_gears) {}
    Bicycle(const Bicycle&) = default;

    double get_max_speed() const override { return n_gears_ * 3; }

private:
    int n_gears_;
};

double compute_min_travel_duration(double distance, const Vehicle& vehicle);

std::string compute_min_travel_duration_as_string(double distance, const Vehicle& vehicle);

std::vector<Vehicle*> filter_vehicles(
        std::vector<Vehicle*>::const_iterator vehicles_begin,
        std::vector<Vehicle*>::const_iterator vehicles_end,
        std::function<bool(const Vehicle&)> predicate);


enum Gender {
    Male,
    Female
};

class Driver {
public:
    Driver(std::string name, std::unique_ptr<Vehicle> vehicle_ptr, Gender gender) : name_(name),
                                        vehicle_ptr_(std::move(vehicle_ptr)), gender_(gender) {}
    Driver(std::string name, Gender gender) : Driver(name, nullptr, gender) {}
    Driver(Driver& driver) = delete;
    Driver(Driver&& driver) : name_(driver.name_), vehicle_ptr_(std::move(driver.vehicle_ptr_)) {} //przenoszący konstruktor kopiujący
    Driver& operator=(Driver& driver) = delete;
    Driver& operator=(Driver&& driver);

    void assign_vehicle(std::unique_ptr<Vehicle> vehicle_ptr){
        vehicle_ptr_ = std::move(vehicle_ptr);
    }
    std::string get_name() const {return name_;}
    Gender get_gender() const {return gender_;}
    const Vehicle* get_vehicle() const {return vehicle_ptr_.get(); }

private:
    std::string name_;
    std::unique_ptr<Vehicle> vehicle_ptr_;
    Gender gender_;
};


std::string to_string(const Driver&);

void assign_vehicle_to_driver(std::vector<std::unique_ptr<Vehicle>>& vehicles, Driver& owner);
#endif /* VEHICLES_HPP_ */
