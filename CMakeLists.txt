cmake_minimum_required(VERSION 3.10)
project(TR1-Simulador_Chat C)

set(CMAKE_C_STANDARD 99)

add_executable(server include/console.h src/server.c include/server.h)
target_link_libraries(server sqlite3)

add_executable(client include/settings.h include/console.h src/client.c include/client.h)
target_link_libraries(server sqlite3)
