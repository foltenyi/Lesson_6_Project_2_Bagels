################################################################
# line length <= 99
#
# bagels_02.py
# Added multiple players, if one s/he plays against the computer, if more they are
# playing against each other.
# The history of each player is kept and listed if more than one player.
# For this the Player class was introduced.
#
# bagels_01.py
# Made it more pythonic, more accurate, and more flexible.
#
# bagels_00.py
# Taken from the book:
# Sweigart, Al. Invent Your Own Computer Games with Python, 4E (p. 151).
# No Starch Press. Kindle Edition.
#
################################################################
#
import random
import inspect as ins  # Location in the program, members of a class


def ln() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed


class c:  # Members not starting with '_' can be modified
    NUM_DIGITS =  3
    MAX_GUESS  = 10
    NUMBER_OF_PLAYERS = 1


players = []  # players[i] is an instance of Player for player{i+1}
class Player:  # Add here what we shold know about a player
    def __init__(self, secret, n):
        self.attempts = []  # Will contain (<user guess>, <computer answer, clue>)
                           #                  string             string
        self.secretNum = secret
        self.Iam = n  # The player number, n+1 for the user interface
        self.foundIt = False

    def add(self, _guess, _clue):
        self.attempts.append((_guess, _clue))

    def List(self, final):
        if len(self.attempts) > 0:
            print('You guessed: computer gave clue:')
            for i in range(len(self.attempts)):
                print(f'{i+1:2d}.   {self.attempts[i][0]}     {self.attempts[i][1]}')
            if not self.foundIt and final:
                print(f'The Secret Number was: {self.secretNum}')


def getParameters():  # What are in class c
    print('You can modify the next parameters:')
    for m in ins.getmembers(c):  # type(m)=tuple (name as string, value as it is)
        if m[0][0] == '_':
            continue
        p = f'{m[0]} = {m[1]} ... Keep it? (y/n): '  # Make a prompt
        if input(p).lower().startswith('y'):
            continue  # for m
        # Get a new value
        while True:  # To allow to correct a bad answer
            v = input('Enter its new value: ')
            if v.isdecimal():
                # Construct the statement
                exec(f'c.{m[0]}={v}')
                break  # Out from while True
            else:  # Entered not decimal
                print('Please enter a decimal number.')
    # for m ...


def isGoodNumber(num) -> bool:  # num is a string
    if len(num) != c.NUM_DIGITS:
        print(f'Enter {c.NUM_DIGITS}-digit number.')
        return False
    if not num.isnumeric():
        print(f'Enter digits only.')
        return False
    # And now check for duplicate character
    for i in range(len(num) - 1):
        if num[i] in num[i + 1:]:
            break
    else:  # Executed if NO break
        return True
    print('There were duplicate digits')
    return False


def getSecretNum(n) -> str:
    # Returns a string of unique random digits that is NUM_DIGITS long.
    if c.NUMBER_OF_PLAYERS == 1:  # Generate the number string
        numbers = list(range(10))
        random.shuffle(numbers)
        _secretNum = ''
        for i in range(c.NUM_DIGITS):
            _secretNum += str(numbers[i])
    else:  # Ask another player to enter the number
        while (m := random.randint(0, c.NUMBER_OF_PLAYERS-1)) == n:
            pass
        print(f'Player{n+1}, please turn away')
        while True:
            _secretNum = input(f'Player{m+1}, please enter a Secret Number: ')
            if isGoodNumber(_secretNum):
                break

        print('Please, clan the screen')
        # I was unable to find the getpass library
        while True:
            a = input('How many lines to scroll?: ')
            if a.isdecimal():
                for _ in range(int(a)):
                    print()
                break

    return _secretNum  # As one string


def getGuess(p) -> str:  # p is an instance of class Player
    if c.NUMBER_OF_PLAYERS == 1:
        while True:
            _guess = input(f'Guess #{guessesTaken} (or q): ').lower()
            if _guess[0] == 'q':
                return _guess
            if isGoodNumber(_guess):
                return _guess

    # Multiple players
    print(f"It is Player{p.Iam+1}'s turn")
    p.List(False)  # Not final listing
    while True:
        _guess = input(f'Guess #{guessesTaken} (or q): ').lower()
        if _guess[0] == 'q':
            return _guess
        if isGoodNumber(_guess):
            return _guess


def getClues(p_guess, secret) -> str:
    # Returns a string with the Pico, Fermi, & Bagels clues to the user.
    if p_guess == secret:
        return 'You got it!'

    clues = []
    for i in range(len(p_guess)):
        if p_guess[i] == secret[i]:
            clues.append('Fermi')
        elif p_guess[i] in secret:
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'

    clues.sort()
    return ' '.join(clues)


# breakpoint()  # ???? ONLY FOR DEBUGGING


print('One or more players can play the Bagels Game.')
print('If one player, then the computer will generate the Secret Number.')
print('If more players, then another player will "hide" the Secret Number,')
print(f'The Secret Number is a {c.NUM_DIGITS}-digit number without repeating digits,')
print(f'the {c.NUM_DIGITS} can be changed. You try to guess what it is.')
print('The clues, given by the computer, are...')
print('When it said:  That means:')
print('   Bagels      None of the digits is correct.')
print('   Pico        One digit is correct but in the wrong position.')
print('   Fermi       One digit is correct and in the right position.')

while True:
    getParameters()  # Into class c
    for i in range(c.NUMBER_OF_PLAYERS):
        secretNum = getSecretNum(i)
        print(f'{ln()}. {secretNum=}')
        players.append(Player(secretNum, i))
        s = 'I have thought up a number. You' if c.NUMBER_OF_PLAYERS==1 else f'Player{i+1} you'
        print(s + f' have {c.MAX_GUESS} guesses to get it.')

    guessesTaken = 1
    # Preparation is done, start the game
    while guessesTaken <= c.MAX_GUESS:
        # Step through the players
        for i in range(len(players)):
            if players[i].foundIt:
                continue
            guess = getGuess(players[i])  # Instance of class Player
            # Any player can quit the game
            if guess[0] == 'q':
                print('Quitting the game ...')
                guessesTaken = c.MAX_GUESS
                break
            clue = getClues(guess, players[i].secretNum)
            players[i].add(guess, clue)
            print(clue)
            players[i].foundIt = (guess == players[i].secretNum)

        guessesTaken += 1

    # Game is over. List what the player(s) did.
    print('\nGame is over, this happened:')
    for i in range(len(players)):
        pr = 'Attempts' + (':' if c.NUMBER_OF_PLAYERS == 1 else f' of Player{i+1}:')
        print(pr)
        players[i].List(True)  # Final listing

    if input('Do you want to play again? (y/n): ').lower().startswith('y'):
        # Some clean up
        for i in range(len(players)):
            del players[i]  # class Player instance
        players = []
    else:
        break
