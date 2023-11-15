cmake_minimum_required(VERSION 3.21)
project(impl C)

set(CMAKE_C_STANDARD 99)

add_executable(impl main.c doubly_linked_list.h)
