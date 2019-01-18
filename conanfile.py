from conans import ConanFile, CMake, tools
import os
import shutil


class CmsisConan(ConanFile):
    name = "CMSIS-DSP"
    version = "1.5.3"  # DSP package version
    git_sha = "362bc60946c5626b3f090249a181bed480c86e47"  # origin/develop branch currently
    license = "Apache-2.0"
    author = "Torfinn Berset <torfinn@bloomlife.com>"
    url = "https://github.com/ARM-software/CMSIS_5"
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
        for file in self.exports:
            src = "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), file)
            shutil.copy(src, "{}/{}".format(os.curdir, file))

        cmake = CMake(self)

        cmake.configure(defs={
            "ARCHITECTURE": self.settings.arch
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
