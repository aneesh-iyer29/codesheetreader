from multiprocessing import Value
from tokenize import String
import pandas as pd
import random
import math
import os
import re
import subprocess
import numpy as np
import unicodedata

# Aristocrat_Code

# monoalphabetic
def aristo_letter_replacement(s, keyword="", shift="", alph=""):
    def derangement(lst):
        """Generate a derangement of lst"""
        while True:
            result = lst[:]
            random.shuffle(result)
            if all(x != y for x, y in zip(lst, result)):
                return result

    def randomize_string_no_same_position(alphabet):
        char_list = list(alphabet)
        deranged_list = derangement(char_list)
        randomized_string = ''.join(deranged_list)
        return randomized_string
    if alph == "":
        alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        replacement_alphabet = randomize_string_no_same_position(alphabet_upper)
    elif alph == "K2":
        alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        replacement_alphabet = process_word(keyword, shift).upper()
    elif alph == "K1":
        alphabet_upper = process_word(keyword, shift).upper()
        replacement_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        alphabet_upper = process_word(keyword,0).upper()
        replacement_alphabet = process_word(keyword, 26 - shift).upper()

    for i in range(26):
        if alphabet_upper[i] == replacement_alphabet[i]:
            raise ValueError("Cannot have a letter map to itself; check your keys")
    translation_table = str.maketrans(alphabet_upper, replacement_alphabet)
    replaced_string = s.upper().translate(translation_table)
    
    return replaced_string

def aristo_format_sentence(s):
    words = s.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    lines = 1
    for word in words:
        if total_length + len(word) + 1 > 52:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
            lines +=1
        else:
            current_line += word + " "
            total_length += len(word) + 1    
    formatted_string += current_line.rstrip()
    formatted_string += "\n"
    return formatted_string

def pat_format_sentence(s):
    q = ""
    s = re.sub(r'[^a-zA-Z]', '', s)
    for i in range(len(s)):
        q += s[i]
        if (i % 5 == 4):
            q += " "
    
    words = q.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    lines = 1
    for word in words:
        if total_length + len(word) + 1 > 52:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
            lines+=1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    
    formatted_string += current_line.rstrip()
    formatted_string += "\n"
    return formatted_string

def aristo_frequency_table(ct, alph):
    if alph == "K2":
        o = ''''''
        o += 'Replacement'
        for i in range(26):
            o += '&'
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += "K2"
        for i in range(26):
            o += '&'
            o += chr(i+65)
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += 'Frequency'
        for i in range(26):
            o += '&'
            o += str(ct.count(chr(i+65)))         
        o += '\\\\'    
        return(o)
    else:
        o = f'''{alph}'''
        for i in range(26):
            o += '&'
            o += chr(i+65)
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += 'Frequency'
        for i in range(26):
            o += '&'
            o += str(ct.count(chr(i+65))) 
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += 'Replacement'
        for i in range(26):
            o += '&'
        o += '\\\\'    
        return(o)

def process_word(word, shift):
    seen = set()
    unique_letters = []
    word = word.lower().replace(" ","")
    for char in word:
        if char not in seen:
            unique_letters.append(char)
            seen.add(char)
    
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    
    unused_letters = sorted(alphabet - seen)
    
    result = ''.join(unique_letters) + ''.join(unused_letters)
    
    shift = shift % len(result)  
    
    shifted_result = result[-shift:] + result[:-shift]
    return shifted_result

def monoalph_creator(s, value, type, hint_type, hint, alph="", keyword="", shift="", extract = False):
    replaced_string = aristo_letter_replacement(s, keyword, shift, alph)
    if type == "Aristocrat":
        formatted_string = aristo_format_sentence(replaced_string)
    if type == "Patristocrat":
        formatted_string = pat_format_sentence(replaced_string)
        replaced_string = re.sub(r'[^a-zA-Z]', '', replaced_string)
    table = aristo_frequency_table(replaced_string, alph)
    if alph != "":
        alph += " "
    
    if not extract:
        v = "\\normalsize \\question[" + str(value) + "] Solve this \\textbf{" + alph + type + "}"
    else:
        if type == "Aristocrat":
          v = "\\normalsize \\question[" + str(value) + "] The following quote was encoded as an \\textbf{" + type + "} with a " + alph + " alphabet"
        elif type == "Xenocrypt":
              v = "\\normalsize \\question[" + str(value) + "] The following quote was encoded as a \\textbf{" + type + "} with a " + alph + " alphabet"
        elif type == "Patristocrat":
            v = "\\normalsize \\question[" + str(value) + "] The following quote was encoded as a \\textbf{" + type + "} with a " + alph + " alphabet"
    if hint_type == "None":
        v += ".\n"
    elif hint_type == "Word" or hint_type == "Letters":
        v+= ". You are told that " + hint + ".\n"
    elif hint_type == "Word + Subject" or hint_type == "Letters + Subject":
        hint = hint.split(",")
        v+= " about " + hint[1] + ". You are told that " + hint[0] + ".\n"
    elif hint_type == "Subject":
        v+= f" about {hint}."
    else:
        v+=". "
    if extract:
        v+=f"You are told that the keyword used is {len(keyword)} letters long. What is the keyword? "
        v+="$\\boxed{\\text{Box}}$ your final answer."
    v += "\n\\Large{\n"
    v += "\\begin{verbatim}\n"
    v += formatted_string + "\n"
    v += "\\end{verbatim}}\n"
    v += "{\\normalsize\n"
    v += "\\begin{center}\n"
    v += "\\begin{tabular}\n"
    v += "{|m{2cm}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|}\n"
    v += "\\hline\n"
    v += table + "\n"
    v += "\\hline\n"
    v += "\\end{tabular}\n"
    v += "\\end{center}}\n"
    v += "\\vfill\n"
    v += "\\uplevel{\\hrulefill}\n"
    return v

# atbash

def atbash(text):
    text = re.sub(r'[^a-zA-Z]', '', text).upper()
    reverse_mapping = {chr(i): chr(155 - i) for i in range(65, 91)}  # A-Z to Z-A
    reversed_text = ''.join(reverse_mapping.get(char, char) for char in text)
    return reversed_text

def atbash_encoder(text, bs, value):
    t = atbash(text)
    v = ""
    for i in range(len(t)):
        v += t[i]
        if (i + bs > 52):
            v += "\n\n\n"
        if (i % bs == bs - 1):
            v += " "
    result = []
    result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Atbash}} cipher.")
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{v}\n")
    result.append("\\end{verbatim}}\n")
    result.append("\\vfill")
    result.append("\\uplevel{\\hrulefill}")
    
    return "\n".join(result)

# BACONIAN

# baconian letters

def baconLetterEncoder(s, a, b, lw, type):
    baconed = ""
    encoded = ""
    # Coerce to string so numeric keys from Excel (e.g. 134, 689) work
    a = list(str(a))
    b = list(str(b))
    s = s.upper().replace(" ", "")
    alphabet = {
        "A": "AAAAA",
        "B": "AAAAB",
        "C": "AAABA",
        "D": "AAABB",
        "E": "AABAA",
        "F": "AABAB",
        "G": "AABBA",
        "H": "AABBB",
        "I": "ABAAA",
        "J": "ABAAA",
        "K": "ABAAB",
        "L": "ABABA",
        "M": "ABABB",
        "N": "ABBAA",
        "O": "ABBAB",
        "P": "ABBBA",
        "Q": "ABBBB",
        "R": "BAAAA",
        "S": "BAAAB",
        "T": "BAABA",
        "U": "BAABB",
        "V": "BAABB",
        "W": "BABAA",
        "X": "BABAB",
        "Y": "BABBA",
        "Z": "BABBB"
    }
    for let in s:
        baconed += alphabet[let]
    x = 0
    y = 0
    if type == "LETTERS":
        for let in baconed:
            if let == "A":
                encoded += a[x]
                x += 1
                if x == len(a):
                    x = 0
            if let == "B":
                encoded += b[y]
                y += 1
                if y == len(b):
                    y = 0
    if type == "RANDOM LETTERS":
        for let in baconed:
            if let == "A":
                encoded += a[random.randint(0, len(a) - 1)]
            if let == "B":
                encoded += b[random.randint(0, len(b) - 1)]
    if type == "SEQUENCE":
        for let in baconed:
            if let == "A":
                encoded += a[x]
                x += 1
                if x == len(a):
                    x = 0
            if let == "B":
                encoded += b[x]
                x += 1
                if x == len(b):
                    x = 0   
    spaced = ""
    lines = 1
    for i in range(len(encoded)):
        spaced += encoded[i]
        if (i % lw == lw - 1):
            spaced += "\n\n\n"
            lines +=1
    return spaced

