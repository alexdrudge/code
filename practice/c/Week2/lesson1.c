#include <stdio.h>
#include <math.h>

double pow3(double value){
    return pow(value, 3);
}

double natural(double value) {
    return log(value);
}

int main(void) {
    printf("Hello World\n");
    double result = pow3(3.2);
    double result2 = natural(3.2);
    printf("%f, %f", result, result2);
    return 0;
}