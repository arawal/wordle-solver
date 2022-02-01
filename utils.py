import pandas as pd
from collections import Counter

def get_score(w, c):
    s = 0
    
    # remove duplicate chars
    w = ''.join(set(w))
    
    for l in w:
        s += c[l]

    return s

def generate_word_scores_from_populace(words_list, special = {}):
    # get most used alphabets
    vowel_counts = Counter(
        letter for word in words_list for letter in word if letter in "aeiou")
    vowel_totals = sum(vowel_counts.values())
    vowel_counts = {k: v/vowel_totals for k, v in vowel_counts.items()}

    consonant_counts = Counter(
        letter for word in words_list for letter in word if letter not in "aeiou ")
    consonant_totals = sum(consonant_counts.values())
    consonant_counts = {k: 4.2*v/consonant_totals for k, v in consonant_counts.items()}

    consonant_counts.update(vowel_counts)
    counts = consonant_counts
    # counts = Counter(
    #     letter for word in words_list for letter in word)
    
    for k, _ in counts.items():
        if "pos" in special and k in special["pos"]:
            counts[k] *= 2
        elif "final" in special and k in special["final"]:
            counts[k] *= 3

    # sort words with most used alphabets
    # this will be used as first suggestion
    word_scores = {}
    for word in words_list:
        word_scores[word] = get_score(word, counts)

    word_scores = dict(
        sorted(word_scores.items(), key=lambda item: item[1], reverse=True))

    word_scores = {k: v for k, v in word_scores.items() if v != 0}
    
    return word_scores

def preprocess():
    # get all 5 letter words
    with open('all_words.txt') as f:
        lines = f.readlines()

    words_list = []
    for line in lines:
        words_list.extend(line.split(' '))

    words_list = [word.lower() for word in words_list]

    word_scores = generate_word_scores_from_populace(words_list)
    
    df = pd.DataFrame.from_dict(word_scores, orient="index", )
    df.to_csv("word_scores.csv")
