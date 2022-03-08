#include <stdio.h>
#include <math.h>
#include <string.h>

  /* 
  * Lab Sheet 3
  */

  /* Question 1
  
  Complete the function below which converts a hexadecimal string into its decimal value. (Do not use a C standard library function.) 

  The main function calls this function with an example hexadecimal value. Change this value to test your program.
  */

int calcValue(int mult, int power) {
  return mult * pow(16, power);
}

int hexToDec(char hex[]){
  int power = 0;
  int total = 0;
  int length = strlen(hex) - 1;
  for (length; length > -1; length--) {
    if (hex[length] == '0') {
      total += calcValue(0, power);
    } else if (hex[length] == '1') {
      total += calcValue(1, power);
    } else if (hex[length] == '2') {
      total += calcValue(2, power);
    } else if (hex[length] == '3') {
      total += calcValue(3, power);
    } else if (hex[length] == '4') {
      total += calcValue(4, power);
    } else if (hex[length] == '5') {
      total += calcValue(5, power);
    } else if (hex[length] == '6') {
      total += calcValue(6, power);
    } else if (hex[length] == '7') {
      total += calcValue(7, power);
    } else if (hex[length] == '8') {
      total += calcValue(8, power);
    } else if (hex[length] == '9') {
      total += calcValue(9, power);
    } else if (hex[length] == 'A') {
      total += calcValue(10, power);
    } else if (hex[length] == 'B') {
      total += calcValue(11, power);
    } else if (hex[length] == 'C') {
      total += calcValue(12, power);
    } else if (hex[length] == 'D') {
      total += calcValue(13, power);
    } else if (hex[length] == 'E') {
      total += calcValue(14, power);
    } else if (hex[length] == 'F') {
      total += calcValue(15, power);
    }
    power++;
  }
  return total;
}

/* Question 2
 Complete the function below that print out a tree shape such as the following: 

    *
   ***
  *****
 *******
*********
   ***
   ***
   ***
   ***

  Note you can (and probably should) implement additional functions to help.

  You can assume that the width of the tree will be odd and hence every line will have an odd number of asterisks. The trunk will always have a width of three.

  Call this function from the main to test your program.
*/


void printTrunk(int width, int trunkLength, int stars){
  int gap = (width - stars) / 2;
  for (int i=0;i<trunkLength;i++){
    for (int j=0;j<gap;j++){
      printf(" ");
    }
    for (int j=0;j<stars;j++){
      printf("*");
    }
    printf("\n");
  }
}

void printBranches(int width){
  int length = (width + 1) / 2;
  for (int i=0; i<length;i++){
    int stars = 2*i + 1;
    printTrunk(width, 1, stars);
  }
}

void printTree(int width, int trunkLength){
  printBranches(width);
  printTrunk(width, trunkLength, 3);
}

int main(void) {
  char hex[4] = "FF3";
  printf("The hex value %s is %d in decimal\n", hex, hexToDec(hex));

  printTree(9, 2);
  return 0;
}