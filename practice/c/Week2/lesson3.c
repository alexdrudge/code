#include <stdio.h>
#include <stdbool.h>

int mod3(int n);

int main(void) {
    int test = mod3(5);
    printf("%d", test);
    return 0;
}

int mod3(int n) {
    if (((n % 3) == 0) || (n % 5) == 0) {
        return true;
    } else {
        return false;
    }
}