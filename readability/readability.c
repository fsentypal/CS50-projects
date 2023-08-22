#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int main(void)
{
    //Ask user for text
    string text = get_string("Text: ");

    //Set counter
    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        //Loop to check for letters, words, and sentences
        if (isalpha(text[i]))
        {
            letters++;
        }

        else if (text[i] == ' ')
        {
            words++;
        }

        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }

    //Define L and S according to given formula
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;

    //Use formula to calculate grade level
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        //If the index is less than the calculated Grade 1 print "Before Grade 1"
        printf("Before Grade 1\n");
    }

    else if (index > 16)
    {
        //If the index is greater than the calculated Grade 16 print "Grade 16+"
        printf("Grade 16+\n");
    }

    else
    {
        //If the index is in between 1 and 16 print "Grade %i"
        printf("Grade %i\n", index);
    }
}