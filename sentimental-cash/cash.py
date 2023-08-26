while True:
    try:
        # ask for amount of change owed
        change = float(input("Change owed: "))

        # if the input is non-negative, break
        if change >= 0:
            break
    # if the input is not a number, continue
    except ValueError:
        continue

# convert the change from dollars to cents
cents = round(change * 100)
# initialize a counter
coins = 0

# loop through each coin type
for coin in [25, 10, 5, 1]:
    # add the number of coins to the counter
    coins += cents // coin
    # update the remaining cents
    cents %= coin

print(coins)