#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        // get user input
        n = get_int("Height: ");

    }
    while (n < 1 || n > 8);

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (i + j < n - 1)

            {
                // add blankspace
                printf(" ");
            }
            else
            {
                // add number of hashes
                printf("#");
            }
        }
        printf("\n");
    }
}