import re

# letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# print (dict(zip(letters, LANGUAGES["English"]))["o"])
# print (dict(zip(letters, LANGUAGES["English"])))
# [8.2, 1.5, 2.8, 4.3, 13, 2.2, 2, 6.1, 7, 0.15, 0.77, 4, 2.4, 6.7, 7.5, 1.9, 0.095, 6, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2, 0.074]

LANGUAGES = {
    "English": {
        "Statistics": {"e": 13, "t": 9.1, "a": 8.2, "o": 7.5, "i": 7, "n": 6.7, "s": 6.3, "h": 6.1, "r": 6, "d": 4.3, "l": 4, "u": 2.8, "c": 2.8, "w": 2.4, "m": 2.4, "f": 2.2, "y": 2, "g": 2, "p": 1.9, "b": 1.5, "v": 0.98, "k": 0.77, "x": 0.15, "j": 0.15, "q": 0.095, "z": 0.074},
        "Most Common Words": ["the", "of", "a", "that", "which"] # http://norvig.com/mayzner.html --- most common words with each different length; 5
    }
}

def align(sign, spaces = None, depend = None):
    if spaces is None:
        if depend is None:
            raise Exception("Need something to depend")
        else:
            spaces = len(str(len(depend) + 1))
    return f"{'':<{spaces}}{sign}{'':<{spaces}}" # "{spaces}{sign}{spaces}" spaces = number of " "

def choose_language():
    possible_languages = {}

    while True:
        print ("====================")
        for i, language in zip(range(1, len(LANGUAGES) + 1), LANGUAGES):
            possible_languages[i] = language
            print (f"{i}{align('=', depend = LANGUAGES)}{language}")
        print ("====================")
        print ("P.S. This is based on statistics and does not always decode the words. It will also not work if the words are misspelled and/or using multiple languages at the same time... as of the moment. It is most effective in long texts")

        try:
            return possible_languages[int(input("Choose the likely language used by encoded words: "))]
        except KeyError:
            print ("I'm sorry, but your choice is not valid. Please try again.\n")

def find_frequency(text, string_length = None):
    text = text.lower()

    if string_length is None:
        pattern = r"[a-z]"
    else:
        pattern = r"\b[a-z]{%s}\b" % string_length
    text = re.findall(pattern, text) # To future me: (?=()) means ahead lookup, you can use re.findall(pattern, text)
    length = len(text)

    statistics = {}

    unique = set(text)
    for unique_element in unique:
        statistics[unique_element] = (text.count(unique_element) / length) * 100

    return statistics

def custom_binary_search(stat, x):
    low = 0
    high = len(stat) - 1

    stat = list(stat.items())

    if x > stat[low][1]:
        return 101
    elif x < stat[high][1]:
        return -101

    while low <= high:
        mid = (high + low) >> 1

        if stat[mid][1] < x:
            high = mid - 1
        elif stat[mid + 1][1] > x:
            low = mid + 1
        elif stat[mid][1] > x >= stat[mid + 1][1]:
            return stat[mid + 1][0]

def convert(text, key):
    text = list(text)
    text = [key[i] if i in key else key[i.lower()].upper() if i.lower() in key else i for i in text]
    text = ''.join(letter for letter in text)
    print (text)

def decode(text, language):
    old_letter_statistics = LANGUAGES[language]["Statistics"].copy()
    conversion = {}

    # First hint: common words
    most_common_words = []
    for common_word in LANGUAGES[language]["Most Common Words"]:
        output = find_frequency(text, len(common_word))
        most_common_words.append(sorted(output.items(), key = lambda x:x[1])[len(output) - 1][0])

    output = find_frequency(text)
    new_letter_statistics = dict(reversed(sorted(output.items(), key = lambda x:x[1])))

    for common_word, most_common_word in zip(LANGUAGES[language]["Most Common Words"], most_common_words):
        print (common_word, most_common_word)
        for oldletter, newletter in zip(common_word, most_common_word):
            if newletter not in conversion:
                conversion[newletter] = oldletter
                try:
                    del old_letter_statistics[oldletter]
                    del new_letter_statistics[newletter]
                except KeyError:
                    pass

    # Letter stats
    lowest = []
    # candidates = {}
    for letter, stat in list(new_letter_statistics.items()):
        outcome = custom_binary_search(old_letter_statistics, stat)
        if outcome == 101:
            if letter not in conversion:
                conversion[letter] = list(old_letter_statistics.items())[0][0]
                del old_letter_statistics[list(old_letter_statistics.items())[0][0]]
                del new_letter_statistics[letter]
        elif outcome == -101:
            lowest.append((letter, stat))
        else:
            if letter not in conversion:
                conversion[letter] = outcome
                del old_letter_statistics[outcome]
                del new_letter_statistics[letter]
    
    for letter in reversed(lowest):
        outcome = list(old_letter_statistics.items())[len(old_letter_statistics) - 1][0]
        if letter not in conversion:
            conversion[letter] = outcome
            del old_letter_statistics[outcome]
            del new_letter_statistics[letter]

    # print (old_letter_statistics)
    # print (new_letter_statistics)
    print (conversion)
    convert(text, conversion)

language = choose_language()

text = r'''
Aol Hymhp pujpklua (Pukvulzphu: Wlypzapdh Hymhp) dhz h zrpytpzo iladllu Pukvulzphu Hytf zvskplyz huk Myll Whwbh Tvcltlua mpnoalyz ihjrlk if svjhs zftwhaopglyz vu 28 Qbsf 1965, dolyl aol mpnoalyz shbujolk h yhpk hnhpuza hu Pukvulzphu ihyyhjrz pu hu haaltwa av jhwabyl mpylhytz.
'''

# The Arfai incident (Indonesian: Peristiwa Arfai) was a skirmish between Indonesian Army soldiers and Free Papua Movement fighters backed by local sympathizers on 28 July 1965, where the fighters launched a raid against an Indonesian barracks in an attempt to capture firearms. # https://en.wikipedia.org/wiki/Arfai_incident

decode(text, language)

# Unimplemented Ideas:
# Starting with the longest word, using the letters you already know because of the most common word, imput it in a Word Guesser, like https://github.com/Imaginatorix/Word-Guesser.
# Why was it not implemented?
# You need a database for each language, which is not ideal and practical for a small project like this.


