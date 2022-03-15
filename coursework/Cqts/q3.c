#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

void redact_words(const char *text_filename, const char *redact_words_filename){
    // open the files
    FILE *input, *redact;
    input = fopen(text_filename, "r");
    redact = fopen(redact_words_filename, "r");
    if (input == NULL) return;
    if (redact == NULL) return;

    // get the length and text from input file
    fseek(input, 0, SEEK_END);
    int input_length = ftell(input);
    fseek(input, 0, SEEK_SET);
    char input_text[input_length+1];
    if (input_length == 0) return;
    int input_read_length = fread(input_text, 1, input_length, input);
    input_text[input_read_length] = '\0'; // should be input_length

    // get the length and text from redact file
    fseek(redact, 0, SEEK_END);
    int redact_length = ftell(redact);
    fseek(redact, 0, SEEK_SET);
    char redact_text[redact_length + 1];
    if (redact_length == 0) return; // create the empty file before this
    int redact_read_length = fread(redact_text, 1, redact_length, redact);
    redact_text[redact_read_length] = '\0'; // should be redact_length

    // get each item in the list from redact
    // need to remove any spaces that occur
    // also make sure not to redact any new lines
    // something to do with strchr to find where the strings occur
    char redact_text_copy[redact_length + 1];
    strcpy(redact_text_copy, redact_text);
    char *tok_ptr = strtok(redact_text_copy, ",");
    while (tok_ptr != NULL) {
        printf("%s\n", tok_ptr);
        tok_ptr = strtok(NULL, ",");
    }
    printf("%s\n", redact_text);

    // close the files
    fclose(input);
    fclose(redact);
}

int main(void){
    const char *input_file = "input.txt";
    const char *redact_file = "redact.txt";
    redact_words(input_file, redact_file);
    printf("sucess");
    return 0;
}