#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

/* 
 *  A function which takes in a filename and returns the contents as a string, 
 *  with all non-alphanumeric (i.e., not A-Z, a-z, or 0-9) removed and characters
 *  converted to uppercase.
 */
char *read_string(const char *filename){
    // open the file and get its length and text
    FILE *input;
    input = fopen(filename, "r");
    if (input == NULL) return NULL;
    fseek(input, 0, SEEK_END);
    int input_length = ftell(input);
    fseek(input, 0, SEEK_SET);
    char input_text[input_length+1];
    int input_read_length = fread(input_text, 1, input_length, input);
    input_text[input_read_length] = '\0';

    // filter text into a new string
    char *filtered = (char*) malloc(sizeof(char)*(input_length+1));
    if (filtered == NULL) return filtered;
    int i = 0;
    int j = 0;
    while (input_text[i] != '\0'){
        if (isalnum(input_text[i])){
            filtered[j] = toupper(input_text[i]);
            j++;
        }
        i++;
    }
    filtered[j] = '\0';
    return filtered;
}

/* 
 *  A function which takes in a filename and encrypts the contents using the
 *  key string which is obtained from the "key_filename" file. The encrypted 
 *  message should be returned using the "result" buffer, which you should 
 *  assume has not been initialised or any memory allocated to it.
 */
void encrypt_columnar(const char *message_filename, const char *key_filename, char **result){
    // get plain text and key and lengths
    char *message = read_string(message_filename);
    if (message == NULL) return;
    char *key = read_string(key_filename);
    if (key == NULL){
        free(message);
        return;
    }
    int message_length = strlen(message);
    int key_length = strlen(key);
    if (message_length == 0) return;
    if (key_length == 0) return;

    // construct 2D array
    int rows;
    if (message_length % key_length == 0){
        rows = message_length / key_length + 1;
    } else {
        rows = message_length / key_length + 2;
    }
    char cipher[key_length][rows+1];
    for (int i=0;i<key_length;i++){
        cipher[i][0] = key[i];
        cipher[i][rows] = '\0';
    }
    int l = 0;
    for (int j=1;j<rows;j++){
        for (int i=0;i<key_length;i++){
            if (l >= message_length){
                cipher[i][j] = 'X';
            } else {
                cipher[i][j] = message[l];
            }
            l++;
        }
    }

    // bubble sort to put the key into alphabetical order
    char temp[rows];
    for (int i=0;i<key_length-1;i++){
        for (int j=i+1;j<key_length;j++){
            if (cipher[i][0] > cipher[j][0]){
                strcpy(temp, cipher[i]);
                strcpy(cipher[i], cipher[j]);
                strcpy(cipher[j], temp);
            }
        }
    }

    // store the ciphertext in the buffer
    *result = (char*) malloc(sizeof(char) * key_length * (rows-1) + 1);
    if (*result == NULL){
        free(message);
        free(key);
        return;
    }
    int k = 0;
    for (int j=1;j<rows;j++){
        for (int i=0;i<key_length;i++){
            *(*result + k) = cipher[i][j];
            k++;
        }
    }
    *(*result + k) = '\0';

    free(message);
    free(key);
}

/* 
 *  A function which takes in a string and decrypts the contents using the
 *  key string which is obtained from the "key_filename" file. The decrypted 
 *  message should be returned using the "result" buffer, which you should 
 *  assume has not been initialised or any memory allocated to it. The function 
 *  should return true if decryption was successful, false if not.
 */
int decrypt_columnar(const char *message_filename, const char *key_filename, char **result){
    // get cipher text and key and lengths
    char *message = read_string(message_filename);
    if (message == NULL) return 0;
    char *key = read_string(key_filename);
    if (key == NULL){
        free(message);
        return 0;
    }
    int message_length = strlen(message);
    int key_length = strlen(key);
    if (message_length == 0) return 0;
    if (key_length == 0) return 0;

    // sort key alphabetically
    if (message_length % key_length != 0) return 0;
    char key_copy[key_length+1];
    strcpy(key_copy, key);
    char temp;
    for (int i=0;i<key_length-1;i++){
        for (int j=i+1;j<key_length;j++){
            if (key_copy[i] > key_copy[j]){
                temp = key_copy[i];
                key_copy[i] = key_copy[j];
                key_copy[j] = temp;
            }
        }
    }
    
    // construct 2D array
    int rows = message_length / key_length + 1;
    char cipher[key_length][rows+1];
    for (int i=0;i<key_length;i++){
        cipher[i][0] = key_copy[i];
        cipher[i][rows] = '\0';
    }
    int l = 0;
    for (int j=1;j<rows;j++){
        for (int i=0;i<key_length;i++){
            cipher[i][j] = message[l];
            l++;
        }
    }

    // decrpyt the message
    int n;
    bool found;
    int cipher_length = key_length;
    char plain[key_length][rows+1];
    for (int i=0;i<key_length;i++){
        n = 0;
        found = false;
        while (!found){
            if (key[i] == cipher[n][0]){
                found = true;
                strcpy(plain[i], cipher[n]);
                for (int j=n;j<cipher_length;j++) strcpy(cipher[j], cipher[j+1]);
                cipher_length--;
            }
            n++;
        }
    }

    // store the ciphertext in the buffer
    *result = (char*) malloc(sizeof(char) * key_length * (rows-1) + 1);
    if (*result == NULL){
        free(message);
        free(key);
        return 0;
    }
    int k = 0;
    for (int j=1;j<rows;j++){
        for (int i=0;i<key_length;i++){
            *(*result + k) = plain[i][j];
            k++;
        }
    }
    *(*result + k) = '\0';

    free(message);
    free(key);
    return 1;   
}

int main(void){
    char *result;
    encrypt_columnar("plain.txt", "key.txt", &result);
    printf("%s\n", result);
    free(result);
    result = NULL;

    char *result2;
    int success = decrypt_columnar("cipher.txt", "key.txt", &result2);
    printf("%s, %d\n", result2, success);
    free(result2);
    result2 = NULL;

    printf("success\n");
    return 0;
}