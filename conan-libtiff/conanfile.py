#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class LibtiffConan(ConanFile):
    name = "libtiff"
    description = "Library for Tag Image File Format (TIFF)"
    version = "4.0.10"
    url = "http://github.com/bincrafters/conan-tiff"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    homepage = "http://www.simplesystems.org/libtiff"
    exports = ["LICENSE.md"]
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    requires = "zlib/1.2.11@conan/stable", "libjpeg/9c@bincrafters/stable" #, "lzma/5.2.4@bincrafters/stable"

    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("http://download.osgeo.org/libtiff/tiff-{0}.zip".format(self.version))
        os.rename('tiff-' + self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)

        cmake.definitions['CMAKE_INSTALL_LIBDIR'] = 'lib'
        cmake.definitions['CMAKE_INSTALL_BINDIR'] = 'bin'
        cmake.definitions['CMAKE_INSTALL_INCLUDEDIR'] = 'include'

        cmake.definitions["lzma"] = False
        cmake.definitions["jpeg"] = True
        cmake.definitions['ZLIB_INCLUDE_DIR'] =  self.deps_cpp_info["zlib"].include_paths[0]
        cmake.definitions['ZLIB_LIBRARY'] =  os.path.join(self.deps_cpp_info["zlib"].lib_paths[0],
                self.deps_cpp_info["zlib"].libs[0]+'.lib')
#        cmake.definitions['LIBLZMA_INCLUDE_DIR'] =  self.deps_cpp_info["lzma"].include_paths[0]
#        cmake.definitions['LIBLZMA_LIBRARY'] =  os.path.join(self.deps_cpp_info["lzma"].lib_paths[0],
#                self.deps_cpp_info["lzma"].libs[0]+'.lib')
        cmake.definitions['JPEG_INCLUDE_DIR'] =  self.deps_cpp_info["libjpeg"].include_paths[0]
        cmake.definitions['JPEG_LIBRARY'] =  os.path.join(self.deps_cpp_info["libjpeg"].lib_paths[0],
                self.deps_cpp_info["libjpeg"].libs[0]+'.lib')

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("COPYRIGHT", src=self._source_subfolder, dst="licenses", ignore_case=True, keep_path=False)
        shutil.rmtree(os.path.join(self.package_folder, 'share', 'man'), ignore_errors=True)
        shutil.rmtree(os.path.join(self.package_folder, 'share', 'doc'), ignore_errors=True)

        # remove binaries
        for bin_program in ['fax2ps', 'fax2tiff', 'pal2rgb', 'ppm2tiff', 'raw2tiff', 'tiff2bw', 'tiff2pdf',
                            'tiff2ps', 'tiff2rgba', 'tiffcmp', 'tiffcp', 'tiffcrop', 'tiffdither', 'tiffdump',
                            'tiffgt', 'tiffinfo', 'tiffmedian', 'tiffset', 'tiffsplit']:
            for ext in ['', '.exe']:
                try:
                    os.remove(os.path.join(self.package_folder, 'bin', bin_program+ext))
                except:
                    pass

    def package_info(self):
        self.cpp_info.libs = ["tiff", "tiffxx"]
        if self.settings.os == "Windows" and self.settings.build_type == "Debug" and self.settings.compiler == 'Visual Studio':
            self.cpp_info.libs = [lib+'d' for lib in self.cpp_info.libs]
        if self.options.shared and self.settings.os == "Windows" and self.settings.compiler != 'Visual Studio':
            self.cpp_info.libs = [lib+'.dll' for lib in self.cpp_info.libs]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
