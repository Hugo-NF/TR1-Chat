#ifndef TR1_SIMULADOR_CHAT_SETTINGS_H
#define TR1_SIMULADOR_CHAT_SETTINGS_H

// Compiler includes
#include <sqlite3.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/signal.h>
#include <sys/types.h>


typedef enum return_codes{
    SUCCESS,
    IPC_QUEUE_CREAT_ERR,
    IPC_QUEUE_SEND_ERR,
    IPC_QUEUE_RCV_ERR,
    IPC_QUEUE_RMID_ERR
}return_codes;

typedef enum operation_codes{
    CONNECT,
    CONNECT_ACK,
    CONNECT_NACK,
    JOIN,
    JOIN_ACK,
    JOIN_NACK,
    SEND,
    SEND_ACK,
    SEND_NACK,
    LEAVE,
    LEAVE_ACK,
    LEAVE_NACK,
    DISCONNECT,
    DISCONNECT_ACK,
    DISCONNECT_NACK
}operation_codes;

typedef struct payload_data {
    long uid;
    int operation;
    int error_code;
    /*TODO Pending message body*/
}payload_data;

typedef struct payload{
    long dest;
    payload_data data;
}payload;

unsigned long hash(const char *token);


#endif //TR1_SIMULADOR_CHAT_SETTINGS_H
