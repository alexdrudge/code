/*==============================================================================
  Run-length Encoding - Decoder
  Principles of Programming 2 Week Two Lab Exercise
==============================================================================*/

#include <stdio.h>
#include <string.h>
#include <stdbool.h> // We can use this to help simplify our boolean expressions
#include <ctype.h> // TIP: This is a clue - what can this library give us that could be useful?

void decode(char input[]) {

    char output[100] = {'\0'}; // This is where you should store your output

    int i = 0;
    int count[5] = {0, 0, 0, 0, 0};
    int j = 0;
    int total = 0;

    while (input[i]){
        if (isalpha(input[i])){
            // convert count[] into total
            for (int k=0; k<5; k++){
                if (count[k]){
                    total = total * 10 + count[k];
                }
            }
            // add char to output total times
            for (int k=0; k<total; k++){
                sprintf(output, "%s%c", output, input[i]);
            }
            // reset count[]
            for (int k=0; k<5; k++){
                count[k] = 0;
            }
            // reset other variables
            total = 0;
            j = 0;
        } else {
            count[j] = input[i] - '0';
            j++;
        }
        i++;
    }
    
    printf("Input: %s, Output: %s\n",input, output);
}


int main(void){
    char input[] = "14A3B2C1D2A";
    decode(input);
    return 0;
}