def baconianLetters(s, a, b, lw, value, type, hint_type, hint, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s).upper()
    t = baconLetterEncoder(s, a, b, lw, type)
    result = []
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    if hint_type == "Letters":
        result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Baconian}} cipher. You are told that {hint}.{bonus_text}")
    else:
        result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Baconian}} cipher.{bonus_text}")
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{t}\n")
    result.append("\\end{verbatim}}\n")
    result.append("\\vfill")
    result.append("\\uplevel{\\hrulefill}")
    
    return "\n".join(result)
    
# baconian words

def words(s,alph):
    s = baconWordsEncoder(s)
    alph = alph.replace(" ","")
    alph += alph + alph + alph + alph + alph + alph + alph + alph + alph + alph + alph + alph + alph
    alph = alph[0:26]
    alph = alph.upper()
    s=s.upper()
    a=""
    b=""
    worded=""
    x=0
    while x<26:
        l = alph[x]
        if l == "A":
            a += chr(x+65)
        if l == "B":
            b += chr(x+65)
        x+=1
    y=0
    while y<len(s):
        if s[y] == "A":
            first = a
        elif s[y] == "B":
            first = b
        if s[y+1] == "A":
            second = a
        elif s[y+1] == "B":
            second = b
        if s[y+2] == "A":
            third = a
        elif s[y+2] == "B":
            third = b
        if s[y+3] == "A":
            fourth = a
        elif s[y+3] == "B":
            fourth = b
        if s[y+4] == "A":
            fifth = a
        elif s[y+4] == "B":
            fifth = b
        words_list = get_matching_words(first,second,third,fourth,fifth)
        worded+=words_list[random.randint(0,len(words_list)-1)]
        worded += " "
        worded = worded.upper()
        y+=5
    return words_format_sentence(worded)
        
def baconWordsEncoder(s):
    baconed = ""
    encoded = ""
    s = s.replace(" ","").replace("'","").replace(".","").upper()
    alphabet = {
        "A": "AAAAA",
        "B": "AAAAB",
        "C": "AAABA",
        "D": "AAABB",
        "E": "AABAA",
        "F": "AABAB",
        "G": "AABBA",
        "H": "AABBB",
        "I": "ABAAA",
        "J": "ABAAA",
        "K": "ABAAB",
        "L": "ABABA",
        "M": "ABABB",
        "N": "ABBAA",
        "O": "ABBAB",
        "P": "ABBBA",
        "Q": "ABBBB",
        "R": "BAAAA",
        "S": "BAAAB",
        "T": "BAABA",
        "U": "BAABB",
        "V": "BAABB",
        "W": "BABAA",
        "X": "BABAB",
        "Y": "BABBA",
        "Z": "BABBB"
    }
    for let in s:
        baconed += alphabet[let]
    return baconed

def get_matching_words(first_letters, second_letters, third_letters, fourth_letters, fifth_letters):
    with open("sgb-words.txt", 'r') as file:
        words = file.read().splitlines()
    first_letters = first_letters.lower()
    second_letters = second_letters.lower()
    third_letters = third_letters.lower()
    fourth_letters = fourth_letters.lower()
    fifth_letters = fifth_letters.lower()
    
    matching_words = []
    for word in words:
        if (word[0] in first_letters and
            word[1] in second_letters and
            word[2] in third_letters and
            word[3] in fourth_letters and
            word[4] in fifth_letters):
            matching_words.append(word)
    
    return matching_words


def words_format_sentence(s):
    words = s.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    lines = 1
    for word in words:
        if total_length + len(word) + 1 > 58:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
            lines += 1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    
    formatted_string += current_line.rstrip()
    return formatted_string

def bacon_words_middle_hint(plaintext, crib, alph, encoded_sentence):
    pt_clean = re.sub(r'[^a-zA-Z]', '', plaintext).upper()
    crib_clean = re.sub(r'[^a-zA-Z]', '', crib).upper()

    crib_start = pt_clean.find(crib_clean)
    if crib_start == -1:
        raise ValueError(f"Crib '{crib}' not found in plaintext '{pt_clean}'")

    # Each plaintext letter → 1 output word (5 bits select one word)
    word_offset = crib_start
    crib_word_count = len(crib_clean)

    all_words = encoded_sentence.split()
    crib_words = all_words[word_offset: word_offset + crib_word_count]
    crib_words_str = " ".join(crib_words)

    char_start = crib_start + 1
    char_end = crib_start + len(crib_clean)

    return crib_words_str, char_start, char_end


def baconianWordsFormatter(s, alph, crib, value, hint_type, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s)
    t = words(s, alph)
    result = []
    bonus_text = ""
    if bonus:
        bonus_text = " \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"

    # ── Auto-detect hint type from crib position in plaintext ───────────────
    if crib:
        pt_clean   = s.upper()
        crib_clean = re.sub(r'[^A-Z]', '', crib.upper())
        try:
            hint_type = detect_hint_type(pt_clean, crib_clean)
        except ValueError as e:
            print(f"[baconianWordsFormatter detect WARNING] {e}")

    if hint_type == "Start Crib":
        result.append(
            f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
            f"\\textbf{{Baconian}} cipher. You are told that the plaintext starts with "
            f"\\textbf{{{crib}}}.{bonus_text}"
        )
    elif hint_type == "End Crib":
        result.append(
            f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
            f"\\textbf{{Baconian}} cipher. You are told that the plaintext ends with "
            f"\\textbf{{{crib}}}.{bonus_text}"
        )
    elif hint_type == "Middle Crib":
        try:
            crib_words_str, char_start, char_end = bacon_words_middle_hint(s, crib, alph, t)
            result.append(
                f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
                f"\\textbf{{Baconian}} cipher. You are told that the plaintext contains "
                f"\\textbf{{{crib}}}, encoding to \\textbf{{{crib_words_str}}}, "
                f"or characters {char_start}-{char_end}.{bonus_text}"
            )
        except ValueError as e:
            print(f"[bacon_words_middle_hint WARNING] {e}\n  Falling back to plain crib text.")
            result.append(
                f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
                f"\\textbf{{Baconian}} cipher. You are told that the plaintext contains "
                f"\\textbf{{{crib}}}.{bonus_text}"
            )
    else:
        result.append(
            f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
            f"\\textbf{{Baconian}} cipher.{bonus_text}"
        )

    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{t}\n")
    result.append("\\end{verbatim}}\n")
    result.append("{\\normalsize")
    result.append("\\begin{flushleft}")
    result.append("\\begin{tabular}")
    result.append("{|m{2cm}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|}")
    result.append("\\hline")
    result.append("&A&B&C&D&E&F&G&H&I&J&K&L&M&N&O&P&Q&R&S&T&U&V&W&X&Y&Z\\\\")
    result.append("\\hline")
    result.append("Replacement&&&&&&&&&&&&&&&&&&&&&&&&&&\\\\")
    result.append("\\hline")
    result.append("\\end{tabular}")
    result.append("\\end{flushleft}}")
    result.append("\\vfill")
    result.append("\\uplevel{\\hrulefill}")

    return "\n".join(result)

# caesar

def caesar_encoder(s, shift, bs):
    if shift % 26 == 0:
        raise ValueError("Self-mapping is not allowed, change shift from 0")
    s = s.upper().replace(" ", "").replace("'", "").replace(",", "").replace(".", "")
    c = [ord(i) - 65 for i in s]
    encoded = []
    nospace = ""
    
    for ele in c:
        value = (ele + shift)%26
        
        encoded.append(chr(value + 65))
    
    nospace = ''.join(encoded)
    spaced = ""
    for i in range(len(nospace)):
        spaced += nospace[i]
        if (i % bs == bs - 1):
            spaced += " "
    return spaced

