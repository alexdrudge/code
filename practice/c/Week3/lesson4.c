#include <stdio.h>
#include <string.h>

char string2[11];

void copyAndPrintArray(char string1[]){
    strcpy(string2, string1);
    for (int i=strlen(string2); i>-1; i--) {
        printf("%c\n", string2[i]);
    }
    printf("%s\n", string2);
}

int main(void) {
    char string1[11] = "my message";
    copyAndPrintArray(string1);
    return 0;
}