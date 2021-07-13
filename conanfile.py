import os
import shutil
from conans import ConanFile, CMake, tools


class CmsisConan(ConanFile):
    name = "CMSIS-DSP"
    version = "1.9.0"  # DSP package version
    git_sha = "13b9f72f212688d2306d0d085d87cbb4bf9e5d3f"
    license = "Apache-2.0"
    author = "Torfinn Berset <torfinn@bloomlife.com>"
    url = "https://github.com/torfinnberset/CMSIS_5"
    homepage = "http://www.keil.com/pack/doc/CMSIS/DSP/html/index.html"
    description = "A suite of common signal processing functions for use on Cortex-M processor based devices"
    exports = ["CMakeLists.txt", "arm_bitreversal.c", "arm-none-eabi.cmake"]
    topics = ("arm", "dsp", "cmsis")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.url, self.git_sha))
        os.rename("CMSIS_5-{}".format(self.git_sha), "CMSIS_5")

    def build(self):
        for f in self.exports:
            src = "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), f)
            shutil.copy(src, "{}/{}".format(os.curdir, f))

        cmake = CMake(self)

        cmake.configure(defs={
            "ARCHITECTURE": self.settings.arch,
            # Prevents ARM startup code from being generated
            "__PROGRAM_START": None
        })

        cmake.build()

    def package(self):
        self.copy(pattern="*.h", dst="include/", src='CMSIS_5/CMSIS/DSP/Include')
        self.copy(pattern="*.h", dst="include/", src='CMSIS_5/CMSIS/Core/Include')

        self.copy("*CMSIS-DSP.dll", dst="bin", keep_path=False)
        self.copy("*CMSIS-DSP.so", dst="lib", keep_path=False)
        self.copy("*CMSIS-DSP.dylib", dst="lib", keep_path=False)
        self.copy("*CMSIS-DSP.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["CMSIS-DSP"]

        # Prevents ARM startup code from being generated
        self.cpp_info.defines = ['__PROGRAM_START']
