// Project includes
#include "console.h"
#include "server.h"
#include "settings.h"

// Server global variables
server_network conf;

int main(int argc, char **argv) {

    signal(SIGINT, shutdown);

    /*TODO: Handle multiple servers online (the next server must not try to create a new ipcs queue)*/
    conf.queue_id = msgget(NETWORK_KEY, IPC_CREAT | 0x1FF);
    if(conf.queue_id < 0) {
        error("[Server %d]: Could not open server connection. Aborting...\n");
        exit(IPC_QUEUE_CREAT_ERR);
    }

    sqlite3_open(DB_LOCATION, &conf.db_conn);
    configure_server_db(&conf.db_conn);


    message("TR1-Chat v." VERSION "\nServer is now running...\nPress Ctrl-C to stop\n");
    while(1){
        // Handle requests
    }

}

void shutdown() {
    message("\nStop signal received. Stopping...\n");
    free(conf.connected_clients);
    sqlite3_close(conf.db_conn);
    if(msgctl(conf.queue_id, IPC_RMID, NULL) < 0) {
        warning("[Server %d]: Could not close server connection, leaving queue open.\n");
        exit(IPC_QUEUE_RMID_ERR);
    }
    message("Goodbye.\n");
    exit(SUCCESS);
}

void configure_server_db(sqlite3** conn){
    const char *sql[6] = {"CREATE TABLE IF NOT EXISTS `messages` (\n"
                          "\t`id_message`\tINTEGER NOT NULL,\n"
                          "\t`id_user`\tINTEGER NOT NULL,\n"
                          "\t`id_room`\tINTEGER NOT NULL,\n"
                          "\t`message_text`\tTEXT NOT NULL,\n"
                          "\t`created_at`\tDATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\n"
                          "\tPRIMARY KEY(`id_message`),\n"
                          "\tFOREIGN KEY(`id_user`) REFERENCES `users`(`id_user`),\n"
                          "\tFOREIGN KEY(`id_room`) REFERENCES `rooms`(`id_room`)\n"
                          ");",

                          "CREATE TABLE IF NOT EXISTS `rooms` (\n"
                          "\t`id_room`\tINTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\n"
                          "\t`room_name`\tVARCHAR ( 255 ) NOT NULL,\n"
                          "\t`no_connected`\tINTEGER DEFAULT 0\n"
                          ");",

                          "CREATE TABLE IF NOT EXISTS `rooms_users` (\n"
                          "\t`id_room`\tINTEGER NOT NULL,\n"
                          "\t`id_user`\tINTEGER NOT NULL,\n"
                          "\tFOREIGN KEY(`id_room`) REFERENCES `rooms`(`id_room`) ON DELETE CASCADE,\n"
                          "\tFOREIGN KEY(`id_user`) REFERENCES `users`(`id_user`),\n"
                          "\tPRIMARY KEY(`id_room`,`id_user`)\n"
                          ");",

                          "CREATE TABLE IF NOT EXISTS `users` (\n"
                          "\t`username`\tVARCHAR ( 64 ) NOT NULL UNIQUE,\n"
                          "\t`password`\tINTEGER NOT NULL,\n"
                          "\t`display_name`\tVARCHAR ( 25 ) NOT NULL UNIQUE,\n"
                          "\t`id_user`\tINTEGER NOT NULL,\n"
                          "\tPRIMARY KEY(`id_user`)\n"
                          ");",

                          "CREATE TRIGGER IF NOT EXISTS decr_room AFTER DELETE ON rooms_users BEGIN"
                          "\tUPDATE rooms SET no_connected = no_connected - 1 WHERE id_room = OLD.id_room; END",

                          "CREATE TRIGGER IF NOT EXISTS incr_room AFTER INSERT ON rooms_users BEGIN"
                          "\tUPDATE rooms SET no_connected = no_connected + 1 WHERE id_room = NEW.id_room; END"
                          };

    for (int i = 0; i < 6; ++i)
        sqlite3_exec(*conn, sql[i], NULL, NULL, NULL);

}

