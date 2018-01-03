#!/bin/usr/python3

import numpy as np
import sys
from stemming.porter2 import stem
import os


def parse_args():
    if len(sys.argv) == 4 and sys.argv[3] == "--use-noise-reduction-indices":
        return sys.argv[1], int(sys.argv[2]), True
    elif len(sys.argv) == 3:
        return sys.argv[1], int(sys.argv[2]), False
    print('python3 search.py phrase amount_of_results [--use-noise-reduction-indices]')
    exit(1)



def create_bagv_for_phrase(bag_v, phrase):
    p_words = [stem(w.lower()) for w in phrase.split()]
    res = np.zeros(bag_v.shape[0])
    for i in range(bag_v.shape[0]):
        if bag_v[i] in p_words:
            res[i] += 1
    return res

def check_indices(use_reduction):
    if use_reduction:
        if os.path.isfile("./priv/engine/indices/term_by_document_noise_reduction.npy") and os.path.isfile("./priv/engine/indices/bag_of_words_noise_reduction.npy") and os.path.isfile("./priv/engine/indices/files_order_noise_reduction.npy"):
                return True
        else:
            exit(24)
    else:
        if os.path.isfile("./priv/engine/indices/term_by_document.npy") and os.path.isfile("./priv/engine/indices/bag_of_words.npy") and os.path.isfile("./priv/engine/indices/files_order.npy"):
                return True
        else:
            exit(24)


## main

phrase, k, use_noise_reduction = parse_args()

term_by_doc  = ""
bag_v = ""
docs = ""

check_indices(use_noise_reduction)

if use_noise_reduction:
    term_by_doc = np.load('./priv/engine/indices/term_by_document_noise_reduction.npy')
    bag_v = np.load('./priv/engine/indices/bag_of_words_noise_reduction.npy')
    docs = np.load('./priv/engine/indices/files_order_noise_reduction.npy')
else:
    term_by_doc = np.load('./priv/engine/indices/term_by_document.npy')
    bag_v = np.load('./priv/engine/indices/bag_of_words.npy')
    docs = np.load('./priv/engine/indices/files_order.npy')

bagv_p = np.transpose(create_bagv_for_phrase(bag_v, phrase))
res = np.dot(bagv_p, term_by_doc)

res = sorted(zip(res, docs), key=lambda s: s[0], reverse=True)[:k]

string_res = ""
for correctness, file_p in res:
    string_res += str(file_p) + "$" + str(correctness) + "#"
print(string_res)
