from conans import ConanFile, CMake, tools
import os
import glob


class JxrlibConan(ConanFile):
    name = "jxrlib"
    url = ""
    version = "1.1.1"
    description = "Jpeg XR codec."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    license = "BSD 2-Clause"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/Booritas/jxrlib.git", "v{0}".format(self.version))

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os == "Linux":
           cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True
        cmake.configure()
        return cmake

    def build(self):
        # ensure that bundled cmake files are not used
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ["include/jxrlib"]
