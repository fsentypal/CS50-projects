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
    intletters = 0;
   int words = 1;
    intsentences = 0;

   for (int i = 0; i < strlen(text); i++)
   {
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

   float L = (float) letters / (float) words * 100;
   float S = (float) sentences / (float) words * 100;

   int index = round(0.0588 * L - 0.296 * S - 15.8);

   if (index < 1)
   {
       printf("Before Grade 1\n");
   }

   else if (index > 16)
   {
       printf("Grade 16+\n");
   }

   else
   {
       printf("Grade %i\n", index);
   }
}
