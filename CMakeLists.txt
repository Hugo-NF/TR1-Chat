cmake_minimum_required(VERSION 3.10)
project(TR1-Simulador_Chat C)

set(CMAKE_C_STANDARD 99)


include_directories(include)

set(SERVER_SOURCES src/server.c src/settings.c)
set(CLIENT_SOURCES src/client.c src/settings.c)

add_executable(server ${SERVER_SOURCES})
target_link_libraries(server sqlite3)

add_executable(client ${CLIENT_SOURCES})
target_link_libraries(server sqlite3)
