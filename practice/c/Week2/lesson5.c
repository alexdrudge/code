#include <stdio.h>

int fibonacci(int term) {
    if (term == 0) {
        return 0;
    } else if (term == 1) {
        return 1;
    } else if (term == 2) {
        return 1;
    } else {
        int num = 0;
        int num2 = 1;
        int num3 = 1;
        int n;
        for (n=0; n <= term-3; n++) {
            num = num2;
            num2 = num3;
            num3 = num + num2;
        }
        return num3;
    }
}

int main(void) {
    printf("Hello World\n");
    int result = fibonacci(4);
    printf("%d", result);
    return 0;
}