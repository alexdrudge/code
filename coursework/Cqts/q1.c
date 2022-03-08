#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

// returns how many days are in a month accounting for leap years
int monthLength(int month, int year){
    if (month == 4 || month == 6 || month == 9 || month == 11){
        return 30;
    } else if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12){
        return 31;
    } else if (month == 2){
        if (year % 400 == 0){
            return 29;
        } else if (year % 100 == 0){
            return 28;
        } else if (year % 4 == 0){
            return 29;
        } else{
            return 28;
        }
    }
    return 0;
}

// Returns how many Fridays fell on the fifth of the month during the nineteenth and twentieth centuries (1 Jan 1801 to 31 Dec 2000) given the dates in the question text
int howManyDays() {
    int total = 0;
    int day = 24;
    int month = 3;
    int year = 2002;
    int name = 3; // defines the day of the week mon-sun, 1-7 (2:wed)
    
    while (year >= 1801){
        // check if its the fifth and a friday (5) and before the 21st century
        if (day == 5 && name == 5 && year < 2001){
            total += 1;
        }

        // reverse backwards by a day
        name--;
        if (name == 0) name = 7;
        day--;
        if (day == 0){
            month--;
            if (month == 0){
                month = 12;
                year--;
            }
            day = monthLength(month, year);
        }
    }

    return total;
}

int main(void){
    printf("%d", howManyDays());
    return 0;
}