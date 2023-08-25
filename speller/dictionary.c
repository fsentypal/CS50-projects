// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// keeping track of number of words loaded
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    char temp[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        // convert to lowercase
        temp[i] = tolower(word[i]);
    }
    temp[len] = '\0';

    // get hash index
    int index = hash(temp);
    node *cursor = table[index];

    // go through the list at the hash index
    while (cursor != NULL)
    {
        // if the word is found return true
        if (strcmp(temp, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // mpas first letter of the word to an index
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    // read each word from the dict
    while (fscanf(file, "%s", word) != EOF)
    {
        // save memory for a node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }
        strcpy(new_node->word, word);
        int index = hash(word);
        // insert new node at start of list
        new_node->next = table[index];
        table[index] = new_node;
        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
   return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // go through each bucket
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        // clear each node in the list for the bucket
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
