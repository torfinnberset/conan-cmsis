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

if (NOT CMAKE_CROSSCOMPILING)
    target_compile_definitions(
            CMSIS-DSP
            PRIVATE
            -D__ARM_ARCH_6M__ # Compile as Cortex M0
    )

    # Optimize code for the same instruction set as we compile on
    # This will make the library non-portable, but potentially much faster due to advanced SIMD instructions
    target_compile_options(
            CMSIS-DSP
            PRIVATE
            -march=native -mtune=native
    )

    #
    # Add bitreversal reference function, which is only available in ARM assembly otherwise
    #
    target_sources(
            CMSIS-DSP
            PRIVATE
            arm_bitreversal.c
    )

endif ()

