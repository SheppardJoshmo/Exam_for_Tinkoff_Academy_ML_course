import ast
import argparse


def levenshtein_distance(a: str, b: str):
    "Calculates the Levenshtein distance between a and b"
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def preprocessing(a: list):
    "Translates the program text into a syntax tree"
    a = "".join(a)
    a = ast.parse(a)
    a = ast.dump(a)
    return a


def console_interface():
    "Takes the names of input and output files from the command line"
    parser = argparse.ArgumentParser(description='Name of files for input and output')
    parser.add_argument('input_file', type=str, help='Name of the input file')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    return args.input_file, args.output_file


name_file_in, name_file_out = console_interface()
pairs_to_compare = []
with open(name_file_in) as file_in:
    for line in file_in:
        line = line.split()
        pairs_to_compare.append(line)

scores = []
for pair in pairs_to_compare:
    with open(pair[0]) as file_in:
        code_1 = file_in.readlines()
    with open(pair[1]) as file_in:
        code_2 = file_in.readlines()
    code_1 = preprocessing(code_1)
    code_2 = preprocessing(code_2)
    # according to this formula 0 <= score <= 1
    # if score = 1 -> code is the same, if score = 0 -> code is absolutely different
    score = (len(code_1) - levenshtein_distance(code_1, code_2)) / len(code_1)
    scores.append(str(score))

with open(name_file_out, "w") as file_out:
    for i in scores:
        file_out.write(i + "\n")
