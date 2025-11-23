from arabica import arabica_freq
import pandas
import random
import re

def blend(text1, text2, num_lines=5):
    poem = []
    text1_unigrams, text1_trigrams = find_ngrams(text1)
    text2_unigrams, text2_trigrams = find_ngrams(text2)

    intersection = text1_unigrams.intersection(text2_unigrams)

    for i in range(num_lines):
        line = []
        bridge_word = random.choice(list(intersection))

        if i % 2 == 0:
            prefix = choose_prefix(text1_trigrams, bridge_word)
            suffix = choose_suffix(text2_trigrams, bridge_word)
        else:
            prefix = choose_prefix(text2_trigrams, bridge_word)
            suffix = choose_suffix(text1_trigrams, bridge_word)

        prefix = prefix.split(',')
        suffix = suffix.split(',')

        line.append(prefix[:2])
        line.append([bridge_word])
        line.append(suffix[1:])
        poem.append(line)

    return poem

# Helper functions

def find_ngrams(text):
    df = arabica_freq(text = [text],
             time = "",
             date_format = 'us',              # Use US-style date format to parse dates
             time_freq = 'ungroup',           # Calculate n-grams frequencies without period aggregation
             max_words = 10000,                  # Display 10 most frequent unigrams, bigrams, and trigrams
             stopwords = ['english'],         # Remove English set of stopwords
             stopwords_ext = [''],     # Remove extended list of English stopwords
             skip = ['<br />'],               # Remove additional strings. Cuts the characters out without tokenization, useful for specific or rare characters. Be careful not to bias the dataset.
             numbers = True,                  # Remove numbers
             lower_case = True)
    
    unigrams = set(df["unigram"][:1000])
    trigrams = list(df["trigram"])

    return unigrams, trigrams

def choose_prefix(trigrams, bridge_word):
    pre_pattern = re.compile(fr'{bridge_word}$') # Regex expression for 'ends with' bridge word 
    options = [s for s in trigrams if pre_pattern.search(s)]
    if options:
        prefix = random.choice(options)
    else:
        prefix = ""
    return prefix

def choose_suffix(trigrams, bridge_word):
    post_pattern = re.compile(fr'^{bridge_word}') # Regex expression for 'starts with' bridge word.
    options = [s for s in trigrams if post_pattern.search(s)]
    if options:
        suffix = random.choice(options)
    else:
        suffix = ""
    return suffix

# Example of use:

with open("Thus_Spake_Zarathustra.txt", "r", encoding="utf-8") as f:
    zarathustra = f.read()

with open("Microsoft_Services_Terms_and_Conditions.txt", "r", encoding="utf-8") as f:
    microsoft = f.read()

print(blend(zarathustra, microsoft, 10))
