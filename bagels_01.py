################################################################
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


class c:  # Members not starting with '_' can be modified
    NUM_DIGITS =  3
    MAX_GUESS  = 10


def getSecretNum():
    # Returns a string of unique random digits that is NUM_DIGITS long.
    numbers = list(range(10))
    random.shuffle(numbers)
    _secretNum = ''
    for i in range(c.NUM_DIGITS):
        _secretNum += str(numbers[i])
    return _secretNum  # As one string


def getClues(p_guess, secret):
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


print(f'I am thinking of a {c.NUM_DIGITS}-digit number without repeating digits,')
print(f'the {c.NUM_DIGITS} can be changed. Try to guess what it is.')
print('The clues I give are...')
print('When I say:    That means:')
print(' Bagels        None of the digits is correct.')
print(' Pico          One digit is correct but in the wrong position.')
print(' Fermi         One digit is correct and in the right position.')

while True:
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

    secretNum = getSecretNum()
    print(f'I have thought up a number. You have {c.MAX_GUESS} guesses to get it.')

    guessesTaken = 1
    while guessesTaken <= c.MAX_GUESS:
        guess = ''
        while True:  # Break out if we have a syntactically correct guess
            guess = input(f'Guess #{guessesTaken}: ')
            if len(guess) != c.NUM_DIGITS:
                print(f'Enter {c.NUM_DIGITS}-digit number.')
                continue
            if not guess.isnumeric():
                print(f'Enter digits only.')
                continue
            # And now check for duplicate character
            for i in range(len(guess)-1):
                if guess[i] in guess[i+1:]:
                    break
            else:  # Executed if NO break
                break  # from while True
            print('There were duplicate digits')

        print(getClues(guess, secretNum))
        guessesTaken += 1

        if guess == secretNum:
            break
        if guessesTaken > c.MAX_GUESS:
            print(f'You ran out of guesses. The answer was {secretNum}.')

    print('Do you want to play again? (y/n)')
    if not input().lower().startswith('y'):
        break
