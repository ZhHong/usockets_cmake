##################################################    Project     ##################################################
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
project               (uSockets VERSION 0.1.2 LANGUAGES CXX)
list                  (APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
set_property          (GLOBAL PROPERTY USE_FOLDERS ON)
set                   (CMAKE_CXX_STANDARD 17)
set                   (CMAKE_CXX_VISIBILITY_PRESET hidden)
set                   (CMAKE_VISIBILITY_INLINES_HIDDEN 1)

##################################################    Options     ##################################################
option(USE_LIBUV "Use libuv." OFF)
option(USE_OPENSSL "Use OpenSSL." ON)

##################################################    Sources     ##################################################
file(GLOB_RECURSE PROJECT_HEADERS src/*.h src/*.hpp)
file(GLOB_RECURSE PROJECT_SOURCES src/*.c src/*.cpp)
set (PROJECT_FILES ${PROJECT_HEADERS} ${PROJECT_SOURCES})

##################################################  Dependencies  ##################################################
include(conan)
include(conan_utility)

add_conan_remote(bincrafter      https://api.bintray.com/conan/bincrafters/public-conan)
add_conan_remote(conan-community https://api.bintray.com/conan/conan-community/conan   )

conan_cmake_run(CONANFILE conanfile.py BASIC_SETUP BUILD missing)
list           (APPEND PROJECT_INCLUDE_DIRS ${CONAN_INCLUDE_DIRS_RELEASE})
list           (APPEND PROJECT_COMPILE_DEFINITIONS ${CONAN_COMPILE_DEFINITIONS_RELEASE})
foreach        (_LIB ${CONAN_LIBS_DEBUG})
  list         (APPEND PROJECT_LIBRARIES debug ${_LIB})
endforeach     ()  
foreach        (_LIB ${CONAN_LIBS_RELEASE})
  list         (APPEND PROJECT_LIBRARIES optimized ${_LIB})
endforeach     ()

##################################################  Definitions   ##################################################
set(BUILD_SHARED_LIBS OFF)

if    (USE_LIBUV)
  list(APPEND PROJECT_COMPILE_DEFINITIONS LIBUS_USE_LIBUV)
else  ()
  list(APPEND PROJECT_COMPILE_DEFINITIONS LIBUS_USE_EPOLL)
endif ()

if    (USE_OPENSSL)
  list(APPEND PROJECT_COMPILE_DEFINITIONS LIBUS_USE_OPENSSL)
else  ()
  list(APPEND PROJECT_COMPILE_DEFINITIONS LIBUS_NO_SSL)
endif ()

##################################################    Targets     ##################################################
add_library(${PROJECT_NAME} ${PROJECT_FILES})
target_include_directories(${PROJECT_NAME} PUBLIC 
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
  $<INSTALL_INTERFACE:src> PRIVATE source)
target_include_directories(${PROJECT_NAME} PUBLIC ${PROJECT_INCLUDE_DIRS})
target_link_libraries     (${PROJECT_NAME} PUBLIC ${PROJECT_LIBRARIES})
target_compile_definitions(${PROJECT_NAME} PUBLIC ${PROJECT_COMPILE_DEFINITIONS})
set_target_properties     (${PROJECT_NAME} PROPERTIES LINKER_LANGUAGE CXX)

##################################################  Installation  ##################################################
install(TARGETS ${PROJECT_NAME} EXPORT ${PROJECT_NAME}-config
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)
install(EXPORT  ${PROJECT_NAME}-config DESTINATION cmake)
export (TARGETS ${PROJECT_NAME}        FILE        ${PROJECT_NAME}-config.cmake)
