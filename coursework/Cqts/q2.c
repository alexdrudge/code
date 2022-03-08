#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

int intpow(int x, int y){
    if (y == 0) return 1;
}

void removeDigit(int x, int n, int* a_ptr, int* b_ptr){
    int a, b;
    if (n % 2 == 0){
        a = n / 2;
        b = n / 2;
    } else {
        a = n / 2 + 1;
        b = n / 2;
    }

    int solution = 0;
    int i = 0;
    int power = 1;
    int ap, bp;

    while (!solution){

        if (i){
            i--;
            power *= 10;
        }
        ap = a % (power * 10);
        bp = b % (power * 10);

        if (ap == x * power || bp == x * power){
            a += power;
            b -= power;
        } else {
            *a_ptr += ap;
            *b_ptr += bp;
            a -= ap;
            b -= bp;
            i++;
        }

        if (a == 0 && b == 0){
            solution = 1;
        }

        printf("%d, %d, %d, %d, %d\n", power, a, b, *a_ptr, *b_ptr);
    }
}

int main(void){
    int a = 0;
    int b = 0;
    int n = 45776;
    int x = 2;
    removeDigit(x, n, &a, &b);
    printf("N=%d and X=%d has solution A=%d and B=%d", n, x, a, b);
    return 0;
}