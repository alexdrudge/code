#include <stdio.h>

int evenNumbersSize = 10;
int evenNumbers[10];

void populateArray(){
    for(int i=0; i<evenNumbersSize; i++){
        evenNumbers[i] = (i+1)*2;
    }
}

void printArray() {
    for(int i=0; i<evenNumbersSize; i++){
        printf("%d ", evenNumbers[i]);
    }
}

int main(void) {
    populateArray();
    printArray();
    return 0;
}