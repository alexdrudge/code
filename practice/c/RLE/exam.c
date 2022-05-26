#include <stdio.h>

void function(int a) {
    int *b;
    b = &a;
    *b += 1;
    printf("%d", *b);
    printf("%d", a);
    return;
}

int main (void) {
    int num = 5;
    function(num);
    printf("%d", num);
    return 0;
}