cmake_minimum_required(VERSION 3.13)
project(CMSIS C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

################################################################################################################

file(GLOB_RECURSE CMSIS_DSP_C_SOURCES CMSIS_5/CMSIS/DSP/Source/*.c)
file(GLOB_RECURSE CMSIS_DSP_S_SOURCES CMSIS_5/CMSIS/DSP/Source/*.S)

add_library(
        CMSIS-DSP
        ${CMSIS_DSP_C_SOURCES}
        ${CMSIS_DSP_S_SOURCES}
)

target_include_directories(
        CMSIS-DSP
        PUBLIC
        CMSIS_5/CMSIS/DSP/Include
        CMSIS_5/CMSIS/Core/Include
)

