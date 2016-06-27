cmake_minimum_required(VERSION 2.8)
project(chip-client CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pedantic -Wall -Wextra -Wcast-align -Wcast-qual -Wctor-dtor-privacy -Wdisabled-optimization -Wformat=2 -Winit-self -Wmissing-declarations -Wmissing-include-dirs -Wold-style-cast -Woverloaded-virtual -Wredundant-decls -Wshadow -Wsign-conversion -Wsign-promo -Wstrict-overflow=5 -Wswitch-default -Wundef -Werror -Wno-unused")

file(GLOB SOURCE_FILES 
    *.cpp)

add_library(${CMAKE_PROJECT_NAME} STATIC ${SOURCE_FILES})

install(TARGETS ${CMAKE_PROJECT_NAME} 
    DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)

