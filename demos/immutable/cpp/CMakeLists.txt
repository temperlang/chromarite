# Builds one attempt at a time, which run.py writes to build/check.cpp,
# against the C++ that `temper build -b cpp` generates at the repo's top.

cmake_minimum_required(VERSION 3.16)
project(chromarite_immutable CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(TEMPER_OUT ${CMAKE_CURRENT_SOURCE_DIR}/../../../temper.out/cpp)

file(GLOB STD_SOURCES ${TEMPER_OUT}/std/*.cpp)
list(FILTER STD_SOURCES EXCLUDE REGEX "/main\\.cpp$")
add_library(chromarite ${TEMPER_OUT}/chromarite/init.cpp ${STD_SOURCES})
target_include_directories(chromarite PUBLIC ${TEMPER_OUT})

add_executable(check ${CMAKE_BINARY_DIR}/check.cpp)
target_link_libraries(check PRIVATE chromarite)
