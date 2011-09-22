from vendor.fuzzywuzzy import process


def match(word, possibilities):
    return process.extract(word, possibilities)
