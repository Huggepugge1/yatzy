from die import Die
from player import Player
from bot import *
from os import path
import json

difficulty = 2

def create_highscorelist():
    if not path.exists('./highscore.json'):
        with open('./highscore.json', 'w') as f:
            f.write(json.dumps("{}"))

def add_highscorelist(player, score):
    with open('./highscore.json', 'r') as f:
        highscore = json.load(f.read())
    with open('./highscore.json', 'w') as f:
        highscore[player] = score
        f.write(json.dumps(highscore))

def sort_highsorelist():
    with open('./highscore.json', 'r') as f:
        highscore = json.load(f.read())
    with open('./highscore.json', 'w') as f:
        highscore = sorted(highscore, key=lambda x: x[1])
        f.write(json.dumps(highscore))

def add_dice():
    dice = []
    for i in range(5):
        dice.append(Die())
    return dice

def add_players():
    players = []
    num_of_players = 0
    min_players = 1
    max_players = 5
    while min_players > num_of_players or num_of_players > max_players:
        try:
            num_of_players = int(input("How many players will play the game? "))
        except:
            print("Number of players has to be an integer.")
        if num_of_players > max_players:
            print(f"Cannot start game with more than {max_players} people")
        elif num_of_players < min_players:
            print(f"Cannot start game with less than {min_players} person")

    for _ in range(num_of_players):
        players.append(Player(name=input("What is your name? "), bot=False))

    num_of_bots = -1
    while 0 > num_of_bots:
        try:
            num_of_bots = int(input("How many bots will play the game? "))
        except:
            print("Number of bots has to be an integer.")

    for i in range(num_of_bots):
        players.append(Player(name=f"Bot_{i}", bot=True))

    return players

def save(dice, roll):
    saved = input(f"Your roll is {roll}, which dice do you want do save? ").replace(" ", "")
    try:
        saved = sorted([int(num) for num in saved])
    except:
        pass
    while len(saved) > 0:
        die = int(saved[0])
        dice = sorted([num for num in dice], lambda x: x.number)
        for i in range(len(dice)):
            if dice[i].number == die and not dice[i].saved:
                dice[i].saved = True
                break
            else:
                dice[i].saved = False
        saved = saved[1:]

def roll_die(dice):
    roll = []
    for die in dice:
        if die.saved:
            roll.append(die.number)
        else:
            roll.append(die.roll_dice())

    return roll

def validate_throw(player, roll):
    option = input("What do you want to do? ")
    if len(option.split()) > 0 and option.split()[0] == "erase":
        option = option[6:]
        correct = player.erase(roll, option)
    else:
        correct = player.throw(roll, option)
    while correct != 0:
        if correct == -1:
            option = input(f"{option} is not possible from your dice values.\nWhat do you want to do? ")
        elif correct == -2:
            option = input(f"{option} is not a valid option.\nWhat do you want to do? ")
        elif correct == -3:
            option = input(f"{option} is deleted.\nWhat do you want to do? ")
        elif correct == -4:
            option = input(f"You have already gotten {option}.\nWhat do you want to do? ")
        else:
            assert False, "Unreachable"

        if option == "":
            correct = -2
        elif option.split()[0] == "erase":
            option = option[6:]
            correct = player.erase(roll, option)
        else:
            correct = player.throw(roll, option)

def main():
    dice = add_dice()
    players = add_players()

    for i in range(len(alternatives)):
        for player in players:
            if not player.bot:
                print("---------------------------------------------------")
                player.print_table()
                for i in range(3):
                    print("----------------------------------")
                    roll = roll_die(dice)
                    if i != 2:
                        save(dice, roll)

                print(f"Your roll is {roll}")
                validate_throw(player, roll)

            else:
                for i in range(3):
                    roll = roll_die(dice)
                    if i != 2:
                        bot_save(dice, roll, difficulty, i)
                bot_validate_throw(player, roll, difficulty)

            for die in dice:
                die.value = 0
                die.saved = False

    s = []
    for i in players:
        if not player.bot:
            create_highscorelist()
            add_highscorelist(player.name, player.sum)
            sort_highsorelist()

        s.append(i.sum)

    print(min(s), max(s), sum(s) // len(s))

    option = input("Do you want to show, search or do nothing with the highscorelist? ")
    if option in ["show", "search"]:
        if option == "show":
            with open('./highscore.json', 'w') as f:
                for name, value in json.load(f.read()).values:
                    print(f"{name}: {value}")

if __name__ == "__main__":
    while True:
        main()