def caesar_format_sentence(s):
    words = s.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    lines = 1
    for word in words:
        if total_length + len(word) + 1 > 52:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
            lines +=1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    
    formatted_string += current_line.rstrip()
    return formatted_string

def caesar_formatter(s, shift, value, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s)
    encoded_text = caesar_encoder(s, shift, 5)
    formatted_string = caesar_format_sentence(encoded_text)
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result = []
    result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Caesar}} cipher.{bonus_text}")
    result.append("\n\\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{formatted_string}\n")
    result.append("\\end{verbatim}}")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")
    
    return "\n".join(result)

# columnar

def randomizeColumnarString(columns):
    string = ""
    x = 0
    letters = ""
    while x < columns:
        string += str(random.randint(0, 9))
        x += 1
    for i in string:
        letters += str(chr(int(i) + 65))
    return letters

def encryptColumnarMessage(msg, key):
    cipher = ""
    msg = msg.replace(" ", "").replace("'", "").replace(".", "").replace("?","").replace("!","").upper()
    # track key indices
    k_indx = 0

    msg_len = float(len(msg))
    msg_lst = list(msg)
    key_lst = sorted(list(key))

    # calculate the column of the matrix
    col = len(key)

    # calculate maximum row of the matrix
    row = int(math.ceil(msg_len / col))

    # add the padding character '_' in empty
    # the empty cell of the matix
    fill_null = int((row * col) - msg_len)
    msg_lst.extend('X' * fill_null)

    # create Matrix and insert message and
    # padding characters row-wise
    matrix = [msg_lst[i: i + col]
              for i in range(0, len(msg_lst), col)]

    # read matrix column-wise using key
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += ''.join([row[curr_idx]
                           for row in matrix])
        k_indx += 1

    return cipher

def columnarFormatter(s, columns, crib, value, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s)
    key = ""
    for i in range(columns):
        key += str(i)
    key = ''.join(random.sample(key,len(key)))
    t = encryptColumnarMessage(s, key)
    t = t.upper().replace(" ", "")
    
    spaced = ""
    for i in range(len(t)):
        spaced += t[i]
        if (i % 5 == 4):
            spaced += " "
    words = spaced.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    lines = 1
    for word in words:
        if total_length + len(word) + 1 > 52:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
            lines += 1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    formatted_string += current_line.rstrip()
    spaced = formatted_string
    
    result = []
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Complete Columnar}} cipher. You are told that the plaintext contains \\textbf{{{crib.upper()}}}.{bonus_text}")
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{spaced}\n")
    result.append("\\end{verbatim}}\n")
    result.append("\\vfill")
    result.append("\\uplevel{\\hrulefill}")
    
    return "\n".join(result)

def cryptarithm_formatter(value, solution_text, solution_numbers, operation, bonus):
    solution_text = solution_text.split(" ")
    solution_numbers = str(solution_numbers).split(" ")
    text_sol_numbers = " ".join(solution_numbers)
    math_solution_numbers = "\\:".join(solution_numbers)
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result = """\\normalsize \\question[""" + str(value) + """] Solve this \\textbf{cryptarithm} for $""" + math_solution_numbers + """$. Write out your final answer and $\\boxed{\\text{box}}$ it.""" + bonus_text + """
\\parskip 1cm

\\Large
\\begin{verbatim}
Base 10 """ + operation + """
Answer: """ + text_sol_numbers + """

    TEXAS
x     BED
---------
   MTIESS
   DAMSS
 ERDAAS
---------
 MISTRESS

\\end{verbatim}
\\vfill
\\uplevel{\\hrulefill}"""
    
    return result

# fractionated morse

def fracalphabet(keyword):
    keyword = keyword.upper()
    seen = set()
    keyword_unique = ''.join([c for c in keyword if not (c in seen or seen.add(c))])
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    remaining_letters = ''.join([c for c in alphabet if c not in keyword_unique])

    k1_alphabet = keyword_unique + remaining_letters
    return k1_alphabet

def morseCode(message):
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
        'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', "'": '', " ": ''
    }
    
    # Convert the message to uppercase
    message = message.upper()

    # Convert each character in the message to Morse code
    morse_message = ""
    for char in message:
        morse_message += morse_code_dict.get(char, '')
        morse_message += "x"
    return morse_message

def fractionatedEncoder(s, keyword):
    a = fracalphabet(keyword)
    b = [c for c in a]
    fmorse = {
        "...": b[0], "..-": b[1], "..x": b[2], ".-.": b[3], ".--": b[4],
        ".-x": b[5], ".x.": b[6], ".x-": b[7], ".xx": b[8], "-..": b[9],
        "-.-": b[10], "-.x": b[11], "--.": b[12], "---": b[13], "--x": b[14],
        "-x.": b[15], "-x-": b[16], "-xx": b[17], "x..": b[18], "x.-": b[19],
        "x.x": b[20], "x-.": b[21], "x--": b[22], "x-x": b[23], "xx.": b[24],
        "xx-": b[25]
    }
    if len(s.replace(" ", "")) % 3 == 1:
        s += "xx"
    if len(s.replace(" ", "")) % 3 == 2:
        s += "x"
    x = 0
    encoded = ""
    while x < len(s):
        temp = ""
        if s[x] in " ":
            x += 1
            encoded += " "
        temp += s[x]
        temp += s[x+1]
        temp += s[x+2]
        encoded += fmorse[temp]
        x += 3
    return encoded

def wordBreaker(s):
    message = morseCode(s)
    a = [char for char in message]
    morse = ""
    pending = ""
    x = 0
    while x < len(a) - 1:
        temp = ""
        temp += a[x]
        temp += a[x+1]
        if temp == "xx":
            if x % 3 == 0:
                morse += " "
                morse += a[x]
                pending = ""
            elif x % 3 == 1:
                morse += a[x]
                pending = " "
            elif x % 3 == 2:
                morse += a[x]
                morse += " "
                pending = ""
        else:
            morse += a[x]
            morse += pending
            pending = ""
        x += 1
    return morse
_MORSE_LETTERS = {
    'A': '.-',  'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',   'F': '..-.',
    'G': '--.',  'H': '....', 'I': '..',   'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--',   'N': '-.',   'O': '---',  'P': '.--.', 'Q': '--.-','R': '.-.',
    'S': '...',  'T': '-',   'U': '..-',  'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..'
}
_SYMBOL_MAP = {'.': "$\\newmoon$", '-': "-$\\,$", 'x': "$\\times$"}
 
 
def _frac_morse_stream(plaintext):
    """
    Convert plaintext to the full Fractionated Morse stream string.
    Letters are separated by a single 'x'; words are separated by 'xx'
    (i.e. the trailing letter-sep 'x' of the last letter + an extra 'x').
    This exactly mirrors the morseCode() / wordBreaker() pipeline.
    """
    plaintext = re.sub(r"[^\w\s]", "", plaintext).upper()
    stream = ""
    words = plaintext.split()
    for wi, word in enumerate(words):
        for ch in word:
            if ch not in _MORSE_LETTERS:
                continue
            stream += _MORSE_LETTERS[ch]
            stream += 'x'               # letter separator
        if wi < len(words) - 1:
            stream += 'x'               # extra x → xx total between words
    return stream
 
 
def _frac_crib_start_index(plaintext, crib):
    """
    Return the integer index where the crib's morse stream begins inside
    the full plaintext's morse stream.  Raises ValueError if not found.
    """
    crib_clean = re.sub(r"[^\w\s]", "", crib).upper().strip()
    crib_stream = _frac_morse_stream(crib_clean)
    full_stream = _frac_morse_stream(plaintext)
 
    idx = full_stream.find(crib_stream)
    if idx == -1:
        raise ValueError(
            f"Crib '{crib}' not found in morse stream.\n"
            f"  Full stream : {full_stream}\n"
            f"  Crib stream : {crib_stream}"
        )
    return idx
 
 
