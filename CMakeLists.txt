cmake_minimum_required(VERSION 3.20)
project(kinet-gpu-rt VERSION 0.1.1 LANGUAGES CXX)

# kinet-gpu-rt builds ONLY a static core library (C++23 abstract GPU runtime).
# This is linked into kinet-accel, not used directly by consumers.
#
# Renamed from `kinet-gpu` (v0.1.0): the CMake project namespace `kinet-gpu`
# is now reserved for the MLX-fork at ~/work/kinet/gpu (Identity C).
# Header namespace `kinet::gpu` is unchanged for API stability.

add_library(kinet_gpu_rt STATIC
  src/context.cpp
  src/device.cpp
  src/buffer.cpp
  src/kernel.cpp
  src/registry.cpp
)

# Alias for internal use
add_library(kinet::gpu-rt ALIAS kinet_gpu_rt)

target_compile_features(kinet_gpu_rt PUBLIC cxx_std_23)

target_include_directories(kinet_gpu_rt
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# PIC required since this will be linked into shared library
set_target_properties(kinet_gpu_rt PROPERTIES
  POSITION_INDEPENDENT_CODE ON
  CXX_VISIBILITY_PRESET hidden
  VISIBILITY_INLINES_HIDDEN ON
)

# Platform-specific libraries for dlopen
if(UNIX AND NOT APPLE)
  target_link_libraries(kinet_gpu_rt PRIVATE dl)
endif()

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# Install static library (for C++ consumers who want to build their own accel)
install(TARGETS kinet_gpu_rt
  EXPORT kinet-gpu-rt-targets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(EXPORT kinet-gpu-rt-targets
  NAMESPACE kinet::
  FILE kinet-gpu-rtTargets.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/kinet-gpu-rt
)

configure_package_config_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/kinet-gpu-rtConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/kinet-gpu-rtConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/kinet-gpu-rt
)

write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/kinet-gpu-rtConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY ExactVersion
)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/kinet-gpu-rtConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/kinet-gpu-rtConfigVersion.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/kinet-gpu-rt
)
