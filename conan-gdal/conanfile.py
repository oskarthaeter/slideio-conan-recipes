from conans import ConanFile, tools, VisualStudioBuildEnvironment
import os


class GDALConanFile(ConanFile):
    name = "gdal"
    version = "3.0.2"
    license = "MIT"
    generators = "visual_studio_multi"
    settings = "os", "arch", "compiler", "build_type"
    description = "GDAL Library."
    short_paths = True
    requires =  "sqlite3/3.29.0@bincrafters/stable", \
                "proj/6.2.1@local/stable", \
                "jasper/2.0.14@conan/stable", \
                "libjpeg/9c@bincrafters/stable", \
                "libtiff/4.0.10@local/stable"

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/OSGeo/gdal.git", "v{0}".format(self.version))
    def build(self):
        if self.settings.os == 'Windows':
            env_build = VisualStudioBuildEnvironment(self)
            vars = env_build.vars
            # proj library
            vars['PROJ_INCLUDE'] = self.deps_cpp_info["proj"].include_paths[0]
            vars['PROJ_LIBRARY'] = os.path.join(self.deps_cpp_info["proj"].lib_paths[0],
                self.deps_cpp_info["proj"].libs[0]+'.lib')
            # sqlite3 library
            vars['SQLITE_LIB'] = os.path.join(self.deps_cpp_info["sqlite3"].lib_paths[0],
                self.deps_cpp_info["sqlite3"].libs[0]+'.lib')
            # jasper jpeg2000 library
            vars['JASPER_DIR'] =  self.deps_cpp_info["jasper"].rootpath
            vars['JASPER_INCLUDE'] =  self.deps_cpp_info["jasper"].include_paths[0]
            vars['JASPER_LIB'] =  os.path.join(self.deps_cpp_info["jasper"].lib_paths[0],
                self.deps_cpp_info["jasper"].libs[0]+'.lib')
            # jpeg lib
            vars['JPEG_EXTERNAL_LIB'] =  "1"
            vars['JPEGDIR'] =  self.deps_cpp_info["libjpeg"].rootpath
            vars['JPEG_LIB'] =  os.path.join(self.deps_cpp_info["libjpeg"].lib_paths[0],
                self.deps_cpp_info["libjpeg"].libs[0]+'.lib')
            # libtif
            vars['TIFF_OPTS'] =  "-DBIGTIFF_SUPPORT"
            vars['TIFF_INC'] =  self.deps_cpp_info["libtiff"].include_paths[0]
            vars['TIFF_LIB'] =  os.path.join(self.deps_cpp_info["libtiff"].lib_paths[0],
                self.deps_cpp_info["libtiff"].libs[0]+'.lib')

            build_folder = os.path.join(self.build_folder,'build')
            vars['GDAL_HOME'] = build_folder
            vars['DLLBUILD'] = '0'
            if self.settings.build_type=='Debug':
                vars['DEBUG'] = '1'
            with tools.environment_append(vars):
                vcvars = tools.vcvars_command(self.settings)
                command = ('%s && cd gdal '
                            '&& mkdir %s '
                            '&& nmake /NOLOGO /f makefile.vc WIN64=yes '
                            '&& nmake /NOLOGO /f makefile.vc WIN64=yes devinstall '
                            '&&  cd ..') 
                self.run(command % (vcvars, build_folder))
    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["gdal"]
        self.cpp_info.libdirs = ["lib"]

    def package(self):
        self.copy("*", dst="include/gdal", src="build/include")
        self.copy("*.h", dst="include/gdal/port", src="gdal/port")
        self.copy("*.cpp", dst="include/gdal/port", src="gdal/port")
        self.copy("*", dst="lib", src="build/lib", keep_path=False)