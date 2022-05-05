from player import Player
from die import Die
from random import *
import itertools

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

permutations = {}
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    perm = [i, j, k, l, m]
                    perm.sort()
                    strperm = "".join(str(num) for num in perm)
                    if strperm in permutations:
                        permutations[strperm] += 1
                    else:
                        permutations[strperm] = 1

optimal = {}
for perm in permutations:
    player = Player("test", True)
    optimal[perm] = []
    for option in alternatives:
        if option != "chance":
            optimal[perm].append([player.validate([int(num) for num in perm], option), option])
    optimal[perm].sort(key=lambda x: x[0], reverse=True)
    optimal[perm].append([sum(int(num) for num in perm), "chance"])

def save(dice, roll, saved):
    while len(saved) > 0:
        die = int(saved[0])
        for i in range(len(dice)):
            if dice[i].number == die and not dice[i].saved:
                dice[i].saved = True
                break
            saved = saved[1:]

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

    elif difficulty == 1:
        for option in alternatives:
            correct = player.throw(roll, option)
            if correct == 0:
                return
        for option in alternatives:
            correct = player.erase(roll, "erase " + option)
            if correct == 0:
                return

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

    elif difficulty == 3:
        roll.sort()
        strroll = "".join(str(num) for num in roll)
        for option in optimal[strroll]:
            if player.validate(roll, option[1]) > 0:
                player.throw(roll, option[1])
                return
        for option in alternatives:
            correct = player.erase(roll, "erase " + option)
            if correct == 0:
                return
    else:
        assert False, "unreachable"
