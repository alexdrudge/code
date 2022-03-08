#include <stdio.h>

void printCharsInString(char string[]){
    int i = 0;
    while (string[i] != '\0'){
        printf("%c\n", string[i]);
        i++;
    }
}

int main(void) {
    char my_string[] = "This is a string";
    printCharsInString(my_string);
    return 0;
}