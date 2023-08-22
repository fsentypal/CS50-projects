#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool only_digits(string s);
char rotate(char c, int key);

int main(int argc, string argv[])
{
    // check for arguments
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // set up function to convert key to integer
    int key = atoi(argv[1]);

    // ask user for plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");

    // encrypt and print
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }
    printf("\n");

    return 0;
}

bool only_digits(string s)
{
    // iterate over each char
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // if not a string return false
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    // if other return true
    return true;
}

char rotate(char c, int key)
{
    // check if char is an alphabetical char
    if (isalpha(c))
    {
        // determine base and ASCII value
        char base = isupper(c) ? 'A' : 'a';
        // update char then turn it back to the base value
        return (c - base + key) % 26 + base;
    }
    // return c
    return c;
}