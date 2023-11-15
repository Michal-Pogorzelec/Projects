#include "gtest/gtest.h"

#include "matlab.hpp"

TEST(MatlabVectorTest, createWithSize) {
    Matlab::Vector<int> v(2U);

    // Użyto ASSERT_XXX, gdyż dalsze warunki testowe mają sens tylko wówczas,
    //   gdy wektor zawiera (co najmniej) dwie składowe. Jeśli warunek nie jest
    //   spełniony, należy bezwzględnie przerwać dalsze wykonywanie testów
    //   (inaczej np. wywołanie `v.get_elem(0)` może rzucić wyjątek, jeśli
    //   kontener jest pusty.
    // EXPECT_XXX jedynie oznacza test jako "nie powiódł się", jednak pozwala na
    //   wykonywanie dalszych instrukcji w ramach tego testu, co często umożlwia
    //   uzyskanie dalszych informacji diagnostycznych (np. tu - informację
    //   o faktycznej wartości obu (!) składowych, niezależnie od tego, czy są
    //   to wartości poprawne, czy też nie.
    ASSERT_EQ(v.size(), 2U);
    EXPECT_EQ(v[0], 0);
    EXPECT_EQ(v[1], 0);
}

TEST(MatlabVectorTest, createFromVector) {
    Matlab::Vector<int> v(std::vector<int>{1, 2});

    ASSERT_EQ(v.size(), 2U);
    EXPECT_EQ(v[0], 1);
    EXPECT_EQ(v[1], 2);
}

TEST(MatlabVectorTest, createFromString) {
    Matlab::Vector<int> v("[1, 2, 3]");

    ASSERT_EQ(v.size(), 3U);
    EXPECT_EQ(v[0], 1);
    EXPECT_EQ(v[1], 2);
    EXPECT_EQ(v[2], 3);
}

TEST(MatlabVectorTest, norm) {
    // Inicjalizacja w poniższym teście została przeprowadzona w sposób bardziej
    //   zwięzły, za pomocą tzw. list initialization:
    //   https://en.cppreference.com/w/cpp/language/list_initialization
    std::vector<int> vs{3, 4, 0};
    Matlab::Vector<int> v(vs);

    EXPECT_EQ(v.norm(), 5);
}

TEST(MatlabVectorTest, addVectorsOfSameSize) {
    Matlab::Vector<int> v1(std::vector<int>{1, 2});
    Matlab::Vector<int> v2(std::vector<int>{4, 5});

    ASSERT_NO_THROW({
                        Matlab::Vector<int> v_sum = Matlab::add_vectors(v1, v2);

                        ASSERT_EQ(v_sum.size(), 2U);
                        EXPECT_EQ(v_sum[0], 5);
                        EXPECT_EQ(v_sum[1], 7);
                    });
}

TEST(MatlabVectorTest, addVectorsOfDifferentSize) {
    Matlab::Vector<int> v1(std::vector<int>{1});
    Matlab::Vector<int> v2(std::vector<int>{1, 2});

    ASSERT_THROW(add_vectors(v1, v2), std::invalid_argument);
}

TEST(MatlabVectorTest, toString) {
    Matlab::Vector<int> v(std::vector<int>{1, 2});

    std::string str = Matlab::to_string(v);

    ASSERT_EQ(str, "[ 1, 2 ]");
}

TEST(MatlabVectorTest, sumElements) {
    Matlab::Vector<int> v(std::vector<int>{1, 2});

    ASSERT_EQ(v.sum(), 3);
}

TEST(MatlabVectorAuxTest, exceptionCatchingWhenAddingVectorsOfSameSizes) {
    Matlab::Vector<int> v1(std::vector<int> { 1 });
    Matlab::Vector<int> v2(std::vector<int> { 1 });

    EXPECT_EQ(Matlab::was_exception_raised_when_adding_vectors(v1, v2), "");
}

TEST(MatlabVectorAuxTest, exceptionCatchingWhenAddingVectorsOfDifferentSizes) {
    Matlab::Vector<int> v1(std::vector<int> { 1 });
    Matlab::Vector<int> v2(std::vector<int> { 1, 2 });

    EXPECT_EQ(Matlab::was_exception_raised_when_adding_vectors(v1, v2), "Vectors have unequal size (1 and 2)");
}

