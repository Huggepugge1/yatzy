from die import Die
from player import Player
from bot import *

difficulty = 2

def print_highscore_list():
    

def add_dice():
    dice = []
    for i in range(5):
        dice.append(Die(0, False))
    return dice

def add_players():
    players = []
    num_of_players = 0
    min_players = 0
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

    num_of_bots = 1000
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
    while len(saved) > 0:
        die = int(saved[0])
        for i in range(len(dice)):
            if dice[i].number == die and dice[i].saved == False:
                dice[i].saved = True
                break
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
                        bot_save(dice, roll, difficulty)
                bot_validate_throw(player, roll, difficulty)

            for die in dice:
                die.value = 0
                die.saved = False

    s = []
    yatzy = 0
    for i in players:
        if i.yatzy == 50: yatzy += 1
        s.append(i.sum)

    print(min(s), max(s), sum(s) // len(s))

if __name__ == "__main__":
    while True:
        main()