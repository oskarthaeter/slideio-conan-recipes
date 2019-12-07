from conans import ConanFile, CMake, tools
import os


class PROJConan(ConanFile):
    name = "proj"
    version = "6.2.1"
    license = "MIT"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    description = "PROJ Library."

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/OSGeo/PROJ.git", self.version)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):

        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)