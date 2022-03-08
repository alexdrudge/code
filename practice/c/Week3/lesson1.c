#include <stdio.h>

void printLine(int n, int m) {
    int j;
    for (j=0; j<=m; j++) {
        printf("%d ", j*n);
    }
    printf("\n");
}

void squareMultTable(int n, int m) {
    int i;
    for (i=0; i<=n; i++) {
        printLine(i, m);
    }
}

int main(void) {
    squareMultTable(6, 7);
    return 0;
}
