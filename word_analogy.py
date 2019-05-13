#!/usr/bin/env python3

import sys
import os
import numpy

vector_file = sys.argv[1]
input_dir = sys.argv[2]
output_dir = sys.argv[3]
eval_file = sys.argv[4]

word_vectors = {}
with open(vector_file, 'r') as open_file:
    for line in open_file.readlines():
        word = line.split()[0]
        vector = line.split()[1:]
        word_vectors[word] = numpy.array(vector, dtype=float)


def word_checker(word):
    if word in word_vectors:
        return word_vectors[word]
    else:
        return [0] * 300


def find_e_dist(v1, v2):
    squared_sum = numpy.square(v1 - v2)
    total = numpy.sum(squared_sum)
    return total


for filename in os.listdir(input_dir):
    if filename.startswith('.'):
        continue
    if not filename.endswith('.txt'):
        continue
    file_path = os.path.join(input_dir, filename)
    file_path_out = os.path.join(output_dir, filename)
    count = 0
    lines = 0
    with open(file_path, 'r') as open_file:
        with open(file_path_out, 'w') as output_file:
            for line in open_file.readlines():
                lines += 1
                A_word = line.split()[0]
                A_vec = numpy.array(word_checker(A_word), dtype=float)
                B_word = line.split()[1]
                B_vec = numpy.array(word_checker(B_word), dtype=float)
                C_word = line.split()[2]
                C_vec = numpy.array(word_checker(C_word), dtype=float)
                D_word = line.split()[3]
                D_vec = C_vec + B_vec - A_vec
                smallest = 100
                smallest_word = None
                for word in word_vectors:
                    distance = find_e_dist(D_vec, word_vectors[word])
                    if distance < smallest:
                        smallest = distance
                        smallest_word = word
                if smallest_word == D_word:
                    count += 1
                output_file.write(A_word + " " + B_word + " " + C_word + " " + str(smallest_word) + "\n")

    with open(eval_file, 'a') as eval:
        percent = count/lines
        eval.write(filename + "\n" + "ACCURACY: " + str(percent) + " " + str(count) + "/" + str(lines) + "\n")


#   References
#   Thank you to Justin & Sophia! Also worked with Kelsey!
#   https://www.guru99.com/reading-and-writing-files-in-python.html - how to add to a file instead of rewrite it
