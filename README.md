# conan-cmsis-dsp
Author: Torfinn Berset, 2019

A [Conan](https://conan.io) package for the [ARM CMSIS DSP](https://github.com/ARM-software/CMSIS_5) library, which can be compiled for x86 as well as for ARM architectures.
Currently, the build assumes a _Little Endian_ architecture.

# Cortex-M target

To build for ARM Cortex-M, you need an ARM-GCC toolchain.
- [Homebrew (macOS) version](https://github.com/torfinnberset/homebrew-embedded)
- [Other versions](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm) 

# x86 target 

To enable compilation for x86, we have to use the latest `develop` branch (as of 2019-01-17) as well as a custom 
`arm_bitreversal_32` function. 

The `master` branch currently has issues with non-portable pointer arithmetic, and the `arm_bitreversal_32` function is only available in ARM assembly through the CMSIS repo.

# License

This work follows the Apache-2.0 license, the [same](https://github.com/ARM-software/CMSIS_5/blob/develop/LICENSE.txt) as the CMSIS library itself. The project is not affiliated with ARM or Conan.