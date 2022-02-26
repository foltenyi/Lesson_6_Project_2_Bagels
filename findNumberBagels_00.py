###############################################################################
# Line length <= 99 characters
#
# findNumberBagels_00.py
#
# Helper program to
# CS-043-T001 Part 2 - Unit 6 - Final Collaborative Project: 2-3
# Bagels Game
# This script to find the Secret Number.
#
# bagels.py - The base for the other versions ...
# Taken from the book:
# Sweigart, Al. Invent Your Own Computer Games with Python, 4E (p. 151).
# No Starch Press. Kindle Edition.
#
###############################################################################

import itertools as ite
import inspect as ins  # Location in the program, members of a class


def ln() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed


class c:  # The variables not starting with '_' can be overwritten at the beginning
    # Using only class variables
    NUM_DIGITS =  3

poss = set()  # Set of the all possible numbers. The processing of the clue from the
              # Bagels program means deleting the impossible numbers from here

def getParameter():
    print('You can modify the number of digits')
    for m in ins.getmembers(c):  # type(m)=tuple (name as string, value as it is)
        if m[0][0] != '_':
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


def printInstruction():
    print(
"""
This program will give suggestion which number to give to the Bagels game.
If you entered that number, just copy and paste the clue from The Bagels program.
if you entered another number, then prepend it to the clue, e.g.
<your number> Fermi Pico
"""
    )


def fillAllPossibleNumbers():
    global c, poss
    poss = set()
    for n in list(ite.permutations('0123456789', c.NUM_DIGITS)):
        t = ''  # n is a tuple with characters
        for d in n:  # Should be a simpler way
            t += d
        poss.add(t)


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


def processBagles(num):
    global poss
    # Delete the numbers from poss, which DOES contain any digit from num
    possCopy = poss.copy()
    for n in possCopy:
        for d in num:
            if d in n:
                poss.remove(n)
                break  # Get the next n
    lpc = len(possCopy) ; lp = len(poss)
    print(f'Bagels: for {num} {lpc}-{lp}={lpc-lp} number was deleted.')


def processFermi(num, cfermi):
    if cfermi == 0:
        return
    # Delete the numbers from poss, which DOES NOT have cfermi digits on the same column as num
    possCopy = poss.copy()
    for n in possCopy:
        m = 0
        for i in range(len(num)):  # n and num have the same length
            if num[i] == n[i]:
                m += 1

        if m != cfermi:
            poss.remove(n)
            # print(f'{ln()}. removed {n=}')  # ???? Debug

    lpc = len(possCopy) ; lp = len(poss)
    print(f'Fermi {cfermi}: for {num} {lpc}-{lp}={lpc-lp} number was deleted.')


def processPico(num, cpico):
    if cpico == 0:
        return
    # Delete the numbers from poss, which DOES NOT have the same cpico number
    possCopy = poss.copy()
    for n in possCopy:
        m = 0
        for i in range(len(num)):  # n and num have the same length
            if num[i] == n[i]:
                continue  # This would be a Fermi number
            elif num[i] in n:
                m += 1

        if m != cpico:
            poss.remove(n)
            # print(f'{ln()}. removed {n=}')  # ???? Debug

    lpc = len(possCopy) ; lp = len(poss)
    print(f'Pico {cpico}: for {num} {lpc}-{lp}={lpc-lp} number was deleted.')


#######################################################################
def main():
    # Double loop, the outher for repeating games, the inner to find the Secret Number
    while True:
        getParameter()
        printInstruction()
        fillAllPossibleNumbers()

        while True:
            if len(poss) == 1:
                print(f'\nThe Secret Number was: {poss.pop()}\n')
                break

            recomm = next(iter(poss))
            print(f'Try: {recomm}')
            # Process the clue from the Bagels game program
            clue = input('Copy paste the clue (or q): ')
            if clue.lower().startswith('q'):
                break
            clueValid = True  # Most of the time
            bagelsWas = False
            cfermi = cpico = 0
            for w in clue.split():
                if w.isdecimal():
                    if isGoodNumber(w):
                        recomm = w
                    else:
                        clueValid = False
                        break  # for w ...
                elif w == 'Bagels':
                    bagelsWas = True
                elif w == 'Fermi':
                    cfermi += 1
                elif w == 'Pico':
                    cpico += 1
                else:
                    print(f"Unknown word '{w}'")
                    clueValid = False
                    break  # for w ...

            if not clueValid:
                print('Your clue input was ignored')
                continue  # The inner while True

            if bagelsWas:
                processBagles(recomm)
                continue

            processFermi(recomm, cfermi)
            processPico(recomm, cpico)

        if input('Do you want another assistance? (y/n): ').lower().startswith('n'):
            break


#######################################################################
if __name__ == '__main__':
    # breakpoint()  # ???? DEBUG, to set other breakpoints
    main()
    print('\nThanks for using this program, any suggestion is welcomed.')
