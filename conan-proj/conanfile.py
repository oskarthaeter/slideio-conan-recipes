from conans import ConanFile, CMake, tools
import os


class PROJConan(ConanFile):
    name = "proj"
    version = "6.2.1"
    license = "MIT"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    description = "PROJ Library."
    requires =  "sqlite3/3.29.0"
    default_options = "sqlite3:shared=False"
    def source(self):
        git = tools.Git()
        git.clone("https://github.com/OSGeo/PROJ.git", self.version)
        libproj_cmake_path = os.path.join(self.source_folder, "src", "lib_proj.cmake")
        if self.settings.os != "Windows":
            tools.replace_in_file(libproj_cmake_path,
                "target_link_libraries(${PROJ_CORE_TARGET} ${SQLITE3_LIBRARY})",
                "target_link_libraries(${PROJ_CORE_TARGET} ${SQLITE3_LIBRARY} ${CMAKE_DL_LIBS})")
    def configure_cmake(self):
        cmake = CMake(self)
        lib_suff = '.lib'
        lib_pref = ''
        if self.settings.os=='Linux':
            lib_suff = '.a'
            lib_pref = 'lib'
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = 'ON'
        lib_name = lib_pref + self.deps_cpp_info["sqlite3"].libs[0] + lib_suff
        cmake.definitions['SQLITE3_INCLUDE_DIR'] = self.deps_cpp_info["sqlite3"].include_paths[0]
        cmake.definitions['SQLITE3_LIBRARY'] = os.path.join(self.deps_cpp_info["sqlite3"].lib_paths[0],lib_name)
        cmake.definitions['BUILD_LIBPROJ_SHARED'] = 'OFF'
        cmake.definitions['PROJ_TESTS'] = 'OFF'
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
