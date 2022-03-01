###############################################################################
# Line length <= 99 characters
#
# Nothing to do with ...
# Brigham Young University
# CS-043-T001:
# Computer Science, Part 2 (TL)
# Unit 6: Final Collaborative Project
# Project 2-3: Bagels
# ... but there are similarities with the program, which helps to find the Secret Number
#
# find4Wordle_00.py
#
# There are similarities with findNumberBagels_00.py
#
###############################################################################

import re
import itertools as ite
import sqlite3
import inspect as ins  # Location in the program, members of a class


def ln() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.lineno:3d}'
def fl() -> str:
    fi = ins.getframeinfo(ins.currentframe().f_back)
    return f'{fi.function} {fi.lineno:3d}'  # fi.filename if needed


class c:  # The variables not starting with '_' can be overwritten at the beginning
    # Using only class variables
    NUM_LETTERS = 5
    DB_PATH = 'C:/Users/folte/PycharmProjects/cs043/Lesson_6/Project_2_Bagels'
    DB_NAME = 'words_00.db'

##################### G L O B A L S #####################

az = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

patt = []  # list of c.NUM_LETTERS sets, each set contains the letters can be
# in that patt position, start with set(az)

ws = []  # ws[i] is a potential word sorted by how many times the letters in word can be found
# in all words read from the SQLite database sorted in descending order.
# The words read from the database, converted to upper case.

##################### F U N C T I O N S #####################

def getParameters():
    print('You can modify these:')
    for m in ins.getmembers(c):  # type(m)=tuple (name as string, value as it is)
        if m[0][0] != '_':
            p = f'{m[0]} = {m[1]} ... Keep it? (y/n): '  # Make a prompt
            if input(p).lower().startswith('y'):
                continue  # for m
            # Get a new value
            v = input('Enter its new value: ')
            if v.isdecimal():
                # Construct the statement
                exec(f'c.{m[0]}={v}')
            else:  # Entered not decimal, assume it is a string not containing '"'
                exec(f'c.{m[0]}="{v}"')


def printInstruction():
    print(
"""
This program will give suggestion which word to give to the Wordle game.
If you entered that word, just enter the first letters of the colors the computer
answered. If you entered a different word, prepend it. E.g. for 5 letter words:
bgbyy        - if you entered the suggested word
frame gbyby  - if you entered 'frame', not the suggested word
For adding / deleting / editing words in the SQLite database you can use
DB Browser for SQLite
""")


# A word is good if c.NUM_LETTERS long and contains only letters
def isGoodWord(w) -> bool:  # w is a string
    if len(w) != c.NUM_LETTERS:
        print(f'{w} is not {c.NUM_LETTERS} long.')
        return False
    if not w.isalpha():
        print(f'{w} should contain only letters.')
        return False
    return True


def getWords_SetupGame():
    global ws, patt
    db = c.DB_PATH + '/' + c.DB_NAME
    connection = sqlite3.connect(db)  # words is a table in this db
    cursor = connection.cursor()
    tn = f'words_{c.NUM_LETTERS:02d}'
    _ws = cursor.execute(f'SELECT * FROM {tn}').fetchall()
    connection.close()

    _wc = _ws.copy()
    for _w in _wc:  # _w is a tuple with one element
        if not isGoodWord(_w[0]):
            print(f"Delete or correct '{_w[0]}' in {tn}")
            _ws.remove(_w)

    # Upper case all words
    lw = []  # Will be list of all upper case words
    for i in range(len(_ws)):
        lw.append(_ws[i][0].upper())

    # Fill up _t with (n,word)
    _t = []
    for x in lw:
        n = 0
        for y in lw:
            n += len(set(x) & set(y))
        _t.append((n, x))
    _t.sort(reverse=True)
    # Take out the words keeping the order
    ws = []
    for x in _t:
        ws.append(x[1])
    # ws setup is done

    # Set up the pattern for each position, everything is possible
    for i in range(c.NUM_LETTERS):
        patt.append(set(az))

    pass  # ???? to set breakpoint


