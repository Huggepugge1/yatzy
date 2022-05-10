# Koden fungerar, bot suger

from die import Die
from player import Player
from bot import *
from os import path
import json

def create_highscorelist():
    if not path.exists('./highscore.json'):
        with open('./highscore.json', 'w') as f:
            f.write(json.dumps({}))

def add_highscorelist(player, score):
    with open('./highscore.json', 'r') as f:
        highscore = json.loads(f.read())
    with open('./highscore.json', 'w') as f:
        highscore[player] = score
        f.write(json.dumps(highscore))

def sort_highsorelist():
    with open('./highscore.json', 'r') as f:
        highscore = json.loads(f.read())
    with open('./highscore.json', 'w') as f:
        highscore = dict(sorted(highscore.items(), key=lambda x: x[1], reverse=True))
        f.write(json.dumps(highscore))

def search_highscorelist(player):
    with open('./highscore.json', 'r') as f:
        highscorelist = json.load(f)
    try:
        print(f"{player}: {highscorelist[player]}")
    except KeyError:
        print(f"{player} not in highscore list.")

# Main menu
def menu():
    print("This is yatzy. You throw dice and hope to get combinations.")
    print("Your turn consists of 6 phases.")
    print("First you roll, then you save the dice you like.")
    print("Then you roll and save the dice you like.")
    print("Lastly you roll and choose what combination you would like.")
    print("If all possible combinations are already taken, you must erase one combination.\n")
    option = ""
    while option not in [1, 2]:
        try:
            option = int(input("Do you want to play the game (1) or interact with the highscorelist(2)? "))
            if option not in [1, 2]:
                print("Must input 1 or 2.")
        except ValueError:
            print("Must input 1 or 2.")

# Creates five die objects
def add_dice():
    dice = []
    for i in range(5):
        dice.append(Die())
    return dice

# Creates num_of_players number of player Objects
def add_players():
    players = []
    num_of_players = 0
    # Min and max players to prevent bugs
    min_players = 1
    max_players = 10000
    # Making sure num_of_players is int between min and max players
    while min_players > num_of_players or num_of_players > max_players:
        try:
            num_of_players = int(input("How many players will play the game? "))
            if num_of_players > max_players:
                print(f"Cannot start game with more than {max_players} people")
            elif num_of_players < min_players:
                print(f"Cannot start game with less than {min_players} person")
        except ValueError:
            print("Number of players has to be an integer.")

    for _ in range(num_of_players):
        players.append(Player(name=input("What is your name? "), bot=False))

    num_of_bots = -1
    while 0 > num_of_bots:
        try:
            num_of_bots = int(input("How many bots will play the game? "))
        except:
            print("Number of bots has to be an integer.")
    # Adds num_of_bots bots to player list. Name is Bot followed by a number
    for i in range(num_of_bots):
        players.append(Player(name=f"Bot_{i + 1}", bot=True))

    return players

# Saves the dice
def save(dice, roll):
    saved = input(f"Your roll is {roll}, which dice do you want do save? ").replace(" ", "")

    while isinstance(saved, str):
        try:
            saved = sorted([int(num) for num in saved])
        except ValueError:
            print(f"All characters in {saved} is not space or numbers.")
            saved = input(f"Your roll is {roll}, which dice do you want do save? ").replace(" ", "")

    # Sorts dice by value
    dice = sorted([num for num in dice], key=lambda x: x.number)

    # Goes thru dice and saves them if there values are in "saved" list.
    while len(saved) > 0:
        die = saved[0]
        for i in range(len(dice)):
            if dice[i].number == die and not dice[i].saved:
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
        die.saved = False

    return roll

# This function evaluates your throw and adds to yatzy chart
def validate_throw(player, roll):
    option = input("What do you want to do? ")
    # Check if you want to erase thing in yatzy chart
    if len(option.split()) > 0 and option.split()[0] == "erase":
        option = option[6:]
        correct = player.erase(roll, option)
    else:
        correct = player.throw(roll, option)
    # Validates option
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
            # Makes sure code works, if this triggers something is seriously wrong.
            assert False, "Unreachable"

        # Adds combination to yatzy chart
        if option.split()[0] == "erase":
            option = option[6:]
            correct = player.erase(roll, option)
        else:
            correct = player.throw(roll, option)

# Game function
def main():
    create_highscorelist()
    game = menu()
    # If you want to play the game.
    if game == 1:
        dice = add_dice()
        players = add_players()
        difficulty = -1
        while difficulty not in [0, 1, 2]:
            try:
                difficulty = int(input("Choose you difficulty (0, 1, 2)"))
                if difficulty not in [0, 1, 2]:
                    print("Must be 0, 1 or 2.")
            except ValueError:
                print("Must be 0, 1, or 2.")

        # Game is len of alternatives (combinations) turns long
        for _ in range(len(alternatives)):
            # Every player does its turn
            for player in players:
                # a bots turn is a little bit different
                if not player.bot:
                    # Rolling
                    for i in range(3):
                        roll = roll_die(dice)
                        if i != 2:
                            save(dice, roll, 2)
                    # Evaluating throw and adding to yatzy Chart
                    validate_throw(player, roll)

                else:
                    # Bot turn
                    for i in range(3):
                        roll = roll_die(dice)
                        if i != 2:
                            bot_save(dice, roll, difficulty, i)
                    bot_validate_throw(player, roll, difficulty)

        # Add non bots to highscore list
        for player in players:
            if not player.bot:
                add_highscorelist(player.name, player.sum)
        sort_highsorelist()

    # Interact with highscore list
    elif game == 2:
        option = input("Do you want to show, search or do nothing with the highscorelist? ")
        if option in ["show", "search"]:
            if option == "show":
                with open('./highscore.json', 'r') as f:
                    f = json.loads(f.read())
                    for name, score in enumerate(f.items()):
                        print(f"{name}: {score}")
            elif option == "search":
                search_highscorelist(input("Who do you want to search for? "))

if __name__ == "__main__":
    while True:
        main()