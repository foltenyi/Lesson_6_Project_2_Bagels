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
    DB_PATH  = 'C:/Users/folte/PycharmProjects/cs043/Lesson_6/Project_2_Bagels'
    DB_NAME  = 'words_00.db'
    TXT_PATH = 'C:/Users/folte/PycharmProjects/cs043/Lesson_6/Project_2_Bagels'
    TXT_NAME = 'w_05.txt'

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
This program will give suggestions which word to give to the Wordle game.
If you entered the first word, just enter the first letters of the colors the computer
answered. If you entered a different word, prepend it. E.g. for 5 letter words:
bgbyy        - if you entered the first (or only) suggested word
frame gbyby  - if you entered 'frame', not the first of the suggested word
If the solution word was not found, please add it to the words storage, which
can be a text file, order doesn't matter, but try to keep it ordered.
If the suggested word was not accepted by Wordle, please delete it, or
comment out by puting '#' in the first column.
For adding / deleting / editing words in the SQLite database you can use
DB Browser for SQLite utility program.
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


# The input of the words can be from SQLite database or a text file containing
# one word per line
def getWords_SetupGame():
    global az, c, ws, patt
    while True:  # To get 's' or 't'
        _a = input('How to get the words? From SQLite or text file (s/t): ').lower()
        _ws = []
        if _a[0] == 's':
            db = c.DB_PATH + '/' + c.DB_NAME
            connection = sqlite3.connect(db)  # words is a table in this db
            cursor = connection.cursor()
            tn = f'words_{c.NUM_LETTERS:02d}'
            _wt = cursor.execute(f'SELECT * FROM {tn}').fetchall()
            connection.close()
            # Get the words from the tuples
            for t in _wt:
                _ws.append(t[0])
            break
        elif _a[0] == 't':
            tx = c.TXT_PATH + '/' + c.TXT_NAME
            with open(tx) as f:
                while (w := f.readline()[:c.NUM_LETTERS]):
                    if w[0] == '#':
                        continue  # Allow comment line
                    _ws.append(w)
            break
        else:
            print("Please enter 's' or 't'.")

    _wc = _ws.copy()
    for _w in _wc:  # _w is a word, might be the solution
        if not isGoodWord(_w):
            print(f"Delete or correct '{_w}'.")
            _ws.remove(_w)

    # Upper case all words
    lw = []  # Will be list of all upper case words
    for i in range(len(_ws)):
        lw.append(_ws[i].upper())

    # Fill up _t with (n,word)
    _t = []
    # Make the sets first, only once.
    _s = []
    for z in lw:
        _s.append(set(z))
    for i in range(len(lw)):
        n = 0
        # if i%500 == 499: ???? How to print on the same line
        #     print(f"{i+1:,d}.  {lw[i]}", end='\r')
        for j in range(len(lw)):
            n += len(_s[i] & _s[j])
        _t.append((n, lw[i]))

    _t.sort(reverse=True)
    # Take out the words keeping the order
    """
    breakpoint()  # ???? DEBUG
    # Generate a 1st word, which contains the most frequently used letter in that position
    # JUST VALID WORDS CAN BE ENTERED, BY THE WAY 'EEEEE' WAS GENERATED
    fr = dict(zip(az, [0]*len(az)))
    lfr = []
    for _ in range(c.NUM_LETTERS):
        lfr.append(fr)

    ws = ["SOMETHING"]  # ws = []
    for x in _t:
        w = x[1]
        for i in range(len(w)):
            lfr[i][w[i]] += 1  # This letter in this position
        ws.append(w)
    # Generate the very first word
    myword = ''
    for i in range(len(lfr)):
        # lfr[i] is a dictionary, I don't know how to sort by value
        count = 0
        for k, v in lfr[i].items():
            if v > count:
                chr = k; count = v
        myword += chr
    ws[0] = myword  # Hopefully the answer from the computer will be useful
    """
    ws = ['XYZ']
    # Pick up the words with the most 'E's
    eee = []; cnt = 0
    for x in _t:
        w = x[1]
        if (_c := w.count('E')) >= cnt:
            if _c > cnt:
                cnt = _c; eee = []  # Restart
            eee.append(w)
        ws.append(w)
    # breakpoint()  # ???? DEBUG
    print(f"Words with {cnt} 'E's")
    print(re.sub("[',]", "", str(eee)[1:-1]))
    ws[0] = eee[0]
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
    for i in range(len(patt)):
        if len(patt[i]) == 0:
            print(f'Inconsistent color in column {i+1}')
            exit(1)


