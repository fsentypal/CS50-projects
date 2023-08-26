# set height to 0
height = 0

# promt user until input is btwn 1 and 8
while not 1 <= height <= 8:
    try:
        # prompt for height
        height = int(input("Height: "))
    except ValueError:
        pass

# loop through each lvl of the pyramid
for i in range(1, height + 1):
    # print spaces and hashes where needed
    print(" " * (height - i) + "#" * i)