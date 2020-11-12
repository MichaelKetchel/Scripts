import re
import argparse
# from pprint import pprint

parser = argparse.ArgumentParser(add_help=True, description='Generates possible word combinations valid in Scrabble')
parser.add_argument('letters', action="store")
parser.add_argument('pattern', action="store")
parser.add_argument('--file', '-f', action="store", dest="dictfile", default="ospd.txt",
                    help="The dictionary file to use")
args = parser.parse_args()

# Config
#letters = 'ordefbc'
#regex = r'^.*r.*\n'
letters = args.letters
regex = f"^{args.pattern}\n"
filename = args.dictfile

# Constants
letter_values_base = {
    ' ': 0,
    'eaionrtlsu': 1,
    'dg': 2,
    'bcmp': 3,
    'fhvwy': 4,
    'k': 5,
    'jx': 8,
    'qz': 10,
}
letter_values = {}
for ltrs, value in letter_values_base.items():
    letter_values.update({ltr: value for ltr in ltrs})

# Letter analytics
re_letters = ''.join(re.findall(r'(?<!\\)[a-zA-Z]', regex))
check_letters = letters + re_letters
letterCounts = {letter: check_letters.count(letter) for letter in set(check_letters)}

# Grab potential values to check more closely
results = [line.rstrip('\n') for line in open(filename) if re.match(regex, line)]

# Make sure words don't contain letters we don't have.
eligible = []
valuated = []
for word in results:
    keep = True
    value = 0
    remaining_blanks = letterCounts.get('_', 0)
    availableLetters = letterCounts.copy()

    for letter in word:
        availableLetter = availableLetters.get(letter, 0)
        wordLetterCount = word.count(letter)

        if not availableLetter:
            if remaining_blanks > 0:
                remaining_blanks -= 1
                continue
            else:
                keep = False
                break
        availableLetters[letter] -= 1
        value = value + letter_values[letter]
    if keep:
        eligible.append(word)
        valuated.append((value, word))

# Sort

# Print
valuated.sort(key=lambda x: x[0])
for value in valuated:
    print("%s: %s" % value)
