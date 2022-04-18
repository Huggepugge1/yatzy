class Player():
    def __init__(self, name):
        self.name = name
        self.ones = 0
        self.twos = 0
        self.threes = 0
        self.fours = 0
        self.fives = 0
        self.sixes = 0
        self.bonus = 0

        self.pair = 0
        self.two_pairs = 0
        self.three_of_a_kind = 0
        self.four_of_a_kind = 0
        self.small_straight = 0
        self.big_straight = 0
        self.full_house = 0
        self.chance = 0
        self.yatzy = 0

    def erase(self, dice_throw):
        pass

    def throw(self, roll, dice_throw):
        merge_sort(roll)
        roll = divide(roll)

        if dice_throw == "ones":
            if str(roll).count("1") == 0:
                return -1
            self.ones = str(roll).count("1")
        elif dice_throw == "twos":
            if str(roll).count("2") == 0:
                return -1
            self.twos = str(roll).count("2")
        elif dice_throw == "threes":
            if str(roll).count("3") == 0:
                return -1
            self.threes = str(roll).count("3")
        elif dice_throw == "fours":
            if str(roll).count("4") == 0:
                return -1
            self.fours = str(roll).count("4")
        elif dice_throw == "fives":
            if str(roll).count("5") == 0:
                return -1
            self.fives = str(roll).count("5")
        elif dice_throw == "sixes":
            if str(roll).count("6") == 0:
                return -1
            self.fives = str(roll).count("6")

        elif dice_throw == "pair":
            pair = 0
            for value in roll:
                if len(value) >= 2:
                    self.pair = value[0] * 2
            if pair == 0:
                return -1

        elif dice_throw == "two_pairs":
            pairs = []
            for value in roll:
                if len(value) >= 2:
                    pairs.append(value[0] * 2)
            if len(pairs) == 2:
                self.two_pairs += sum(pairs)

        elif dice_throw == "three_of_a_kind":
            triple = 0
            for value in roll:
                if len(value) >= 3:
                    triple = value[0] * 3
                    break
            if triple == 0:
                return -1
            else:
                self.three_of_a_kind = triple

        elif dice_throw == "four_of_a_kind":
            quad = 0
            for value in roll:
                if len(value) >= 4:
                    quad = value[0] * 4
            if quad == 0:
                return -1
            else:
                self.four_of_a_kind = quad

        elif dice_throw == "small_straight":
            if len(roll[0]) > 0 and len(roll[1]) > 0 and len(roll[2]) > 0:
                if len(roll[3]) > 0 and len(roll[4]) > 0:
                    self.small_straight = 15
                else:
                    return -1
            else:
                return -1

        elif dice_throw == "big_straight":
            if len(roll[1]) > 0 and len(roll[2]) > 0 and len(roll[3]) > 0:
                if len(roll[4]) > 0 and len(roll[5]) > 0:
                    self.big_straight = 20
                else:
                    return -1
            else:
                return -1

        elif dice_throw == "full_house":
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
                self.full_house = pair + triple

        elif dice_throw == "chance":
            self.chance = sum(map(lambda x: sum(x), roll))

        elif dice_throw == "yatzy":
            yatzy = 0
            for value in roll:
                if len(value) == 5:
                    yatzy = 50
            if yatzy == 0:
                return -1
            else:
                yatzy = 50


def merge_sort(array):
    if len(array) > 1:
        s = len(array) // 2
        l = array[s:]
        r = array[:s]

        merge_sort(l)
        merge_sort(r)

        i = j = k = 0

        while i - len(l) and j < len(r):
            if l[i] < l[j]:
                array[k] = l[i]
                i += 1
            else:
                array[k] = r[j]
                j += 1
            k += 1

        while i < len(l):
            array[k] = l[i]
            i += 1
            k += 1

        while j < len(r):
            array[k] = r[j]
            j += 1
            k += 1

def divide(array):
    n = [[], [], [], [], [], []]
    for i in array:
        n[i - 1].append(i)
    return n
