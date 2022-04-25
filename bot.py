from random import *

options = []

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

def save(dice, roll, saved):
    while len(saved) > 0:
        die = int(saved[0])
        for i in range(len(dice)):
            if dice[i].number == die and dice[i].saved == False:
                dice[i].saved = True
                break
            saved = saved[1:]

def bot_save(dice, roll, difficulty):
    if difficulty == 0:
        saved = sample(roll, randint(0, 5))
        save(dice, roll, saved)

    elif difficulty == 1:
        saved = [6 for i in range(roll.count(6))]
        save(dice, roll, saved)

    elif difficulty == 2:
        m = 0
        for i in roll:
            if roll.count(i) >= m:
                m = i
        saved = [m for i in range(roll.count(m))]
        save(dice, roll, saved)

def bot_validate_throw(player, roll, difficulty):
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

    if difficulty == 1:
        for option in alternatives:
            correct = player.throw(roll, option)
            if correct == 0:
                return
        for option in alternatives:
            correct = player.erase(roll, "erase " + option)
            if correct == 0:
                return

    if difficulty == 2:
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
