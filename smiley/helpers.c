#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // iterate over each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // check if the pixel is black
            if (image[i][j].rgbtRed == 0 && image[i][j].rgbtGreen == 0 && image[i][j].rgbtBlue == 0)
            {
                // Change the pixel color to red
                image[i][j].rgbtRed = 0;
                image[i][j].rgbtGreen = 255;
                image[i][j].rgbtBlue = 0;
            }
        }
    }
}
