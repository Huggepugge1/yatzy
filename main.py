from die import Die
from player import Player

dice = []
for i in range(5):
    dice.append(Die(0, False))

players = []
for i in range(5):
    players.append(Player(str(i)))

for player in players:
    roll = []
    for die in dice:
        die.roll_dice()
        roll.append(die.number)

    print(f"Your roll is {roll}")
    player.throw(roll, input("What do you want to do? "))

print(list(dir(i) for i in players))
