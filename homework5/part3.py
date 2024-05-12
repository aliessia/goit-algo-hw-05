import os
import timeit
import chardet

def read_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        return raw_data.decode(encoding)

def boyer_moore_search(text, pattern):
    return text.find(pattern)

def kmp_search(text, pattern):
    N, M = len(text), len(pattern)
    lps = [0] * M
    j = 0
    def computeLPSArray():
        length = 0
        i = 1
        while i < M:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length-1]
                else:
                    lps[i] = 0
                    i += 1
    computeLPSArray()
    i = 0
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == M:
            return i - j
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return -1

def rabin_karp_search(text, pattern):
    d = 256
    q = 101
    M = len(pattern)
    N = len(text)
    p = 0
    t = 0
    h = 1
    for i in range(M-1):
        h = (h * d) % q
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(N - M + 1):
        if p == t:
            if text[i:i+M] == pattern:
                return i
        if i < N-M:
            t = (d*(t-ord(text[i])*h) + ord(text[i+M])) % q
            if t < 0:
                t = t + q
    return -1

def measure_time(func, text, pattern):
    setup_code = f"from __main__ import {func.__name__} as tested_func, text"
    stmt = "tested_func(text, pattern)"
    return min(timeit.repeat(setup=setup_code, stmt=stmt, repeat=3, number=100, globals=globals()))


# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the directory containing the text files
data_directory = os.path.join(current_directory, "data")

# Load text files
text1 = read_file(os.path.join(data_directory, "стаття1.txt"))
text2 = read_file(os.path.join(data_directory, "стаття2.txt"))

# Define search patterns
pattern_exist_1 = "алгоритми"
pattern_fiction_1 = "abcdef"
pattern_exist_2 = "рекомендаційні системи"
pattern_fiction_2 = "xyz123"

# Compare algorithms
for text, name in [(text1, "Article 1"), (text2, "Article 2")]:
    print(f"\nResults for {name}:")
    for func in [boyer_moore_search, kmp_search, rabin_karp_search]:
        time_exist = measure_time(func, text, pattern_exist_1 if name == "Article 1" else pattern_exist_2)
        time_fiction = measure_time(func, text, pattern_fiction_1 if name == "Article 1" else pattern_fiction_2)
        print(f"{func.__name__} - Existing: {time_exist:.5f}s, Fictional: {time_fiction:.5f}s")
