#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

void removeDigit(int x, int n, int* a_ptr, int* b_ptr){
    *a_ptr = 0;
    *b_ptr = 0;
    // validate the inputs
    if (!(x <= 9 && x >= 0)) return;
    if (!(n <= 100000000 && n >= 10)) return;
    
    // take the midpoints of both numbers
    // a could be one more than b
    int a, b;
    if (n % 2 == 0){
        a = n / 2;
        b = n / 2;
    } else {
        a = n / 2 + 1;
        b = n / 2;
    }

    bool solution = false;
    bool different = false;
    int power = 1; // the current place being checked
    int ap, bp; // the extracted digit from that place

    while (!solution){
        // move to the next place up
        if (different){
            different = false;
            power *= 10;
        }

        // get the digit in the place
        ap = a % (power * 10);
        bp = b % (power * 10);

        // change digits if one is the same
        if ((ap == x * power && a != 0) || (bp == x * power && b != 0)){
            a += power;
            b -= power;
        } else {
            *a_ptr += ap;
            *b_ptr += bp;
            a -= ap;
            b -= bp;
            different = true;
        }

        // complete when nothing left of the numbers
        if (a == 0 && b == 0){
            solution = true;
        }
    }
}

int main(void){
    int a;
    int b;
    for (int x=0;x<10;x++){
        for (int n=95;n<1005;n++){
            removeDigit(x, n, &a, &b);
            if (a+b != n) printf("ruh roh\n");
        }
    }
    printf("success");
    return 0;
}