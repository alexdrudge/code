#include <stdio.h>

void printHelloWorld(void);
void printXTenTimes(void);
void convertMetricToImperialHeights(void);
void fibonacci(void);
void volumeOfACylinder(void);

int main(void) {
    printf("Question 1\n");
    printHelloWorld();

    printf("\nQuestion 2\n");
    printXTenTimes();

    printf("\nQuestion 3\n");
    convertMetricToImperialHeights();

    printf("\nQuestion 4\n");
    fibonacci();
 
    printf("\nQuestion 5\n");
    volumeOfACylinder();
    return 0;
}

/* 
 * Lab Sheet 1:
 */

 /* Question 1: 
 
 Adapt the “HelloWorld” code below to produce a program that defines a variable capable of holding an integer of your choice. The program should add 3 to that number, multiply the result by 2, subtract 4, subtract twice the original number, add 3, then print the result and a new line.
 */
 
void printHelloWorld(void){
    printf("Hello World\n");
    int num = 1;
    num = (num + 3) * 2 - 4 - num * 2 + 3;
    printf("The number is: %d\n", num);
}

 /* Question 2: 
 
 Complete the function below so that it prints every integer from x to x + 10.  Do not use loops. 
 
 Call this function from the main to test your program.
 */

void printXTenTimes(void){
    int x = 5;
    printf("%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d\n", x, x+1, x+2, x+3, x+4, x+5, x+6, x+7, x+8, x+9, x+10);
}

 /* Question 3: 
 
 Complete the function below so that it converts the height of a person from centimetres to feet and inches. Use integer division (rounding down is acceptable, which is the default for integer division). 
 
 Hint: 254 cm is exactly 100 inches and 12 inches is exactly 1 foot. 
 
 Call this function from the main to test your program.  For example you could test your program with the follow five values, where "?" replaced with the true value.

 101 cm is 3 feet 3 inches to the nearest inch.
 3 cm is 0 feet 1 inches to the nearest inch.
 15 cm is ? feet ? inches to the nearest inch.
 192 cm is ? feet ? inches to the nearest inch.
 124 cm is ? feet ? inches to the nearest inch.
 */

void convertMetricToImperialHeights(void){
    int cm = 173;
    int inch = cm * 100 / 254;
    int feet = inch / 12;
    inch = inch - 12 * feet;
    printf("%dcm is %dft and %din\n", cm, feet, inch);
}

 /* Question 4: 
 
 Complete the function below so that it uses three variables (current, previous, next) to calculate and print out the first ten numbers of the Fibonacci sequence, each on a new line: i.e. the first four lines should be as follows:

 0 
 1 
 1 
 2
 
 Call this function from the main to test your program.
 */

void fibonacci(void){
    int current = 1;
    int previous = 0;
    int next = 1;
    printf("%d\n%d\n%d\n", previous, current, next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
    previous = current;
    current = next;
    next = previous + current;
    printf("%d\n", next);
 }

 /* Question 5: 
 
 Complete the function below so that it uses two variables: height and radius. Use these two variables and print to the screen, the volume of a cylinder. 

 Call this function from the main to test your program.  For example, you could test your program with the following values, 

 height 7.0cm and radius 4.0cm
 height 20.0cm and radius 3.0cm
 height 14.7cm and radius 5.2cm
 
 Which print out, the cylinder with height 7.0cm and radius 4.0cm has a volume of 351.86cm^3
 
*/

void volumeOfACylinder(void){
    #include <math.h>
    double height = 14.7;
    double radius = 5.2;
    double pi = acos(-1);
    double volume = radius * radius * height * pi;
    printf("Volume of a sphere with height %f and radius %f is %f", height, radius, volume);
}