def frac_auto_hint(plaintext, crib, keyword):
    """
    Given the full plaintext, a crib word/phrase, and the encoding keyword,
    return a formatted hint string such as:
        "G = ●●×; O = –×●; S = ×●–; Z = ××–"
    sorted alphabetically by ciphertext letter.
 
    This works for Start, Middle, and End cribs — just pass the crib text.
    """
    keyword = keyword.replace(" ", "")
    crib_clean = re.sub(r"[^\w\s]", "", crib).upper().strip()
 
    # Build keyed trigram→letter map
    alpha = fracalphabet(keyword)
    b = list(alpha)
    fmorse_map = {
        "...": b[0], "..-": b[1], "..x": b[2], ".-.": b[3], ".--": b[4],
        ".-x": b[5], ".x.": b[6], ".x-": b[7], ".xx": b[8], "-..": b[9],
        "-.-": b[10], "-.x": b[11], "--.": b[12], "---": b[13], "--x": b[14],
        "-x.": b[15], "-x-": b[16], "-xx": b[17], "x..": b[18], "x.-": b[19],
        "x.x": b[20], "x-.": b[21], "x--": b[22], "x-x": b[23], "xx.": b[24],
        "xx-": b[25]
    }
 
    start_idx = _frac_crib_start_index(plaintext, crib_clean)
    crib_stream = _frac_morse_stream(crib_clean)
 
    # Pad front to align to trigram boundary, pad back to fill last trigram
    offset = start_idx % 3
    padded = ('x' * offset) + crib_stream
    while len(padded) % 3 != 0:
        padded += 'x'
 
    seen_pairs = {}
    for i in range(0, len(padded), 3):
        trigram = padded[i:i+3]
        if trigram not in fmorse_map:
            continue
        ct_letter = fmorse_map[trigram]
        pretty = ''.join(_SYMBOL_MAP[c] for c in trigram)
        # Exclude trigrams that are entirely padding (before or after the real crib)
        actual_start = i - offset
        actual_end   = actual_start + 3
        if actual_start >= 0 and actual_end <= len(crib_stream):
            seen_pairs[ct_letter] = pretty
 
    parts = [f"{ct} = {tri}" for ct, tri in sorted(seen_pairs.items())]
    return '; '.join(parts)
 
def frac_format_sentence(s):
    words = s.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    
    for word in words:
        if total_length + len(word) + 1 > 21:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    
    formatted_string += current_line.rstrip()
    return formatted_string

def fractionatedFormatter(s, keyword, crib, value, hint_type, hint, bonus):
    s = re.sub(r"[^\w\s]", "", s).upper()
    t = fractionatedEncoder(wordBreaker(s), keyword.replace(" ", ""))
    th = frac_format_sentence(t)
    th = th.replace(" ", "")
    display = "  "
    for i in range(len(th)):
        display += th[i]
        if (i % 1 == 0):
            display += "  "

    result = []
    bonus_text = ""
    if bonus:
        bonus_text = " \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"

    # ── Auto-detect hint type from crib position in plaintext ───────────────
    if crib:
        pt_nospace   = re.sub(r"[^\w]", "", s).upper()
        crib_nospace = re.sub(r"[^\w]", "", crib).upper()
        try:
            hint_type = detect_hint_type(pt_nospace, crib_nospace)
        except ValueError as e:
            print(f"[fractionatedFormatter detect WARNING] {e}")

    # ── Auto-generate the morse hint string ─────────────────────────────────
    auto_hint = hint  # safe fallback
    if hint_type in ("Start Crib", "Middle Crib", "End Crib"):
        try:
            auto_hint = frac_auto_hint(s, crib, keyword)
        except ValueError as e:
            print(f"[frac_auto_hint WARNING] {e}\n  Falling back to manual hint.")

    if hint_type == "Start Crib":
        result.append(
            f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
            f"\\textbf{{Fractionated Morse}} cipher. You are told the plaintext begins with "
            f"\\textbf{{{crib}}} corresponding to \\textbf{{{auto_hint}}}.{bonus_text}"
        )
    elif hint_type == "Middle Crib":
        result.append(
            f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
            f"\\textbf{{Fractionated Morse}} cipher. You are told the plaintext contains "
            f"\\textbf{{{crib}}} corresponding to \\textbf{{{auto_hint}}}.{bonus_text}"
        )
    elif hint_type == "End Crib":
        wb_stripped = wordBreaker(s).replace(" ", "")
        num_padding = (3 - len(wb_stripped) % 3) % 3
        extra_plural = "" if num_padding == 1 else "s"
        result.append(
            f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the "
            f"\\textbf{{Fractionated Morse}} cipher. You are told the plaintext ends with "
            f"\\textbf{{{crib}}} corresponding to \\textbf{{{auto_hint}}}"
            f" and \\textbf{{{num_padding} X{extra_plural} of padding}} at the very end.{bonus_text}"
        )
 
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{display}\n")
    result.append("\\end{verbatim}}\n")
    result.append("\\normalsize")
    result.append("\\begin{center}")
    result.append("\\begin{tabular}")
    result.append("{|m{2cm}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|}")
    result.append("\\hline")
    result.append("Replacement&&&&&&&&&&&&&&&&&&&&&&&&&&\\\\")
    result.append("\\hline")
    result.append("&$\\newmoon$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$-$&$-$&$-$&$-$&$-$&$-$&$-$&$-$&$-$&$\\times$&$\\times$&$\\times$&$\\times$&$\\times$&$\\times$&$\\times$&$\\times$\\\\")
    result.append("&$\\newmoon$&$\\newmoon$&$\\newmoon$&$-$&$-$&$-$&$\\times$&$\\times$&$\\times$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$-$&$-$&$-$&$\\times$&$\\times$&$\\times$&$\\newmoon$&$\\newmoon$&$\\newmoon$&$-$&$-$&$-$&$\\times$&$\\times$\\\\")
    result.append("&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$&$\\times$&$\\newmoon$&$-$\\\\")
    result.append("\\hline")
    result.append("\\end{tabular}")
    result.append("\\end{center}\n\n")
    result.append("\\vfill")
    result.append("\\uplevel{\\hrulefill}")
 
    return "\n".join(result)
 

# hill cipher

def hill_matrix(keyword):
    b = [ord(i) - 65 for i in keyword]
    if len(keyword) == 4:
        matrix=f"""\\[
            \\begin{{pmatrix}}{keyword[0]}&{keyword[1]}\\\\{keyword[2]}&{keyword[3]}\\end{{pmatrix}} = \\begin{{pmatrix}}{b[0]}&{b[1]}\\\\{b[2]}&{b[3]}\\end{{pmatrix}}
            \\]"""
    if len(keyword) == 9:
        z = [ord(i) - 65 for i in keyword]
        a = (z[4]*z[8] - z[5]*z[7]) % 26
        b = -(z[3]*z[8] - z[5]*z[6]) % 26
        c = (z[3]*z[7] - z[4]*z[6]) % 26
        d = -(z[1]*z[8] - z[2]*z[7]) % 26
        e = (z[0]*z[8] - z[2]*z[6]) % 26
        f = -(z[0]*z[7] - z[1]*z[6]) % 26
        g = (z[1]*z[5] - z[2]*z[4]) % 26
        h = -(z[0]*z[5] - z[2]*z[3]) % 26
        i = (z[0]*z[4] - z[1]*z[3]) % 26
        det = (a * z[0] + b * z[1] + c * z[2]) % 26
        det = pow(det, -1, 26)
        w = [(x * det) % 26 for x in [a, d, g, b, e, h, c, f, i]]
        matrix = f"""\\begin{{align*}}
        \\begin{{pmatrix}}{keyword[0]}&{keyword[1]}&{keyword[2]} \\\\ {keyword[3]}&{keyword[4]}&{keyword[5]} \\\\ {keyword[6]}&{keyword[7]}&{keyword[8]} \\end{{pmatrix}} = \\begin{{pmatrix}}{z[0]}&{z[1]}&{z[2]} \\\\ {z[3]}&{z[4]}&{z[5]} \\\\ {z[6]}&{z[7]}&{z[8]} \\end{{pmatrix}} \\qquad \\begin{{pmatrix}}{z[0]}&{z[1]}&{z[2]} \\\\ {z[3]}&{z[4]}&{z[5]} \\\\ {z[6]}&{z[7]}&{z[8]} \\end{{pmatrix}}^{{-1}} = \\begin{{pmatrix}}{w[0]}&{w[1]}&{w[2]} \\\\ {w[3]}&{w[4]}&{w[5]} \\\\ {w[6]}&{w[7]}&{w[8]} \\end{{pmatrix}}
        \\end{{align*}}"""
    
    return matrix

