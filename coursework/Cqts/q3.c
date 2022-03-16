#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

void redact_words(const char *text_filename, const char *redact_words_filename){
    // open the files
    FILE *input, *redact, *output;
    output = fopen("result.txt", "w");
    if (output == NULL) return;
    input = fopen(text_filename, "r");
    if (input == NULL){
        fclose(output);
        return;
    }
    redact = fopen(redact_words_filename, "r");
    if (redact == NULL){
        fclose(output);
        fclose(input);
        return;
    }

    // get the length and text from input file
    fseek(input, 0, SEEK_END);
    int input_length = ftell(input);
    fseek(input, 0, SEEK_SET);
    char input_text[input_length+1];
    if (input_length == 0){
        fclose(input);
        fclose(redact);
        fclose(output);
        return;
    }
    int input_read_length = fread(input_text, 1, input_length, input);
    input_text[input_read_length] = '\0';
    // create a copy with only lowercase
    char input_text_lower[input_length+1];
    for (int i=0;i<input_length+1;i++) input_text_lower[i] = tolower(input_text[i]);

    // get the length and text from redact file
    fseek(redact, 0, SEEK_END);
    int redact_length = ftell(redact);
    fseek(redact, 0, SEEK_SET);
    char redact_text[redact_length + 1];
    if (redact_length == 0){
        fputs(input_text, output); // EOF would be a return anyway
        fclose(input);
        fclose(redact);
        fclose(output);
        return;
    }
    int redact_read_length = fread(redact_text, 1, redact_length, redact);
    redact_text[redact_read_length] = '\0';
    // remove spaces and \n from the redact words
    for (int i=0;i<redact_length;i++){
        if (redact_text[i] == ' '){
            for (int j=i;j<redact_length;j++) redact_text[j] = redact_text[j+1];
            redact_length--;
            i--;
        } else if (redact_text[i] == '\n'){
            redact_text[i] = ',';
        }
    }

    // find any replace the occurances
    // strtok seperates the words in the redact file
    // strstr finds where these words appear in the input
    char *tok_ptr = strtok(redact_text, ",");
    while (tok_ptr != NULL) {
        int tok_length = strlen(tok_ptr);
        char *inp_ptr = strstr(input_text_lower, tok_ptr);
        while (inp_ptr != NULL){
            if (!isalnum(inp_ptr[tok_length]) && (!isalnum(inp_ptr[-1]) || inp_ptr == input_text_lower)){
                for (int i=0;i<tok_length;i++){
                    inp_ptr[i] = '*';
                }
            }
            inp_ptr = strstr(inp_ptr+1, tok_ptr);
        }
        tok_ptr = strtok(NULL, ",");
    }

    // apply the stars to the non-lowered input
    for (int i=0;i<input_length+1;i++){
        if (input_text_lower[i] == '*') input_text[i] = '*';
    }
    fputs(input_text, output);

    // close the files
    fclose(input);
    fclose(redact);
    fclose(output);
}

int main(void){
    const char *input_file = "input.txt";
    const char *redact_file = "words.txt";
    redact_words(input_file, redact_file);
    printf("success");
    return 0;
}