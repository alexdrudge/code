#include <stdio.h>
#include <math.h>

void numberToText(int n);
void lownumsToText(int n);
double calculateDistance(double x1, double y1, double x2, double y2);
void printOddEvenAndOrPrime(int n);

int main(void) {
    printf("Question 1\n");
    numberToText(11);
    printf("\n");
    numberToText(0);
    printf("\n");
    numberToText(100);
    printf("\n");
    numberToText(56);
    printf("\n");
    numberToText(30);
    printf("\n");
    numberToText(99);
    printf("\n");
    numberToText(75);
    printf("\n");
    numberToText(18);
    printf("\n");
    numberToText(10);
    printf("\n");
    numberToText(80);
    printf("\n");
    numberToText(77);
    printf("\n");
    numberToText(69);
    printf("\n");

    printf("\nQuestion 2\n");
    printf("%1.2f\n", calculateDistance(0, 0, 4, 3));
    printf("%1.2f\n", calculateDistance(9, 5, 4, 3));

    printf("\nQuestion 3\n");
    printOddEvenAndOrPrime(0);
    printOddEvenAndOrPrime(1);
    printOddEvenAndOrPrime(2);
    printOddEvenAndOrPrime(3);
    printOddEvenAndOrPrime(4);
    printOddEvenAndOrPrime(5);
    printOddEvenAndOrPrime(6);
    printOddEvenAndOrPrime(7);
    return 0;
}

/* 
 * Lab Sheet 2:
 */

/* Question 1: 
 
 Complete the function below which takes in an integer input between zero and one hundred (0 ≤ n ≤ 100) and prints out the number expressed in English text, with spaces and no dashes (–), e.g. for the number “33”, we would expect to see “thirty three”. Hint: you may want to create additional functions to help.
 
 Call this function from the main to test your program.
 */

void numberToText(int n) {
    if (n == 0) {
        printf("zero");
    } else if (n == 100) {
        printf("one hundered");
    } else if (n == 10) {
        printf("ten");
    } else if (n == 11) {
        printf("eleven");
    } else if (n == 12) {
        printf("twelve");
    } else if (n == 13) {
        printf("thirteen");
    } else if (n == 14) {
        printf("fourteen");
    } else if (n == 15) {
        printf("fiveteen");
    } else if (n == 16) {
        printf("sixteen");
    } else if (n == 17) {
        printf("seventeen");
    } else if (n == 18) {
        printf("eighteen");
    } else if (n == 19) {
        printf("nineteen");
    } else if (n >= 90) {
        printf("ninety ");
        lownumsToText(n-90);
    } else if (n >= 80) {
        printf("eighty ");
        lownumsToText(n-80);
    } else if (n >= 70) {
        printf("seventy ");
        lownumsToText(n-70);
    } else if (n >= 60) {
        printf("sixty ");
        lownumsToText(n-60);
    } else if (n >= 50) {
        printf("fifty ");
        lownumsToText(n-50);
    } else if (n >= 40) {
        printf("fourty ");
        lownumsToText(n-40);
    } else if (n >= 30) {
        printf("thirty ");
        lownumsToText(n-30);
    } else if (n >= 20) {
        printf("twenty ");
        lownumsToText(n-20);
    } else {
        lownumsToText(n);
    }
}

void lownumsToText(int n){
    if (n == 1) {
        printf("one");
    } else if (n == 2) {
        printf("two");
    } else if (n == 3) {
        printf("three");
    } else if (n == 4) {
        printf("four");
    } else if (n == 5) {
        printf("five");
    } else if (n == 6) {
        printf("six");
    } else if (n == 7) {
        printf("seven");
    } else if (n == 8) {
        printf("eight");
    } else if (n == 9) {
        printf("nine");
    }
}

/* Question 2: 
 
 Complete the function below that calculates, and returns, the distance between two points.
 
 Call this function from the main to test your program. Hint: may wish to use the following print statement in your main function, or similar: 

 printf("%1.2f\n", calculateDistance(0, 0, 4, 3));
 */

double calculateDistance(double x1, double y1, double x2, double y2){
    return sqrt(pow(x1-x2,2) + pow(y1-y2,2));
}

/* Question 3: 
 
 Complete the function below that is given an integer, n, where 1 ≤ n ≤ 9999 and prints whether it is even, odd, or/and prime.  The output should be whole sentences for example, 

 1 is odd and not prime.
 2 is even and prime.
 3 is odd and prime.
 4 is even and not prime.
 5 is odd and prime.
 
 Call this function from the main to test your program.
 */

void printOddEvenAndOrPrime(int n){
    printf("%d is ", n);
    if (n % 2 == 0) {
        printf("even and ");
    } else {
        printf("odd and ");
    }
    int prime = 1;
    int i;
    for (i=2; i<=n/2; i++) {
        if (n % i == 0) {
            prime = 0;
        }
    }
    if (n == 1 || n == 0) {
        printf("not prime.\n");
    } else if (prime == 1) {
        printf("prime.\n");
    } else {
        printf("not prime.\n");
    }
}