from die import Die
from player import Player
from bot import *
from os import path
import json

def create_highscorelist():
    # Creates highscorelist if not in current working directory
    if not path.exists('./highscore.json'):
        with open('./highscore.json', 'w') as f:
            f.write(json.dumps({}))

def add_highscorelist(player, score):
    # Opens highscorelist and converts it to a dictionary
    # Adds player and score to the dictionary and writes it to highscore file
    with open('./highscore.json', 'r') as f:
        highscore = json.loads(f.read())
    with open('./highscore.json', 'w') as f:
        highscore[player] = score
        f.write(json.dumps(highscore))

def sort_highsorelist():
    # Opens highscorelist and converts it to a dictionary
    # Sorts highscorelist by values in dictionary
    with open('./highscore.json', 'r') as f:
        highscore = json.loads(f.read())
    with open('./highscore.json', 'w') as f:
        highscore = dict(sorted(highscore.items(), key=lambda x: x[1], reverse=True))
        f.write(json.dumps(highscore))

def search_highscorelist(player):
    # Opens highscorelist and converts it to a dictionary
    # Then it searches for the key "player", if not found, prints not found
    with open('./highscore.json', 'r') as f:
        highscorelist = json.load(f)
    try:
        print(f"{player}: {highscorelist[player]}")
    except KeyError:
        print(f"{player} not in highscore list.")

def print_instructions():
    print("Your turn consists of 6 phases.")
    print("First you roll, then you save the dice you like.")
    print("Then you roll and save the dice you like.")
    print("Lastly you roll and choose what combination you would like.")
    print("If all possible combinations are already taken, you must erase one combination.")
    print("If you want to erase on combination, write erase and then the combination.\n")
    print("Rolling is done automaticly.")
    print("If you want to save some dice, input the VALUES of the dice. "
          "For example \"444\" if you want to save three fours.")
    print("The combinations have the exact same name as in the table shown BEFORE your turn.\n")
    print("Combinations: \n"
          "    Ones: Any amount of ones (\"11111\")\n"
          "    Twos: Any amount of twos (\"22222\")\n"
          "    Threes: Any amount of threes (\"33333\")\n"
          "    Fours: Any amount of fours (\"44444\")\n"
          "    Fives: Any amount of fives (\"55555\")\n"
          "    Sixes: Any amount of sixes (\"66666\")\n"
          "    Bonus: If your total sum of above combinations if above 63 at the end of the game, get"
          "50 extra points.\n\n"
          "    Pair: A pair of any number (\"66\")\n"
          "    Two pairs: Two pairs of any numbers that are not the same (\"6655\")\n"
          "    Three of a kind: Three of any number (\"666\")\n"
          "    Four of a kind: Four of any number (\"6666\")\n"
          "    Small straight: All numbers from 1 to 5 (\"12345\")\n"
          "    Big straight: All numbers from 2 to 6 (\"23456\")\n"
          "    Full house: Three of a kind and pair (\"66655\"\n"
          "    Chance: Any nubers (\"66666\")\n"
          "    Yatzy: Five of a kind (\"66666\")")
# Main menu
def menu():
    print("This is yatzy. You throw dice and hope to get combinations.")
    option = ""
    # Error handling
    while option not in [1, 2, 3, 4]:
        try:
            option = int(input("Do you want to play the game (1), "
                               "interact with the highscorelist (2), "
                               "view the instructions (3)"
                               "or exit (4)?"))
            if option not in [1, 2, 3, 4]:
                print("Must input 1, 2, 3 or 4.")
        except ValueError:
            print("Must input 1, 2, 3 or 4.")
    return option

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
    # Making sure num_of_players is int between min and max players, error handling
    while min_players > num_of_players or num_of_players > max_players:
        try:
            num_of_players = int(input("How many players will play the game? "))
            if num_of_players > max_players:
                print(f"Cannot start game with more than {max_players} people")
            elif num_of_players < min_players:
                print(f"Cannot start game with less than {min_players} person")
        except ValueError:
            print("Number of players has to be an integer.")

    # _ makes sure no variable is created for increased speed and less memory consumption
    for _ in range(num_of_players):
        players.append(Player(name=input("What is your name? "), bot=False))

    num_of_bots = -1
    # Error handling
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
        for curr_die in dice:
            if curr_die.number == die and not curr_die.saved:
                curr_die.saved = True
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
    print(f"Your roll is {roll}.")
    option = input("What do you want to do? ")
    # Check if you want to erase thing in yatzy chart
    if len(option.split()) > 0 and option.split()[0] == "erase":
        option = option[6:]
        correct = player.erase(roll, option.lower())
    else:
        correct = player.throw(roll, option.lower())
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
            correct = player.erase(roll, option.lower())
        else:
            correct = player.throw(roll, option.lower())

# Game function
def main():
    create_highscorelist()
    # mode is the mode your are in (game, highscore, instructions)
    mode = menu()
    # If you want to play the game.
    if mode == 1:
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
                    player.print_table()
                    # Rolling
                    for i in range(3):
                        roll = roll_die(dice)
                        if i != 2:
                            save(dice, roll)
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
    elif mode == 2:
        option = input("Do you want to show, search or do nothing with the highscorelist? ")
        if option in ["show", "search"]:
            if option == "show":
                with open('./highscore.json', 'r') as f:
                    f = json.loads(f.read())
                    for name, score in enumerate(f.items()):
                        print(f"{name}: {score}")
            elif option == "search":
                search_highscorelist(input("Who do you want to search for? "))

    elif mode == 3:
        print_instructions()

    elif mode == 4:
        exit

if __name__ == "__main__":
    while True:
        main()