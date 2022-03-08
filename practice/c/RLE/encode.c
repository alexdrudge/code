/*==============================================================================
  Run-length Encoding - Encoder
  Principles of Programming 2 Week Two Lab Exercise
==============================================================================*/

#include <stdio.h>
#include <string.h>

void encode(char input[]) {

    char output[100]; // This is where you should store your output

    int count = 1;
    int i = 1;
    char previous = input[0];
    
    while (input[i]){
        if (input[i] == previous){
            count += 1;
        } else {
            sprintf(output, "%s%d%c", output, count, previous);
            count = 1;
        }
        previous = input[i];
        i++;
    }
    sprintf(output, "%s%d%c", output, count, previous);

    printf("Input: %s Output: %s \n", input, output);
}

int main(void){
    char input[] = "OOOGGGGKKKBBBBBBBNN::";
    encode(input);
    return 0;
}