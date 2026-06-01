from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout


class KinetGpuRt(ConanFile):
    name = "kinet-gpu-rt"
    package_type = "static-library"  # Always static - linked into kinet-accel
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}

    exports_sources = "CMakeLists.txt", "cmake/*", "include/*", "src/*", "LICENSE*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", self.name)
        self.cpp_info.set_property("cmake_target_name", "kinet::gpu-rt")
        self.cpp_info.set_property("cmake_find_mode", "config")
        self.cpp_info.libs = ["kinet_gpu_rt"]

        # Platform libs for dlopen
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["dl"]
