#ifndef TR1_SIMULADOR_CHAT_SERVER_H
#define TR1_SIMULADOR_CHAT_SERVER_H

#include "settings.h"

#define VERSION     "0.0.1"
#define DB_LOCATION "../db/server"

#define NETWORK_KEY 0x8166

typedef struct server_network {
    sqlite3* db_conn;
    long *connected_clients;
    int queue_id;
}server_network;




void configure_server_db(sqlite3** conn);
void shutdown();

#endif //TR1_SIMULADOR_CHAT_SERVER_H
