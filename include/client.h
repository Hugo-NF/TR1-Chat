#ifndef TR1_SIMULADOR_CHAT_CLIENT_H
#define TR1_SIMULADOR_CHAT_CLIENT_H

#include "settings.h"

typedef struct client_network{
    sqlite3* db_conn;
    int connected_server;
}client_network;

#endif //TR1_SIMULADOR_CHAT_CLIENT_H
