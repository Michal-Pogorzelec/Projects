cmake_minimum_required(VERSION 3.17)
project(siec)

set(CMAKE_CXX_STANDARD 17)


add_compile_options(-Wall -Wextra -Werror -Wpedantic -pedantic-errors -Werror=switch)

include_directories(include)

set(SOURCE_FILES
        src/storage_types.cpp
        src/package.cpp
        src/factory.cpp
        src/helpers.cpp
        src/nodes.cpp)

add_executable(siec ${SOURCE_FILES} main.cpp)

include_directories(netsim_tests/include
        netsim_tests/mocks)

set(SOURCES_FILES_TESTS
        netsim_tests/test/test_package.cpp
        netsim_tests/test/test_Factory.cpp
        netsim_tests/test/test_nodes.cpp
        )

# Dodaj konfigurację typu `Test`.
add_executable(my_project_test ${SOURCE_FILES} ${SOURCES_FILES_TESTS} netsim_tests/test/main_gtest.cpp)

# Dodaj katalogi z plikami nagłówkowymi wyłącznie do konkretnej konfiguracji (tu: `Test`).
target_include_directories(my_project_test PUBLIC
        ../../googletest-master/googlemock/include
        ../../googletest-master/googletest/include
        )

# Dodaj podkatalog `googletest-master`.
add_subdirectory(../../googletest-master googletest-master)

# Podlinkuj bibliotekę o identyfikatorze `gmock` (w pliku CMake) wyłącznie do konkretnej
# konfiguracji (tu: `Test`).
target_link_libraries(my_project_test gmock)
