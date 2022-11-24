class PetSettings:
    autofeed = True
    petfood_key = "ins"
    num_of_pets = 1


class GeneralKeyBindigs:
    interact_key = "space"
    jump_key = "alt"
    rope_lift_key = None


class ScanCodes:
    # this is a list of scan codes and corrsponding keyboard key.
    # do not edit unless you know what you are doing.
    SC_DECIMAL_ARROW = {
        "LEFT": 75, "RIGHT": 77, "DOWN": 80, "UP": 72,
    }

    SC_DECIMAL = {
        "ESC": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10, "0": 11, "-": 12, "=": 13,
        "Q": 16, "W": 17, "E": 18, "R": 19, "T": 20, "Y": 21, "U": 22, "I": 23, "O": 24, "P": 25,
        "[": 26, "]": 27,
        "Enter": 28, "CTRL": 29,
        "A": 30, "S": 31, "D": 32, "F": 33, "G": 34, "H": 35, "J": 36, "K": 37, "L": 38, ";": 39,
        "LShift": 42,
        "Z": 44, "X": 45, "C": 46, "V": 47, "B": 48, "N": 49, "M": 50,
        "RShift": 54, "Alt": 56, "Space": 57,
        "F1": 59, "F2": 60, "F3": 61, "F4": 62, "F5": 63, "F6": 64, "F7": 65, "F8": 66, "F9": 67, "F10": 68,
        "Num": 69, "Scroll": 70, "Home": 71, "PageUp": 73,
        "-": 74, "+": 78,
        "End": 79, "PageDown": 81, "Ins": 82, "Del": 83,
    }
