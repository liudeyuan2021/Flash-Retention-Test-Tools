cmake_minimum_required (VERSION 3.2)
project(retention)

add_executable(diff_bit_log
    # Source code files
    cpp/diff_bit_log.cpp
)

add_executable(check_data
    # Source code files
    cpp/check_data.cpp
)