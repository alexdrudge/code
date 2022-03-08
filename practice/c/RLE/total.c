#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int sum_values(int* array, int num){
	int val;
	
	for(int i = 0; i <= num; i++){
		val += array[i];
	}
	
	return val;
}	

int main(int argc, char** argv)
{
	int values[10];
	int length = 10;
	int sum = 0;
	
	for (int i = 0; i < 10; i++){
		values[i] = i + 1;		
	}
	
	sum = sum_values(values, length);
	printf("Total sum is %d\n", sum);
	
	return 0;
}