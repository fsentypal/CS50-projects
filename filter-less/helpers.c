#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (RGBTRIPLE* pixel = image[i]; pixel < image[i] + width; pixel++)
        {
            // calc the ave of the values
            BYTE average = round((pixel->rgbtRed + pixel->rgbtGreen + pixel->rgbtBlue) / 3.0);

            // set each value to the ave
            pixel->rgbtRed = average;
            pixel->rgbtGreen = average;
            pixel->rgbtBlue = average;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (RGBTRIPLE* pixel = image[i]; pixel < image[i] + width; pixel++)
        {
            // store the original values
            int originalRed = pixel->rgbtRed;
            int originalGreen = pixel->rgbtGreen;
            int originalBlue = pixel->rgbtBlue;

            // calculate the sepia values using the formula
            int sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue);
            int sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue);
            int sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue);

            // make sure each value is capped at 255
            pixel->rgbtRed = (sepiaRed > 255) ? 255 : sepiaRed;
            pixel->rgbtGreen = (sepiaGreen > 255) ? 255 : sepiaGreen;
            pixel->rgbtBlue = (sepiaBlue > 255) ? 255 : sepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // iterate over each row
    for (int i = 0; i < height; i++)
    {
        RGBTRIPLE* start = image[i];
        RGBTRIPLE* end = image[i] + width - 1;

        // reflect the pixels by swapping pixels
        while (start < end)
        {
            RGBTRIPLE temp = *start;
            *start = *end;
            *end = temp;

            start++;
            end--;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    // copy the original image to the copy
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            *(copy[i] + j) = *(image[i] + j);
        }
    }

    // iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (RGBTRIPLE* pixel = image[i]; pixel < image[i] + width; pixel++)
        {
            int sumRed = 0, sumGreen = 0, sumBlue = 0, count = 0;

            // iterate over the pixel's next to the pixel
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    // check if the pixels around the pixel is in the boundaries
                    if (i + k >= 0 && i + k < height && pixel + l >= image[i] && pixel + l < image[i] + width)
                    {
                        RGBTRIPLE* neighbor = (copy[i + k] + (pixel - image[i]) + l);
                        sumRed += neighbor->rgbtRed;
                        sumGreen += neighbor->rgbtGreen;
                        sumBlue += neighbor->rgbtBlue;
                        count++;
                    }
                }
            }

            // calc the ave values and set them to the current pixel
            pixel->rgbtRed = round((float)sumRed / count);
            pixel->rgbtGreen = round((float)sumGreen / count);
            pixel->rgbtBlue = round((float)sumBlue / count);
        }
    }
}