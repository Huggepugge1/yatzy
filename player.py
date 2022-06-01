# All combinations available
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

class Player:
    # Initializes Player object
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.ones = 0
        self.twos = 0
        self.threes = 0
        self.fours = 0
        self.fives = 0
        self.sixes = 0
        self.bonus = 0
        self.mini_sum = 0

        self.pair = 0
        self.two_pairs = 0
        self.three_of_a_kind = 0
        self.four_of_a_kind = 0
        self.small_straight = 0
        self.big_straight = 0
        self.full_house = 0
        self.chance = 0
        self.yatzy = 0
        self.sum = 0

    def print_table(self):
        print("Name:", self.name)
        print("----------------------------------")
        print("Ones:", self.ones)
        print("Twos:", self.twos)
        print("Threes:", self.threes)
        print("Fours:", self.fours)
        print("Fives:", self.fives)
        print("Sixes:", self.sixes)
        print("Bonus:", self.bonus)
        print("Sum:", self.mini_sum)
        print("----------------------------------")
        print("Pair:", self.pair)
        print("Two pairs:", self.two_pairs)
        print("Three of a kind: ", self.three_of_a_kind)
        print("Four of a kind: ", self.four_of_a_kind)
        print("Small straight:", self.small_straight)
        print("Big straight:", self.big_straight)
        print("Full house:", self.full_house)
        print("Chance: ", self.chance)
        print("Yatzy:", self.yatzy)
        print("Sum:", self.sum)

    # If bonus, add 50 to sum
    def check_bonus(self):
        if self.bonus == 0 and self.mini_sum >= 63:
            self.bonus = 50
            self.sum += 50

    # Check if option is valid
    def check_if_in_list(self, dice_throw):
        if dice_throw in alternatives:
            return True
        return False

    # Validates throw
    # Almost just if statements for every singe combination
    # Returns positive value if ok, -1 if not in roll, -2 if option not valid, -3 if erased and -4 if already taken
    def validate(self, roll, dice_throw):
        if not self.check_if_in_list(dice_throw):
            return -2
        self.check_bonus()
        roll = divide(roll)

        # Number of if statements to check if the chosen combination is possible from current throw
        if dice_throw == "ones":
            if self.ones == "-":
                return -3
            elif self.ones != 0:
                return -4
            elif str(roll[0]).count("1") == 0:
                return -1
            return str(roll[0]).count("1") * 1

        elif dice_throw == "twos":
            if self.twos == "-":
                return -3
            elif self.twos != 0:
                return -4
            if str(roll[1]).count("2") == 0:
                return -1
            return str(roll[1]).count("2") * 2

        elif dice_throw == "threes":
            if self.threes == "-":
                return -3
            elif self.threes != 0:
                return -4
            if str(roll[2]).count("3") == 0:
                return -1
            return str(roll[2]).count("3") * 3

        elif dice_throw == "fours":
            if self.fours == "-":
                return -3
            elif self.fours != 0:
                return -4
            if str(roll[3]).count("4") == 0:
                return -1
            return str(roll[3]).count("4") * 4

        elif dice_throw == "fives":
            if self.fives == "-":
                return -3
            elif self.fives != 0:
                return -4
            if str(roll[4]).count("5") == 0:
                return -1
            return str(roll[4]).count("5") * 5

        elif dice_throw == "sixes":
            if self.sixes == "-":
                return -3
            elif self.sixes != 0:
                return -4
            if str(roll[5]).count("6") == 0:
                return -1
            return str(roll[5]).count("6") * 6

        elif dice_throw == "pair":
            if self.pair == "-":
                return -3
            elif self.pair != 0:
                return -4
            pair = 0
            for value in roll:
                if len(value) >= 2:
                    pair = value[0] * 2
            if pair == 0:
                return -1
            return pair

        elif dice_throw == "two pairs":
            if self.two_pairs == "-":
                return -3
            elif self.two_pairs != 0:
                return -4
            pairs = []
            for value in roll:
                if len(value) >= 2:
                    pairs.append(value[0] * 2)
            if len(pairs) >= 2:
                return sum(pairs)
            else:
                return -1

        elif dice_throw == "three of a kind":
            if self.three_of_a_kind == "-":
                return -3
            elif self.three_of_a_kind != 0:
                return -4
            triple = 0
            for value in roll:
                if len(value) >= 3:
                    triple = value[0] * 3
            if triple == 0:
                return -1
            else:
                return triple

        elif dice_throw == "four of a kind":
            if self.four_of_a_kind == "-":
                return -3
            elif self.four_of_a_kind != 0:
                return -4
            quad = 0
            for value in roll:
                if len(value) >= 4:
                    quad = value[0] * 4
            if quad == 0:
                return -1
            else:
                return quad

        elif dice_throw == "small straight":
            if self.small_straight == "-":
                return -3
            elif self.small_straight != 0:
                return -4
            for value in roll[:-1]:
                if not len(value) >= 1:
                    return -1
            return 15

        elif dice_throw == "big straight":
            if self.big_straight == "-":
                return -3
            elif self.big_straight != 0:
                return -4
            for value in roll[1:]:
                if not len(value) >= 1:
                    return -1
            return 20

        elif dice_throw == "full house":
            if self.full_house == "-":
                return -3
            elif self.full_house != 0:
                return -4
            pair = 0
            triple = 0
            for value in roll:
                if len(value) == 2:
                    pair = value[0] * 2
                elif len(value) == 3:
                    triple = value[0] * 3
            if pair == 0 or triple == 0:
                return -1
            else:
                return pair + triple

        elif dice_throw == "chance":
            if self.chance == "-":
                return -3
            elif self.chance != 0:
                return -4
            return sum(map(lambda x: sum(x), roll))

        elif dice_throw == "yatzy":
            if self.yatzy == "-":
                return -3
            elif self.yatzy != 0:
                return -4
            yatzy = 0
            for value in roll:
                if len(value) == 5:
                    return 50
            return -1
        # Something is wrong if executed
        assert False, "unreachable"

    # Erases to yatzy chart
    # Almost just if statements for every singe combination
    def erase(self, roll, dice_throw):
        if not self.check_if_in_list(dice_throw):
            return -2
        val = self.validate(roll, dice_throw)
        if val == -3:
            return -3
        elif val == -4:
            return -4

        # If statements to erase the correct combination in chart
        if dice_throw == "ones":
            self.ones = "-"

        elif dice_throw == "twos":
            self.twos = "-"

        elif dice_throw == "threes":
            self.threes = "-"

        elif dice_throw == "fours":
            self.fours = "-"

        elif dice_throw == "fives":
            self.fives = "-"

        elif dice_throw == "sixes":
            self.sixes = "-"

        elif dice_throw == "pair":
            self.pair = "-"

        elif dice_throw == "two pairs":
            self.two_pairs = "-"

        elif dice_throw == "three of a kind":
            self.three_of_a_kind = "-"

        elif dice_throw == "four of a kind":
            self.four_of_a_kind = "-"

        elif dice_throw == "small straight":
            self.small_straight = "-"

        elif dice_throw == "big straight":
            self.big_straight = "-"

        elif dice_throw == "full house":
            self.full_house = "-"

        elif dice_throw == "chance":
            self.chance = "-"

        elif dice_throw == "yatzy":
            self.yatzy = "-"

        return 0

    # Adds to yatzy chart
    # Almost just if statements for every singe combination
    def throw(self, roll, dice_throw):
        if not self.check_if_in_list(dice_throw):
            return -2

        val = self.validate(roll, dice_throw)
        if val == -1:
            return -1

        if val == -3:
            return -3

        if val == -4:
            return -4

        # If statements which adds points to right places of chart
        if dice_throw == "ones":
            self.ones = val
            self.mini_sum += val
            self.sum += val

        elif dice_throw == "twos":
            self.twos = val
            self.mini_sum += val
            self.sum += val

        elif dice_throw == "threes":
            self.threes = val
            self.mini_sum += val
            self.sum += val

        elif dice_throw == "fours":
            self.fours = val
            self.mini_sum += val
            self.sum += val

        elif dice_throw == "fives":
            self.fives = val
            self.mini_sum += val
            self.sum += val

        elif dice_throw == "sixes":
            self.sixes = val
            self.mini_sum += val
            self.sum += val

        elif dice_throw == "pair":
            self.pair = val
            self.sum += val

        elif dice_throw == "two pairs":
            self.two_pairs = val
            self.sum += val

        elif dice_throw == "three of a kind":
            self.three_of_a_kind = val
            self.sum += val

        elif dice_throw == "four of a kind":
            self.four_of_a_kind = val
            self.sum += val

        elif dice_throw == "small straight":
            self.small_straight = val
            self.sum += val

        elif dice_throw == "big straight":
            self.big_straight = val
            self.sum += val

        elif dice_throw == "full house":
            self.full_house = val
            self.sum += val

        elif dice_throw == "chance":
            self.chance = val
            self.sum += val

        elif dice_throw == "yatzy":
            self.yatzy = val
            self.sum += val

        return 0

# easy but slow sorting algorithm
def sort_array(array):
    # Goes thru list len(list) number of times
    for i in range(len(array)):
        for j in range(len(array) - 1):
            # If current value array[j] > [j+1] switch them around
            if array[j] > array[j+1]:
                # Sets array[j] to array[j+1] and array[j+1] to array[j]
                array[j], array[j+1] = array[j+1], array[j]
    return array

# Make 1d array into 2d array by splitting it by numbers
def divide(array):
    n = [[], [], [], [], [], []]
    for i in array:
        n[i - 1].append(i)
    return n
