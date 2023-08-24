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

    BYTE byte;
    int byteCount = 0;
    int fileNumber = 0;
    FILE *img = NULL;
    char filename[8];

    // read the file by byte
    while (fread(&byte, 1, 1, file))
    {
        byteCount++;

        // check for signature
        if (byteCount >= 4 && byte == 0xff)
        {
            // move back 4 bytes to check signature
            fseek(file, -4, SEEK_CUR);
            BYTE signature[4];
            fread(signature, 1, 4, file);

            if (signature[0] == 0xff && signature[1] == 0xd8 && signature[2] == 0xff && (signature[3] & 0xf0) == 0xe0)
            {
                // if a JPEG is already open, close it
                if (img != NULL)
                {
                    fclose(img);
                }

                // create a new JPEG
                sprintf(filename, "%03i.jpg", fileNumber++);
                img = fopen(filename, "w");
                if (img == NULL)
                {
                    printf("Could not create %s.\n", filename);
                    return 1;
                }

                // reset byte count
                byteCount = 0;
            }
            else
            {
                // move back to where I was
                fseek(file, -3, SEEK_CUR);
            }
        }

        // if a JPEG is open, write to it
        if (img != NULL)
        {
            fwrite(&byte, 1, 1, img);
        }
    }

    // close any lasting files
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(file);
    return 0;
}