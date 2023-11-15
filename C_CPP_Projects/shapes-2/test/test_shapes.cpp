#include "gtest/gtest.h"

#include "shapes.hpp"
#include <memory>

TEST(SquareTest, area) {
    Square square(0.0, 0.0, 1.0);
    EXPECT_EQ(square.area(), 1.0);

    Shape& shape = square;
    EXPECT_EQ(shape.area(), 1.0);
}

TEST(CircleTest, area) {
    Circle circle(0.0, 0.0, 1.0);
    EXPECT_EQ(circle.area(), PI);

    Shape& shape = circle;
    EXPECT_EQ(shape.area(), PI);
}

TEST(ShapesAuxTest, totalAreaOfShapeCollection){

    std::vector<std::unique_ptr<Shape>> v;
    v.push_back(std::make_unique<Square>(0.0, 0.0, 1));
    v.push_back(std::make_unique<Circle>(0.0, 0.0, 1));

    std::vector<Shape*> v_rawptr;
    v_rawptr.reserve(v.size());
    std::transform(v.begin(), v.end(), std::back_inserter(v_rawptr),
                   [] (const std::unique_ptr<Shape>& up) {return up.get();});
    EXPECT_EQ(calculate_total_area(v_rawptr),1+ PI);
}

