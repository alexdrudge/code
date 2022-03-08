#include <stdio.h>

int multiply(int number, int by){
    if (by < 1) {
        return number;
    } else {
        return number + multiply(number, by - 1);
    }
}

int main(void) {
    printf("The multiplication of 2 by 3 is %d\n", multiply(2,3));
    return 0;
}