from player import Player
from die import Die
from random import *
import itertools
# All options available
alternatives = [
    "ones",
    "twos",
    "threes",
    "fours",
    "fives",
    "sixes",
    "pair",
    "two pairs",
    "three of a kind",
    "four of a kind",
    "small straight",
    "big straight",
    "full house",
    "chance",
    "yatzy"
]

# Save dice
def save(dice, roll, saved):
    while len(saved) > 0:
        die = int(saved[0])
        for i in range(len(dice)):
            if dice[i].number == die and not dice[i].saved:
                dice[i].saved = True
                break
            saved = saved[1:]

# How the bots save their rolls. Depends on difficulty
def bot_save(dice, roll, difficulty, roll_number):
    if difficulty == 0:
        saved = sample(roll, randint(0, 5))
        save(dice, roll, saved)

    elif difficulty == 1:
        saved = [6 for i in range(roll.count(6))]
        save(dice, roll, saved)

    elif difficulty == 2:
        m = 0
        for num in roll:
            if roll.count(num) >= m:
                m = num
        saved = [m for num in range(roll.count(m))]
        save(dice, roll, saved)

    elif difficulty == 3:
        pass

# How the bots decide on decide what option to choose. Depends on difficulty
def bot_validate_throw(player, roll, difficulty):
    # Chooses randomly
    if difficulty == 0:
        option = sample(alternatives, 1)[0]
        if len(option.split()) > 0 and option.split()[0] == "erase":
            option = option[6:]
            correct = player.erase(roll, option)
        else:
            correct = player.throw(roll, option)
        while correct != 0:
            option = sample(alternatives, 1)[0]

            if randint(0, 1) == 1:
                option = "erase " + option

            if option.split()[0] == "erase":
                option = option[6:]
                correct = player.erase(roll, option)
            else:
                correct = player.throw(roll, option)

    # Up to down
    elif difficulty == 1:
        for option in alternatives:
            correct = player.throw(roll, option)
            if correct == 0:
                return
        for option in alternatives:
            correct = player.erase(roll, "erase " + option)
            if correct == 0:
                return

    # Trys to choose the best possible choice for the situation
    elif difficulty == 2:
        best = []
        for option in alternatives:
            correct = player.validate(roll, option)
            if correct > 0:
                best.append([correct, option])
        if len(best) > 0:
            m = [0, ""]
            for i in best:
                if i[0] > m[0]:
                    m = i
            player.throw(roll, m[1])
            return
        for option in alternatives:
            correct = player.erase(roll, "erase " + option)
            if correct == 0:
                return

    else:
        assert False, "unreachable"