def reducePattern(word, colors):
    global patt, ws
    for i in range(len(colors)):
        _x = word[i]
        _c = colors[i]
        if _c == 'B':  # From all position word[i] letter should be removed
            for j in range(len(patt)):
                if _x in patt[j]:
                    patt[j].remove(_x)
        elif _c == 'G':  # In the ith position only word[i] can be
            patt[i] = {_x}
        elif _c == 'Y':  # Remove word[i] letter from the current position
            if _x in patt[i]:
                patt[i].remove(_x)
        else:
            breakpoint()  # ???? Internal error


def deleteImpossibleWords():
    global patt, ws
    # Make a re from patt, e.g. [AKJBU][E]...
    r = ''
    for p in patt:
        r += '[' + ''.join(p) + ']'

    # Remove all the words from ws, which does NOT satisfy the regular expression
    wsc = ws.copy()
    for w in wsc:
        m = re.search(r, w, flags=re.I)
        if m is None:
            ws.remove(w)
    lwsc = len(wsc) ; lws = len(ws)
    print(f'{lwsc}-{lws}={lwsc-lws} impossible words were deleted')
    return r  # For further usage


def giveHints(r):  # r is the regular expression for filtering the words
    global patt

    """ exec() does NOT change pri, why ????
    pri = ite.product({1, 2}, {3, 4})  # Otherwise, pri will not be seen
    pr = 'pri = ite.product(patt[0]'
    for i in range(1, len(patt)):
        pr += f',patt[{i}]'
    pr += ')'
    exec(pr)  # pri is iterable for the Cartesian product, presented in tuples
    """
    pri = ite.product(patt[0], patt[1], patt[2], patt[3], patt[4])

    allWords = []
    for t in pri:
        allWords.append(''.join(t))

    print(
f"""As everywhere, case does NOT matter. The word isn't in the database. The word should
correspond to the next regular expression:
{r}
{len(allWords):,d} possible string can be generated. They will be printed in small groups,
if any of them is a meaningful word, please add it to the database.
After adding some words to the database, you can try again.
""")
    for i in range(len(allWords)):
        print(allWords[i])
        if i%15 == 14:
            print('If any meaningful word above, add it to the database.')
            if input("Hit Enter to continue, or 'q' to quit").lower().startswith('q'):
                exit(1)


#######################################################################
def main():
    global patt, ws
    # Double loop, the outher for repeating games, the inner to find the WORD.
    while True:
        getParameters()
        printInstruction()
        getWords_SetupGame()

        while True:
            if len(ws) == 1:
                print(f'\nThe Word might be: {ws[0][1]}\n')
                break

            recomm = ws[0]
            print(f'Try: {recomm}')
            # Process the answer from the Wordle game
            ans = input('Enter the first letter of the colors (or 9 to quit): ')
            ans = ans.upper()
            if ans[0] == '9':
                break
            ans = ans.split()  # At space, if any
            if len(ans) > 1:
                # The user overwrote the recommendation
                if isGoodWord(ans[0]):
                    recomm = ans[0]
                    ans.pop(0)
                else:
                    print(f"You entered a wrong word '{ans[0]}', your input is ignored")
                    continue
            if len(ans) != 1:
                print(f"You entered a wrong answer, please read the instruction.")
                continue

            colors = ans[0]  # It must be c.NUM_LETTERS long and containing [BGY] only
            if len(colors) != c.NUM_LETTERS:
                print(f"Your colors should contain {c.NUM_LETTERS} letters.")
                continue
            if len((re.search('[BGY]*', colors)).group(0)) != c.NUM_LETTERS:
                print(f"For the colors use 'b', 'g', or 'y', case insensitive.")
                continue

            reducePattern(recomm, colors)
            r = deleteImpossibleWords()
            # If anything left, continue the game
            if len(ws) > 0:
                continue

            # The word is NOT in the database.
            giveHints(r)
            break

        # End of inner while True
        if input('Do you want another assistance? (y/n): ').lower().startswith('n'):
            break


#######################################################################
if __name__ == '__main__':
    breakpoint()  # ???? DEBUG, to set other breakpoints
    main()
    print('\nThanks for using this program, any suggestion is welcomed.')