def hillEncoder(text, keyword):
    b = []
    c = []
    e = []
    text = text.upper().replace(" ", "")
    keyword = keyword.upper().replace(" ", "")
    for i in keyword:
        b.append(ord(i) - 65)
    for i in text:
        c.append(ord(i) - 65)
    if len(keyword) == 9:
        if len(c) % 3 == 1:
            c.extend([25, 25])
        elif len(c) % 3 == 2:
            c.append(25)
        d = 0
        while d < len(c):
            value1 = (b[0] * c[d] + b[1] * c[d+1] + b[2] * c[d+2]) % 26
            value2 = (b[3] * c[d] + b[4] * c[d+1] + b[5] * c[d+2]) % 26
            value3 = (b[6] * c[d] + b[7] * c[d+1] + b[8] * c[d+2]) % 26
            e.extend([chr(value1 + 65), chr(value2 + 65), chr(value3 + 65)])
            d += 3
        formatted_string = ""
        current_line = ""
        i = 0
        for char in e:
            if len(current_line) >= 72:
                formatted_string += current_line.rstrip() + "\n\n\n"
                current_line = f"{char} "
            else:
                current_line += char + " "
        formatted_string += current_line.rstrip()
        return formatted_string
    if len(keyword) == 4:
        if len(c) % 2 == 1:
            c.append(25)
        d = 0
        while d < len(c):
            value1 = (b[0] * c[d] + b[1] * c[d+1]) % 26
            value2 = (b[2] * c[d] + b[3] * c[d+1]) % 26
            e.append(chr(value1 + 65))
            e.append(chr(value2 + 65))
            d += 2
        formatted_string = ""
        current_line = ""
        for char in e:
            if len(current_line) >= 72:
                formatted_string += current_line.rstrip() + "\n\n\n"
                current_line = f"{char} "
            else:
                current_line += char + " "
        formatted_string += current_line.rstrip()
        return formatted_string

def hillCreater(s, keyword, value, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s).upper()
    keyword = keyword.upper().replace(" ", "")
    matrix = hill_matrix(keyword)
    formatted = hillEncoder(s,keyword)
    result = []
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Hill}} cipher and the encoding key \\textbf{{{keyword}}}.{bonus_text}")
    result.append(matrix)
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{formatted}\n")
    result.append("\\end{verbatim}}\n")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")

    return "\n".join(result)

# ── Shared helpers ────────────────────────────────────────────────────────────

