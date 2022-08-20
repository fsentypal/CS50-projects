#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask user for their name
    string name = get_string("What's your name? \n");

    // Display user's answer
    printf("hello, %s\n", name);
}