from conans import ConanFile, CMake, tools
import os


class libCZIConan(ConanFile):
    name = "libCZI"
    version = "master"
    license = "MIT"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    description = "CZI Library."
    source_folder = "source_dir"
    build_folder = "build_dir"

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/zeiss-microscopy/libCZI.git", self.version)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        build_type_name = str(self.settings.build_type)
        lib_src = "Src/libCZI/" + build_type_name
        self.copy("libCZI*.h", dst="include/libCZI", src="Src/libCZI")
        self.copy("libCZIStatic.*", dst="lib", src=lib_src, keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["libCZIStatic"]
        self.cpp_info.libdirs = ["lib"]