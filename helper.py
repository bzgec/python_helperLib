import os
import sys
import logging
import json


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
    def setupFile(filePath):
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory) and directory != "" and directory != ".":
            os.makedirs(directory)

        if not os.path.isdir(filePath):
            # Path is not a directory -> path is a file
            if not os.path.isfile(filePath):
                # File doesn't exist
                with open(filePath, "w") as file:
                    # Just create empty file
                    file.write("")

    if type(files) is list:
        # Argument is a list of file/folders
        for filePath in files:
            setupFile(filePath)
    else:
        # Argument is a string
        setupFile(files)


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


def getSmallestPositiveValueIdx(arr):
    return arr.index(min(arr))


# Logger setup
def loggerSetup(loggerName, logFile, level=logging.INFO, dateFormat='%Y/%m/%d %H:%M:%S', fileMode='a'):
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', dateFormat)

    setupFiles(logFile)

    handler = logging.FileHandler(logFile, fileMode)
    handler.setFormatter(formatter)
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def isJson(jsonStr, objStr=None):
    try:
        jsonObj = json.loads(jsonStr)
        json.dumps(jsonObj)

        if objStr is not None:
            myObj = jsonObj[objStr]
            myObj  # To ignore "F841" warning

    except Exception:
        return False

    return True


def promptYesNo(question):
    prompt = f'{question} (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return promptYesNo(question)
    if ans == 'y':
        return True
    return False


def isRunningInDocker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv')
        or os.path.isfile(path) and any('docker' in line for line in open(path))
    )
