import os
import sys


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def bold_str(str):
    return (color.BOLD + str + color.END)


def red_str(str):
    return (color.RED + str + color.END)


def green_str(str):
    return (color.GREEN + str + color.END)


# Check if file path exists, if it doesn't create it
def setupFiles(files):
    for file in files:
        directory = os.path.dirname(file)
        if not os.path.exists(directory) and directory != "" and directory != ".":
            os.makedirs(directory)


# C like sprintf function
def sprintf(string, *args):
    return (string.format(*args))


def printf(format, *args, flush=False):
    sys.stdout.write(sprintf(format, *args))
    if flush is True:
        sys.stdout.flush()


def clearLine():
    sys.stdout.write("\033[K")  # Clear to the end of line


def cursorUpOneLine():
    sys.stdout.write("\033[F")  # Cursor up one line


def cursorUpLines(n):
    while n > 0:
        clearLine()
        cursorUpOneLine()
        clearLine()
        n -= 1


# Function that returns true if the word is found
def isWordPresent(sentence, word):
    # To break the sentence in words
    s = sentence.split(" ")

    for i in s:
        # Comparing the current word
        # with the word to be searched
        if i == word:
            return True

    return False
