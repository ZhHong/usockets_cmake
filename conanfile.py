from   conans       import ConanFile, CMake, tools
from   conans.tools import download, unzip
import os

class Project(ConanFile):
    name            = "uSockets"
    description     = "Conan package for uSockets."
    version         = "0.1.2"                
    url             = "https://github.com/uNetworking/uSockets"
    cmake_name      = "usockets_cmake"
    cmake_version   = "1.0.0"                
    cmake_url       = "https://github.com/acdemiralp/usockets_cmake"
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "cmake"
    options         = {"use_libuv"  : [True, False],
                       "use_openssl": [True, False]} 
    default_options = "use_libuv=False", "use_openssl=True"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.use_libuv = True # The only option on Windows.
    
    def requirements(self):
        if self.options.use_libuv:
            self.requires("libuv/1.27.0@bincrafters/stable")

        if self.options.use_openssl:
            self.requires("OpenSSL/latest_1.1.1x@conan/stable")
    
    def imports(self):
       self.copy("*.dylib*", dst="", src="lib")
       self.copy("*.dll"   , dst="", src="bin")

    def source(self):
        zip_name = "v%s.zip" % self.version
        download ("%s/archive/%s" % (self.url, zip_name), zip_name, verify=False)
        unzip    (zip_name)
        os.unlink(zip_name)

        zip_name   = "%s.zip" % self.cmake_version
        download   ("%s/archive/%s" % (self.cmake_url, zip_name), zip_name, verify=False)
        unzip      (zip_name)
        os.unlink  (zip_name)
        copy_tree  (("%s-%s" % (self.cmake_name, self.cmake_version)), ("%s-%s" % (self.name, self.version)))

    def build(self):
        cmake           = CMake(self)
        libuv_options   = "-DUSE_LIBUV=ON" if self.options.use_libuv else "-DUSE_LIBUV=OFF"
        openssl_options = "-DUSE_OPENSSL=ON" if self.options.use_openssl else "-DUSE_OPENSSL=OFF"
        self.run("cmake %s-%s %s %s %s" % (self.name, self.version, cmake.command_line, libuv_options, openssl_options))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        include_folder = "%s-%s/src" % (self.name, self.version)
        self.copy("*.h"     , dst="include", src=include_folder)
        self.copy("*.hpp"   , dst="include", src=include_folder)
        self.copy("*.inl"   , dst="include", src=include_folder)
        self.copy("*.dylib*", dst="lib"    , keep_path=False   )
        self.copy("*.lib"   , dst="lib"    , keep_path=False   )
        self.copy("*.so*"   , dst="lib"    , keep_path=False   )
        self.copy("*.dll"   , dst="bin"    , keep_path=False   )

    def package_info(self):
        self.cpp_info.libs = [self.name]
