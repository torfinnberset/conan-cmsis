# arm-none-eabi cannot create executable test on x86, so try static library instead
SET(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")

# Indicate we aren't compiling for an OS
SET(CMAKE_SYSTEM_NAME Generic)
SET(CMAKE_SYSTEM_VERSION 1)

# Set C and C++ compilers
set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)

set(CMAKE_AR arm-none-eabi-gcc-ar CACHE FILEPATH "Archiver" FORCE)
set(CMAKE_RANLIB arm-none-eabi-gcc-ranlib CACHE FILEPATH "Ranlib" FORCE)

# Set other tools
set(OBJSIZE arm-none-eabi-size)
set(OBJCOPY arm-none-eabi-objcopy)
set(OBJDUMP arm-none-eabi-objdump)
set(DEBUGGER arm-none-eabi-gdb)

# Set library options
set(SHARED_LIBS OFF)
set(STATIC_LIBS ON)