def ordinal(n):
    """Return ordinal string: 1→'1st', 12→'12th', 23→'23rd', etc."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th'][min(n % 10, 4)]}"


def detect_hint_type(plaintext_clean, crib_clean):
    """
    Determine whether crib_clean sits at the Start, Middle, or End of
    plaintext_clean (both should already be stripped/uppercased).
    Returns one of: 'Start Crib', 'End Crib', 'Middle Crib'.
    Raises ValueError if the crib is not found at all.
    """
    if crib_clean not in plaintext_clean:
        raise ValueError(
            f"detect_hint_type: crib '{crib_clean}' not found in '{plaintext_clean}'"
        )
    if plaintext_clean.startswith(crib_clean):
        return "Start Crib"
    if plaintext_clean.endswith(crib_clean):
        return "End Crib"
    return "Middle Crib"


def nihilist_auto_hint(plaintext_clean, crib, key_clean, pk_clean):
    """
    Build the Middle Crib hint string for Nihilist, e.g.:
      'the 19th through 26th cipher units (72 68 27 76 45 55 28 74) decode to be ONTHEDEF'
    plaintext_clean: J→I replaced, non-alpha stripped, upper-cased.
    Raises ValueError if crib not found.
    """
    crib_clean = re.sub(r'[^A-IK-Z]', '', crib.upper().replace('J', 'I'))
    idx = plaintext_clean.find(crib_clean)
    if idx == -1:
        raise ValueError(
            f"nihilist_auto_hint: crib '{crib_clean}' not found in '{plaintext_clean}'"
        )
    b = create_nihilist_alphabet(pk_clean).upper()
    pk_dict = {b[i]: (i // 5 + 1) * 10 + (i % 5 + 1) for i in range(len(b))}
    encoded_all = []
    x = 0
    for let in plaintext_clean:
        encoded_all.append(pk_dict[let] + pk_dict[key_clean[x]])
        x = (x + 1) % len(key_clean)
    units = encoded_all[idx: idx + len(crib_clean)]
    units_str = ' '.join(str(u) for u in units)
    return (
        f"the {ordinal(idx + 1)} through {ordinal(idx + len(crib_clean))} cipher units "
        f"({units_str}) decode to be {crib_clean}"
    )


def porta_auto_hint(plaintext_clean, crib, keyword):
    """
    Build the Middle Crib hint string for Porta, e.g.:
      'the 12th through 15th cipher characters (SPXW) decode to be CAFE'
    plaintext_clean: non-alpha stripped, upper-cased.
    Raises ValueError if crib not found.
    """
    crib_clean = re.sub(r'[^A-Z]', '', crib.upper())
    idx = plaintext_clean.find(crib_clean)
    if idx == -1:
        raise ValueError(
            f"porta_auto_hint: crib '{crib_clean}' not found in '{plaintext_clean}'"
        )
    encoded_full = porta_encoder(plaintext_clean, keyword, 1).replace(' ', '')
    crib_ct = encoded_full[idx: idx + len(crib_clean)]
    return (
        f"the {ordinal(idx + 1)} through {ordinal(idx + len(crib_clean))} cipher characters "
        f"({crib_ct}) decode to be {crib_clean}"
    )


def checkerboard_auto_hint(plaintext_clean, crib, hkey, vkey, pk):
    """
    Build the Middle Crib hint string for Checkerboard, e.g.:
      'characters 27-34 (HT EG TG ET EI OH HT ET) decode to EPISODES'
    plaintext_clean: J→I replaced, non-alpha stripped, upper-cased.
    Raises ValueError if crib not found.
    """
    crib_clean = re.sub(r'[^A-IK-Z]', '', crib.upper().replace('J', 'I'))
    idx = plaintext_clean.find(crib_clean)
    if idx == -1:
        raise ValueError(
            f"checkerboard_auto_hint: crib '{crib_clean}' not found in '{plaintext_clean}'"
        )
    alph   = checkerboard_alphabet(pk).upper()
    hkey_u = hkey.upper()
    vkey_u = vkey.upper()
    pk_dict = {alph[j + i * 5]: vkey_u[i] + hkey_u[j]
               for i in range(5) for j in range(5)}
    pairs_str = ' '.join(pk_dict[let] for let in crib_clean)
    return (
        f"characters {idx + 1}-{idx + len(crib_clean)} "
        f"({pairs_str}) decode to {crib_clean}"
    )


# nihilist

def create_nihilist_alphabet(keyword):
    keyword = keyword.lower().replace('j', 'i')
    seen = set()
    keyword_unique = []
    
    for char in keyword:
        if char not in seen and char.isalpha():
            seen.add(char)
            keyword_unique.append(char)
    
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    for char in alphabet:
        if char not in seen:
            keyword_unique.append(char)
    
    return ''.join(keyword_unique)

def nihilistEncoder(s, key, pk, bs):
    b = create_nihilist_alphabet(pk).upper()
    s = s.replace(" ", "").replace("'", "").replace(".", "").upper()
    key = key.upper()
    
    pk_dict = {b[i]: (i // 5 + 1) * 10 + (i % 5 + 1) for i in range(len(b))}
    
    encoded = []
    x = 0
    for let in s:
        encoded.append(pk_dict[let] + pk_dict[key[x]])
        x += 1
        if x == len(key):
            x = 0
    
    y = ""
    z = 0
    for i in range(len(encoded)):
        y += str(encoded[i]) + " "
        if (i % bs == bs - 1):
            if bs == 1:
                z += 1
                if z == 16:
                    y += "\n\n\n"
                    z = 0
            elif bs < 7:
                y += "   "
                z += 1
                if z == 3:
                    y += "\n\n\n"
                    z = 0
            else:
                y += "   "
                z += 1
                if z == 2:
                    y += "\n\n\n"
                    z = 0
    
    return y

def nihilistFormatter(s, key, pk, bs, value, type, hint_type, hint, bonus):
    keyf = key.upper().replace("J","I").replace(" ","")
    s = s.upper().replace("J","I")
    s = re.sub(r'[^a-zA-Z]', '', s).upper()
    pkf = pk.upper().replace("J","I").replace(" ","")
    if type == "CRIB":
        v = nihilistEncoder(s, keyf, pkf, 1)
    else:
        if not bs:
            bs = 5
        v = nihilistEncoder(s, keyf, pkf, bs)
    
    result = []
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    if type == "DECODE":
        result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Nihilist Substitution}} cipher with a keyword of \\textbf{{{key}}} and a polybius key of \\textbf{{{pk}}}.{bonus_text}")
    elif type == "CRIB":
        # bs holds the crib text when type == "CRIB"
        crib_clean = re.sub(r'[^A-IK-Z]', '', bs.upper().replace('J', 'I'))
        try:
            hint_type = detect_hint_type(s, crib_clean)
        except ValueError as e:
            print(f"[nihilistFormatter detect WARNING] {e}")
        if hint_type == "Start Crib":
            result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Nihilist Substitution}} cipher. You are told that the keyword used to encode it is between 3 and 7 letters long and the plaintext begins with \\textbf{{{crib_clean}}}.{bonus_text}")
        elif hint_type == "End Crib":
            result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Nihilist Substitution}} cipher. You are told that the keyword used to encode it is between 3 and 7 letters long and the plaintext ends with \\textbf{{{crib_clean}}}.{bonus_text}")
        elif hint_type == "Middle Crib":
            try:
                auto_hint = nihilist_auto_hint(s, bs, keyf, pkf)
            except ValueError as e:
                print(f"[nihilist_auto_hint WARNING] {e}\n  Falling back to manual hint.")
                auto_hint = hint
            result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Nihilist Substitution}} cipher. You are told {auto_hint}.{bonus_text}")
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{v}\n")
    result.append("\\end{verbatim}}\n")
    result.append("{\\renewcommand{\\arraystretch}{1.2}")
    result.append("\\begin{tabular}{|C{18pt}|C{18pt}|C{18pt}|C{18pt}|C{18pt}|C{18pt}|}")
    result.append("\\hline")
    result.append("&1&2&3&4&5  \\\\")
    result.append("\\hline")
    result.append("1&&&&&  \\\\")
    result.append("\\hline")
    result.append("2&&&&&  \\\\")
    result.append("\\hline")
    result.append("3&&&&&  \\\\")
    result.append("\\hline")
    result.append("4&&&&&  \\\\")
    result.append("\\hline")
    result.append("5&&&&&  \\\\")
    result.append("\\hline")
    result.append("\\end{tabular}} \n")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")

    return "\n".join(result)

# porta

# porta
def porta_encoder(s, keyword, bs):
    s = s.upper()
    keyword = keyword.upper()
    b = [ord(i) - 65 for i in keyword]
    c = [ord(i) - 65 for i in s]
    encoded = []
    nospace = ""
    
    x = 0
    for ele in c:
        if ele < 13:
            value = (ele + math.floor(b[x] / 2)) % 13 + 13
        else:
            value = (ele - math.floor(b[x] / 2)) % 13
        x += 1
        if x == len(b):
            x = 0
        
        encoded.append(chr(value + 65))
    
    nospace = ''.join(encoded)
    spaced = ""
    for i in range(len(nospace)):
        spaced += nospace[i]
        if (i % bs == bs - 1):
            spaced += " "
    return spaced

def porta_format_sentence(s):
    words = s.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    
    for word in words:
        if total_length + len(word) + 1 > 52:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    
    formatted_string += current_line.rstrip()
    return formatted_string

def porta_formatter(s, keyword, bs, value, type, hint_type, hint, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s).upper()
    if type == "CRIB":
        crib = bs
        bs = 5
    encoded_text = porta_encoder(s, keyword, bs)
    formatted_string = porta_format_sentence(encoded_text)
    result = []
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    if type == "DECODE":
        result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Porta}} cipher with a keyword of \\textbf{{{keyword}}}.{bonus_text}")
    elif type == "CRIB":
        # Auto-detect hint type from crib position in plaintext
        crib_clean = re.sub(r'[^A-Z]', '', crib.upper())
        try:
            hint_type = detect_hint_type(s, crib_clean)
        except ValueError as e:
            print(f"[porta_formatter detect WARNING] {e}")
        if hint_type == "Start Crib":
            result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Porta}} cipher. You are told the plaintext begins with \\textbf{{{crib_clean}}}.{bonus_text}")
        elif hint_type == "Middle Crib":
            try:
                auto_hint = porta_auto_hint(s, crib, keyword)
            except ValueError as e:
                print(f"[porta_auto_hint WARNING] {e}\n  Falling back to manual hint.")
                auto_hint = hint
            result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Porta}} cipher. You are told {auto_hint}.{bonus_text}")
        elif hint_type == "End Crib":
            result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Porta}} cipher. You are told the plaintext ends with \\textbf{{{crib_clean}}}.{bonus_text}")
    result.append("\n\\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{formatted_string}\n")
    result.append("\\end{verbatim}}")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")
    return "\n".join(result)

# Xenocrypts

def remove_accents(s):
    result = ""
    for char in s:
        if char in ('ñ', 'Ñ'):
            result += char  # keep ñ as-is
            continue
        decomposed = unicodedata.normalize('NFD', char)
        base = ''.join(c for c in decomposed if unicodedata.category(c) != 'Mn')
        result += base
    return result

def xeno_letter_replacement(s, keyword="", shift="", alph=""):
    def derangement(lst):
        """Generate a derangement of lst"""
        while True:
            result = lst[:]
            random.shuffle(result)
            if all(x != y for x, y in zip(lst, result)):
                return result

    def randomize_string_no_same_position(alphabet):
        char_list = list(alphabet)
        deranged_list = derangement(char_list)
        randomized_string = ''.join(deranged_list)
        return randomized_string
    if alph == "":
        alphabet_upper = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        replacement_alphabet = randomize_string_no_same_position(alphabet_upper)
    elif alph == "K2":
        alphabet_upper = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        replacement_alphabet = xeno_process_word(keyword, shift).upper()
    elif alph == "K1":
        alphabet_upper = xeno_process_word(keyword, shift).upper()
        replacement_alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    elif alph == "K3":
        alphabet_upper = xeno_process_word(keyword,0).upper()
        replacement_alphabet = xeno_process_word(keyword,shift).upper()
    for i in range(27):
        if alphabet_upper[i] == replacement_alphabet[i]:
            raise ValueError("Cannot have a letter map to itself; check your keys")
    translation_table = str.maketrans(alphabet_upper, replacement_alphabet)
    replaced_string = s.upper().translate(translation_table)
    
    return replaced_string

def xeno_frequency_table(ct, alph):
    if alph == "K2":
        o = ''''''
        o += 'Replacement'
        for i in range(27):
            o += '&'
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += "K2"
        for i in range(14):
            o += '&'
            o += chr(i+65)
        o += "&Ñ"
        for i in range(14,26):
            o += '&'
            o += chr(i+65)
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += 'Frequency'
        for i in range(14):
            o += '&'
            o += str(ct.count(chr(i+65)))
        o += '&'
        o += str(ct.count(chr(209)))     
        for i in range(14,26):
            o += '&'
            o += str(ct.count(chr(i+65)))     
        o += '\\\\'    
        return(o)
    else:
        o = f'''{alph}'''
        for i in range(14):
            o += '&'
            o += chr(i+65)
        o += "&Ñ"
        for i in range(14,26):
            o += '&'
            o += chr(i+65)
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += 'Frequency'
        for i in range(14):
            o += '&'
            o += str(ct.count(chr(i+65)))
        o += '&'
        o += str(ct.count(chr(209)))     
        for i in range(14,26):
            o += '&'
            o += str(ct.count(chr(i+65)))
        o += '\\\\'
        o += '\n'
        o += '\\hline \n'
        o += 'Replacement'
        for i in range(27):
            o += '&'
        o += '\\\\'    
        return(o)

def xeno_process_word(word, shift):
    seen = set()
    unique_letters = []
    word = word.lower().replace(" ","")
    for char in word:
        if char not in seen:
            unique_letters.append(char)
            seen.add(char)
    
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    
    unused_letters = sorted(alphabet - seen)
    
    # Add 'ñ' in its alphabetical position (after 'n', before 'o') if not in seen
    if 'ñ' not in seen:
        # Find the position where 'o' is (or would be) and insert 'ñ' before it
        if 'o' in unused_letters:
            o_index = unused_letters.index('o')
            unused_letters.insert(o_index, 'ñ')
        else:
            # If 'o' is not in unused_letters, find where it should be inserted
            # 'ñ' should come after 'n', so find the first letter after 'n'
            for i, letter in enumerate(unused_letters):
                if letter > 'n':
                    unused_letters.insert(i, 'ñ')
                    break
            else:
                # If all letters are before 'n', append 'ñ' at the end
                unused_letters.append('ñ')
    
    result = ''.join(unique_letters) + ''.join(unused_letters)
    
    shift = shift % len(result)  
    
    shifted_result = result[-shift:] + result[:-shift]
    return shifted_result

def xeno_creator(s, value, type, hint_type, hint, alph="", keyword="", shift="", extract = False):
    s = remove_accents(s)
    replaced_string = xeno_letter_replacement(s, keyword, shift, alph)
    formatted_string = aristo_format_sentence(replaced_string)
    table = xeno_frequency_table(replaced_string, alph)
    if alph != "":
        alph += " "
    if not extract:
        v = "\\normalsize \\question[" + str(value) + "] Solve this \\textbf{" + alph + "Xenocrypt}"
    else:
        v = "\\normalsize \\question[" + str(value) + "] The following quote was encoded as a \\textbf{Xenocrypt} with a " + alph + " alphabet. "
    if hint_type == "None" or hint_type == None:
        v += ".\n"
    elif hint_type == "Word" or hint_type == "Letters":
        v+= ". You are told that " + hint + ".\n"
    elif hint_type == "Word + Subject" or hint_type == "Letters + Subject":
        hint = hint.split(",")
        v+= " about " + hint[1] + ". You are told that " + hint[0] + ".\n"
    elif hint_type == "Subject":
        v+= f" about {hint}."
    if extract:
        v+=f"The keyword is {len(keyword)} letters long. What is the keyword? "
        v+="$\\boxed{\\text{box}}$ your final answer."
    v += "\n\\Large{\n"
    v += "\\begin{verbatim}\n"
    v += formatted_string + "\n"
    v += "\\end{verbatim}}\n"
    v += "{\\normalsize\n"
    v += "\\begin{center}\n"
    v += "\\begin{tabular}\n"
    v += "{|m{2cm}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|m{9.675pt}|}\n"
    v += "\\hline\n"
    v += table + "\n"
    v += "\\hline\n"
    v += "\\end{tabular}\n"
    v += "\\end{center}}\n"
    v += "\\vfill\n"
    v += "\\uplevel{\\hrulefill}\n"
    return v

# affine (at the end because i forgot oops)
def affine_encoder(s, a, b, bs):
    if a == 1 or a == 13 or a%2==0:
        raise ValueError(f"a = {a}. a must be coprime with 26 (odd and not 1 or 13)")
    s = s.upper().replace(" ", "").replace("'", "").replace(",", "").replace(".", "")
    d = [ord(i) - 65 for i in s]
    encoded = []
    nospace = ""
    
    for ele in d:
        value = ((ele*a)+b)%26
        encoded.append(chr(value + 65))
    
    nospace = ''.join(encoded)
    spaced = ""
    for i in range(len(nospace)):
        spaced += nospace[i]
        if (i % bs == bs - 1):
            spaced += " "
    return spaced

def affine_format_sentence(s):
    words = s.split()
    formatted_string = ""
    current_line = ""
    total_length = 0
    
    for word in words:
        if total_length + len(word) + 1 > 52:
            formatted_string += current_line.rstrip() + "\n\n\n"
            current_line = word + " "
            total_length = len(word) + 1
        else:
            current_line += word + " "
            total_length += len(word) + 1
    
    formatted_string += current_line.rstrip()
    return formatted_string

def affine_formatter(s, a, b, bs, value, type, hint, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s).upper()
    if type == "CRIB":
        bs = 5
    encoded_text = affine_encoder(s, a,b, bs)
    formatted_string = affine_format_sentence(encoded_text)
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result = []
    if type == "DECODE":
        result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Affine}} cipher with $\\textrm{{a}}={a}$ and $\\textrm{{b}}={b}$.{bonus_text}")
    elif type == "CRIB":
        result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Affine}} cipher. You are told that {hint}.{bonus_text}")
    result.append("\n\\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{formatted_string}\n")
    result.append("\\end{verbatim}}")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")
    return "\n".join(result)


# checkerboard cipher

def checkerboard_alphabet(keyword):
    keyword = keyword.lower().replace('j', 'i')
    seen = set()
    keyword_unique = []
    
    for char in keyword:
        if char not in seen and char.isalpha():
            seen.add(char)
            keyword_unique.append(char)
    
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    for char in alphabet:
        if char not in seen:
            keyword_unique.append(char)
    
    return ''.join(keyword_unique)
    
def checkerboard_encoder(hkey,vkey,alph,s,bs):
    hkey = hkey.upper()
    vkey = vkey.upper()
    alph = alph.upper()
    s = s.replace(" ", "").replace("'", "").replace(".", "").replace("?","").replace("!","").upper()
    pk_dict = {}
    for i in range(5):
        for j in range(5):
            pk_dict[alph[j+i*5]] = vkey[i] + hkey[j]
    encoded = []
    for let in s:
        encoded.append(pk_dict[let])
        
    y = ""
    z = 0
    for i in range(len(encoded)):
        y += str(encoded[i]) + " "
        if (i % bs == bs - 1):
            if bs == 1:
                z += 1
                if z == 16:
                    y += "\n\n\n"
                    z = 0
            elif bs < 7:
                y += "   "
                z += 1
                if z == 3:
                    y += "\n\n\n"
                    z = 0
            else:
                y += "   "
                z += 1
                if z == 2:
                    y += "\n\n\n"
                    z = 0
    
    return y

def checkerboarddecode(s, hkey, vkey, pk, bs, value, bonus):
    s = s.upper().replace("J","I")
    s = re.sub(r'[^a-zA-Z]', '', s).upper()
    pkf = pk.upper().replace("J","I")
    alph = checkerboard_alphabet(pk)
    v = checkerboard_encoder(hkey,vkey,alph,s,bs)
    bonus_text=""
    if bonus:
        bonus_text=" \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result = []
    result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Checkerboard}} cipher with a polybius keyword of \\textbf{{{pk}}}.{bonus_text}")
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{v}\n")
    result.append("\\end{verbatim}}\n")
    result.append("{\\renewcommand{\\arraystretch}{1.2}")
    result.append("\\begin{tabular}{m{18pt}|m{18pt}|m{18pt}|m{18pt}|m{18pt}|m{18pt}|}")
    result.append("\\cline{2-6}")
    result.append("& \\multicolumn{1}{r|}{} &  &  &  &  \\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} & \\multicolumn{1}{r|}{} &  &  &  &  \\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\end{tabular}}")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")

    return "\n".join(result)

def checkerboardcrib(s, hkey, vkey, pk, crib, type, mid, value, bonus):
    s = re.sub(r'[^a-zA-Z]', '', s).upper().replace("J","I")
    pkf = pk.upper().replace("J","I")
    alph = checkerboard_alphabet(pk)
    v = checkerboard_encoder(hkey, vkey, alph, s, 1)

    crib_clean = re.sub(r'[^A-IK-Z]', '', crib.upper().replace('J', 'I'))

    c = f"the plaintext begins with \\textbf{{{crib_clean}}}"

    try:
        type = detect_hint_type(s, crib_clean)
    except ValueError as e:
        print(f"[checkerboardcrib detect WARNING] {e}")

    if type == "Start Crib":
        c = f"the plaintext begins with \\textbf{{{crib_clean}}}"
    elif type == "End Crib":
        c = f"the plaintext ends with \\textbf{{{crib_clean}}}"
    elif type == "Middle Crib":
        try:
            c = checkerboard_auto_hint(s, crib, hkey, vkey, pk)
        except ValueError as e:
            print(f"[checkerboard_auto_hint WARNING] {e}\n  Falling back to manual hint.")
            c = mid

    result = []
    bonus_text = ""
    if bonus:
        bonus_text = " \\emph{$\\bigstar$\\textbf{This question is a special bonus question.}}"
    result.append(f"\\normalsize \\question[{value}] Decode this phrase that was encoded using the \\textbf{{Checkerboard}} cipher. You are told that {c}.{bonus_text}")
    result.append("\n \\Large{")
    result.append("\\begin{verbatim}")
    result.append(f"{v}\n")
    result.append("\\end{verbatim}}\n")
    result.append("{\\renewcommand{\\arraystretch}{1.2}")
    result.append("\\begin{tabular}{m{18pt}|m{18pt}|m{18pt}|m{18pt}|m{18pt}|m{18pt}|}")
    result.append("\\cline{2-6}")
    result.append("& \\multicolumn{1}{r|}{} &  &  &  &  \\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} & \\multicolumn{1}{r|}{} &  &  &  &  \\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\multicolumn{1}{|l|}{} &&&&&\\\\ \\hline")
    result.append("\\end{tabular}}")
    result.append("\\vfill \n")
    result.append("\\uplevel{\\hrulefill}")

    return "\n".join(result)


# sheet reading/writing part

def write_file(result, output_file):
    with open(output_file, 'a', encoding='utf-8') as f:  # Specify UTF-8 encoding
        if isinstance(result, str):
            f.write(result + '\n')  # If it's a string, write it directly
        elif isinstance(result, list):
            for item in result:  # If it's a list, write each item on a new line
                f.write(item + '\n')

def main():
    # Create tests directory if it doesn't exist
    tests_dir = "tests"
    os.makedirs(tests_dir, exist_ok=True)
    
    output_file = input("Enter the output file name (without extension, it will be .txt): ")
    key_file = input("Enter the name of the file for the key (must be differnet or errors will happen)")
    input_sheet = input("Enter the name of the .xlsx sheet that contains the quotes (include the .xlsx at the end): ")

    if not output_file.endswith('.txt'):
        output_file += '.txt'
    if not key_file.endswith('.txt'):
        key_file += '.txt'
    
    # Prepend tests directory to file paths
    output_file = os.path.join(tests_dir, output_file)
    key_file = os.path.join(tests_dir, key_file)
    
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write("")  # Create an empty file if it doesn't exist
    if not os.path.exists(key_file):
        with open(key_file, 'w') as f:
            f.write("")  # Create an empty file if it doesn't exist

    df = pd.read_excel(input_sheet, sheet_name="Order")
    df = df.replace(np.nan, '', regex=True)
    return df, output_file, key_file

def sheet_writer(df, output_file, key_file):
    row_counter = 0
    bonus_used = 0
    checkerboard_bonus = False
    while row_counter < len(df):
        result = ""
        if row_counter % 2 == 1:
            result += "\\newpage \n"
        print(row_counter)
        print(df.iloc[row_counter])
        if df.loc[row_counter, "Type"] == "EXTRACT":
            extract = True
        else:
            extract = False
       
        if df.loc[row_counter, "Bonus"]:
            if df.loc[row_counter,"Cipher"] in ["ARISTOCRAT", "PATRISTOCRAT", "XENOCRYPT"]:
                raise ValueError("You cannot set a monoalphabetic cipher to bonus")
            if df.loc[row_counter,"Cipher"] == "CHECKERBOARD":
                checkerboard_bonus = True
            bonus = True
            bonus_used+=1
        else:
            bonus = False
        if not checkerboard_bonus and bonus_used == 3:
            raise ValueError("No checkeboard bonus was set.")
        
        if df.loc[row_counter,"Cipher"] == "ARISTOCRAT":
            result += monoalph_creator(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Value"], "Aristocrat", df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], extract)
            row_counter+=1
        elif df.loc[row_counter,"Cipher"] == "PATRISTOCRAT":
            result += monoalph_creator(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Value"], "Patristocrat", df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], extract)
            row_counter += 1
        elif df.loc[row_counter,"Cipher"] == "ATBASH":
            result += atbash_encoder(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Value"])
            row_counter +=1
        elif df.loc[row_counter, "Cipher"] == "BACONIAN":
            if df.loc[row_counter, "Type"] == "WORDS":
                result += baconianWordsFormatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Value"], df.loc[row_counter, "Type of Hint"], bonus)
                row_counter += 1
            elif df.loc[row_counter, "Type"] in ("LETTERS", "RANDOM LETTERS", "SEQUENCE", "DECODE"):
                # DECODE in the sheet means letter-based Baconian (keys for A/B); use LETTERS encoding
                bacon_type = df.loc[row_counter, "Type"] if df.loc[row_counter, "Type"] != "DECODE" else "LETTERS"
                result += baconianLetters(df.loc[row_counter,"Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], 55, df.loc[row_counter, "Value"], bacon_type, df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], bonus)
                row_counter += 1
            else:
                raise ValueError(f"BACONIAN row {row_counter}: unknown Type {repr(df.loc[row_counter, 'Type'])}. Use WORDS, LETTERS, RANDOM LETTERS, SEQUENCE, or DECODE.")
        elif df.loc[row_counter, "Cipher"] == "CAESAR":
            result += caesar_formatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Value"], bonus)
            row_counter +=1
        elif df.loc[row_counter, "Cipher"] == "COLUMNAR":
            result += columnarFormatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Value"], bonus)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "CRYPTARITHM":
            result += cryptarithm_formatter(df.loc[row_counter, "Value"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Key3"], bonus)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "FRACMORSE":
            result += fractionatedFormatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Value"], df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], bonus)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "HILL":
            result += hillCreater(df.loc[row_counter,"Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter,"Value"], bonus)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "NIHILIST":
            result += nihilistFormatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Value"], df.loc[row_counter, "Type"], df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], bonus)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "PORTA":
            result += porta_formatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Value"], df.loc[row_counter, "Type"], df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], bonus)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "XENOCRYPT":
            result += xeno_creator(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Value"], "Aristocrat", df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], extract)
            row_counter+=1
        elif df.loc[row_counter, "Cipher"] == "AFFINE":
            result += affine_formatter(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Value"], df.loc[row_counter, "Type"], df.loc[row_counter, "Hint"], bonus)
            row_counter +=1
        elif df.loc[row_counter, "Cipher"] == "CHECKERBOARD":
            if df.loc[row_counter, "Type"] == "DECODE":
                result = checkerboarddecode(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Key3"], 5, df.loc[row_counter, "Value"], bonus)
                row_counter +=1
            elif df.loc[row_counter, "Type"] == "CRIB":
                result = checkerboardcrib(df.loc[row_counter, "Plaintext"], df.loc[row_counter, "Key1"], df.loc[row_counter, "Key2"], df.loc[row_counter, "Key3"], df.loc[row_counter, "Hint"], df.loc[row_counter, "Type of Hint"], df.loc[row_counter, "Hint"], df.loc[row_counter, "Value"], bonus)
                row_counter +=1
        # sheet writer
        write_file(result, output_file)
        if df.loc[row_counter-1,"Cipher"] == "ARISTOCRAT" and extract:
            write_string = f"\\question \\textbf{{{df.loc[row_counter-1, "Key1"]}}}: {df.loc[row_counter-1, "Plaintext"]}"
        elif df.loc[row_counter-1,"Cipher"] == "CRYPTARITHM":
            write_string = f"\\question \\textbf{{{df.loc[row_counter-1, "Key1"]}}}: {df.loc[row_counter-1, "Plaintext"]}"
        else:
            write_string = f"\\question {df.loc[row_counter-1, "Plaintext"]}"
        write_file(write_string, key_file)

if __name__ == "__main__":
    df, output_file, key_file = main()
    sheet_writer(df, output_file, key_file)
