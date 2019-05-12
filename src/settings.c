#include "settings.h"

unsigned long hash(const char *token){
    int weight = 1;
    unsigned long value = 0;
    for(int i = 0; i < strlen(token); i++, weight++)
        value += token[i] * weight;

    return value;
}


