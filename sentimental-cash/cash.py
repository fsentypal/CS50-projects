while True:
    try:
        change = float(input("Change owed: "))
        if change >= 0:
            break
    except ValueError:
        continue

cents = round(change * 100)
coins = 0

for coin in [25, 10, 5, 1]:
    coins += cents // coin
    cents %= coin

print(coins)