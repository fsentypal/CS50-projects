# get text input
text = input("Text: ")

# calculate the number of letters, words, and sentences
letters = sum(c.isalpha() for c in text)
words = len(text.split())
sentences = text.count('.') + text.count('!') + text.count('?')

# calculate L and S
L = (letters / words) * 100
S = (sentences / words) * 100

# calculate the index
index = round(0.0588 * L - 0.296 * S - 15.8)

# print the grade level
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")