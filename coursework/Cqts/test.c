#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

int main(void){
    int key_length = 7;
    int message_length = 23;
    printf("%d, %d, %d", key_length, message_length, message_length / key_length);
    return 0;
}