def deleteImpossibleWords():
    global patt, ws
    # Make a re from patt, e.g. [AKJBU][E]...
    r = ''
    for p in patt:
        r += '[' + ''.join(p) + ']'

    print("Delete words, which does NOT correspond to the regular expression:")
    print(f'{r}')
    # breakpoint()  # ???? DEBUG
    # Remove all the words from ws, which does NOT satisfy the regular expression
    wsc = ws.copy()
    for w in wsc:
        m = re.search(r, w, flags=re.I)
        if m is None:
            ws.remove(w)
    lwsc = len(wsc) ; lws = len(ws)
    print(f'{lwsc}-{lws}={lwsc-lws} impossible words were deleted')


def giveHints():  # r is the regular expression for filtering the words
    global patt

    print('\nThe solution word is NOT in the storage, after finding it,')
    print('please add it to the text file or the SQLite database\n')
    r = ''
    for p in patt:
        r += '[' + ''.join(p) + ']'
    """
    # exec() does NOT change pri, why ????
    breakpoint()  # ???? DEBUG
    pr = 'ite.product(patt[0]'
    for i in range(1, len(patt)):
        pr += f',patt[{i}]'
    pr += ')'
    pri = exec(pr)  # pri is iterable for the Cartesian product, presented in tuples
    """
    # For 5-letter words
    pri = ite.product(patt[0], patt[1], patt[2], patt[3], patt[4])

    allWords = []
    for t in pri:
        allWords.append(''.join(t))

    print(
f"""As everywhere, case does NOT matter. The missing word should
correspond to the next regular expression:
{r}
{len(allWords):,d} possible strings can be generated. They will be printed in small
groups, if any of them is a meaningful word, please add it to the word storage.
After adding some words, you can try again.
""")
    for i in range(len(allWords)):
        print(allWords[i])
        if i%15 == 14:
            print('If any meaningful word above, add it to the choose-able words.')
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
                print(f'\nThe Word might be: {ws[0]}\n')
            if len(ws) > 1:
                print('Here are some recommended words:')
                print(re.sub("[',]", "", str(ws[:12])[1:-1]))

            recomm = ws[0]
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
                printInstruction()
                continue

            colors = ans[0]  # It must be c.NUM_LETTERS long and containing [BGY] only
            if len(colors) != c.NUM_LETTERS:
                print(f"Your colors should contain {c.NUM_LETTERS} letters.")
                continue
            if len((re.search('[BGY]*', colors)).group(0)) != c.NUM_LETTERS:
                print(f"For the colors use 'b', 'g', or 'y', case insensitive.")
                continue

            if colors == "G"*c.NUM_LETTERS:
                break  # THE WORD IS FOUND
            reducePattern(recomm, colors)
            deleteImpossibleWords()
            # If anything left, continue the game
            # breakpoint()  # ???? DEBUG
            if len(ws) > 0:
                continue

            # The word is NOT in the database.
            giveHints()
            break

        # End of inner while True
        if input('Do you want another assistance? (y/n): ').lower().startswith('n'):
            break


#######################################################################
if __name__ == '__main__':
    # breakpoint()  # ???? DEBUG, to set other breakpoints
    main()
    print('\nThanks for using this program, any suggestion is welcomed.')
