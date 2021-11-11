cmake_minimum_required(VERSION 3.5)
project(gazebo)

# Skip if Gazebo not present
find_package(gazebo QUIET)
if(NOT gazebo_FOUND)
  message(WARNING "Gazebo not found, proceeding without that simulator.")
  return()
endif()

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY
    config
    launch
    models
    worlds
  DESTINATION
    share/${PROJECT_NAME}/
)

ament_package()

