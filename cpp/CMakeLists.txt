cmake_minimum_required(VERSION 3.0)

project(cpp)

add_executable(cpp main.cpp)


install(TARGETS cpp RUNTIME DESTINATION bin)
