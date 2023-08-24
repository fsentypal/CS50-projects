#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// define a BYTE type
typedef uint8_t BYTE;

// define block size
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // ensure good usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // open the image
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    int fileNumber = 0;
    FILE *img = NULL;
    char filename[8];
    // flag to check if i'm currently writing to a JPEG
    int writingJPEG = 0;

    // read the file in blocks
    while (fread(buffer, BLOCK_SIZE, 1, file))
    {
        // check for signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG is already open, close it
            if (writingJPEG)
            {
                fclose(img);
            }

            // create new JPEG
            sprintf(filename, "%03i.jpg", fileNumber++);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create %s.\n", filename);
                return 1;
            }

            // set the flag to show i'm writing to a JPEG
            writingJPEG = 1;
        }

        // if a JPEG is open, write to it
        if (writingJPEG)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    // close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(file);
    return 0;
}