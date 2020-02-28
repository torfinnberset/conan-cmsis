cmake_minimum_required(VERSION 3.14)

SET(ARCHITECTURE "x86_64" CACHE STRING "Some user-specified option")

if (ARCHITECTURE STREQUAL "x86_64")
    message(WARNING "Compiling for native platform, probably")
else ()
    # Include cross compiling toolchain
    include(arm-none-eabi.cmake)
endif ()

project(CMSIS C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

################################################################################################################

file(GLOB_RECURSE CMSIS_DSP_SOURCES CMSIS_5/CMSIS/DSP/Source/*.c)

if (ARCHITECTURE STREQUAL "x86_64")
    # Will only be compiled for native
    list(APPEND CMSIS_DSP_SOURCES arm_bitreversal.c)
else ()
    # Will only be compiled for ARM
    file(GLOB_RECURSE ASM_SOURCES CMSIS_5/CMSIS/DSP/Source/*.S)
    list(APPEND CMSIS_DSP_SOURCES ${ASM_SOURCES})
endif ()

add_library(CMSIS-DSP ${CMSIS_DSP_SOURCES})

# https://foonathan.net/blog/2018/10/17/cmake-warnings.html
target_include_directories(
        CMSIS-DSP
        PRIVATE
            CMSIS_5/CMSIS/DSP/Include
            CMSIS_5/CMSIS/Core/Include
        SYSTEM INTERFACE
            CMSIS_5/CMSIS/DSP/Include
            CMSIS_5/CMSIS/Core/Include
)

string(TOLOWER "${ARCHITECTURE}" ARCH)

if (ARCH STREQUAL "cortex-m0" OR ARCH STREQUAL "cortex-m1")
    # Cortex M0, M0+ and M1
    set(ARM_ARCH_FLAG "__ARM_ARCH_6M__")
    set(ARCH "armv6-m")
    set(TUNE "cortex-m0") #TODO: can optimize further with M0+/M1
elseif (ARCH STREQUAL "cortex-m3")
    # Cortex M3
    set(ARM_ARCH_FLAG "__ARM_ARCH_7M__")
    set(ARCH "armv7-m")
    set(TUNE "cortex-m3")
elseif (ARCH STREQUAL "cortex-m4")
    # Cortex M4 (without floating point)
    set(ARM_ARCH_FLAG "__ARM_ARCH_7EM__")
    set(ARCH "armv7e-m")
    set(TUNE "cortex-m4")
elseif (ARCH STREQUAL "cortex-m4f")
    # Cortex M4F
    set(ARM_ARCH_FLAG "__ARM_ARCH_7EM__")
    set(ARCH "armv7e-m")
    set(TUNE "cortex-m4")

    # Enable floating point co-processor
    target_compile_definitions(
        CMSIS-DSP
        PUBLIC
        -D__FPU_PRESENT
        -D__FPU_USED
    )
else ()
    # Native platform?
    set(ARM_ARCH_FLAG "__ARM_ARCH_6M__") # Compile as Cortex M0
    set(ARCH "native")
    set(TUNE "native")
endif (ARCH STREQUAL "cortex-m0" OR ARCH STREQUAL "cortex-m1")

message("Target CPU ARCH set to '${ARCH}', adding compile definition -D${ARM_ARCH_FLAG}")

target_compile_definitions(
        CMSIS-DSP
        PUBLIC
        -D${ARM_ARCH_FLAG}
)

if (ARCH STREQUAL "")
    message(WARNING "No ARCH set")
else ()
    message("Setting -march=${ARCH} and -mtune=${TUNE}")

    # Optimize code for given architecture
    # This will make the library non-portable, but potentially much faster due to advanced SIMD instructions
    target_compile_options(
            CMSIS-DSP
            PUBLIC
            -march=${ARCH} -mtune=${TUNE}
    )
endif (ARCH STREQUAL "")
