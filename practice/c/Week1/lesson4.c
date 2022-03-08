#include <stdio.h>

// this function takes a double n and returns n multiplied by itself 
int my_function(double n){
    double n2 = n*n;
    return n2;
}

int main(void) {
    int value = 42;
    double processed_value = my_function(value);
    printf("The initial value was %d", value); 
    printf(" and the processed value is %f\n", processed_value);
    return 0;
}