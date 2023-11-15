cmake_minimum_required(VERSION 3.21)
project(lunar_agh_sim C)

set(CMAKE_C_STANDARD 99)

set(SOURCE_FILES bad_file.c)

add_compile_options(-Wall -Wextra -Werror -Wpedantic -pedantic-errors -Wconversion)

add_executable(lunar_agh_sim main.c)
