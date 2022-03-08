#include <stdio.h>

struct Date {
	int day;
	char month[4];
	int year;
};

void printDate(struct Date d){
    if (d.day < 10) {
        printf("0%d:%s:%d", d.day, d.month, d.year);
    } else {
        printf("%d:%s:%d", d.day, d.month, d.year);
    }

}

int main(void) {
    struct Date date1;
    date1.day = 1;
    date1.month[0] = 'J';
    date1.month[1] = 'A';
    date1.month[2] = 'N';
    date1.month[3] = '\0';
    date1.year = 2019;
    printDate(date1);
    return 0;
}