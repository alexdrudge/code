#include <stdio.h>

int foo(int n);
int m;

int main(void) {
    printf("Hello World\n");
    int n = foo(3);
    printf("%d, %d", n, m);
    return 0;
}

int foo(int n) {
    m = n*n;
    return n*n;
    printf("%d", n*n);
}