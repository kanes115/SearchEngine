#!/usr/bin/python3

## ALWAYS RUN FROM SEARCH_SERVER ROOT FOLDER!!!
## SOME DIRECTORIES ARE HARDCODED
## IT IS BAD DESIGN BUT A FAST ONE
## NOT NECESSARY TO CHANGE IT AS THE TASK
## IS ABOUT SEARCHENGINE ITSELF

from stemming.porter2 import stem
from os import walk
import numpy as np
import math
import sys
import signal
import scipy.sparse as sc
import scipy.sparse.linalg as la

## it gets a word to its basic form
def word_base(x):
    x = x.lower()
    return stem(x)

def parse_args():
    if len(sys.argv) == 2:
        return int(sys.argv[1]), False
    if len(sys.argv) == 3:
        return int(sys.argv[1]), True
    print('python3 indexing.py amount_of_files [--noise-reduction]')
    exit(1)

def get_words_of_file(filepath):
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        return list(map(lambda x: word_base(x), content.split()))



## Create list of directories of documents and
## a dict mapping filename to list of words that are inside it
def get_filepaths(d_dir, amount_files):
    doc_words_dict = dict()
    files = []
    for (dirpath, dirnames, filenames) in walk(d_dir):
        filepaths = list(map(lambda w: dirpath + '/' + w, filenames))
        files.extend(filepaths)
    i = 1
    files = files[:amount_files]# We only run this for this amount of files
    for filepath in files:
        print("Preparing words for file " + filepath + " (" + str(i) + "/" + str(len(files)) + ")")
        i += 1
        doc_words_dict[filepath] = get_words_of_file(filepath)
    return files, doc_words_dict 


## (2) Create bag of words
def create_bag_of_words(files, doc_words_dict):
    bag = set()
    for filepath in files:
        for word in doc_words_dict[filepath]:
            bag.add(word_base(word))
    return np.array(list(bag))

## (3, 4) For each document create a bag-of-words vector
## and then create a term-by-document matrix
def amount_of_word(x, words):
    i = 0
    for word in words: # note, these are already stemmed words!
        if word == x:
            i += 1
    return i

def create_term_by_doc(files, bag_v, doc_words_dict):
    matrix = list()
    i = 1
    for filepath in files:
        if to_stop:
            return np.column_stack(matrix), files[:i]
        print("term by term for " + str(filepath) + " (" + str(i) + "/" + str(len(files)) + ")")
        i += 1
        v = [amount_of_word(x, doc_words_dict[filepath]) for x in bag_v]
        matrix.append(v)
    return np.column_stack(matrix), files

## (5) 
def IDF(term_by_document, i):
    c = 0
    for k in range(term_by_document.shape[1]):
        if term_by_document[i][k] != 0:
            c += 1
    if c == 0:#czy na pewno?
        return 1
    return math.log(term_by_document.shape[0] / c)


def apply_idf(term_by_document):
    for i in range(term_by_document.shape[0]):
        if (i + 1) % 100 == 0:
            print("IDF " + str(i + 1) + "/" + str(term_by_document.shape[0]))
        idf = IDF(term_by_document, i)
        for j in range(term_by_document.shape[1]):
            term_by_document[i][j] *= idf


def stop_and_save(signal, frame):
    global to_stop
    to_stop = True

def reduce_noise(A):
    u, d, v = la.svds(A)
    Ar = sc.csc_matrix(A.shape)
    for i in range(len(d) // 2 ):
        Ar += (d[i] * np.outer(u.T[i], v[i]))
    return Ar

## main
## Documents directory
doc_dir = './priv/static/documents/'
amount_files, do_noise_reduction = parse_args()

files, doc_words_dict = get_filepaths(doc_dir, amount_files)

bag_v = create_bag_of_words(files, doc_words_dict)

to_stop = False
signal.signal(signal.SIGINT, stop_and_save) # next operation is long

term_by_document, files = create_term_by_doc(files, bag_v, doc_words_dict)

term_by_document = term_by_document.astype(float)

apply_idf(term_by_document)

if do_noise_reduction:
    term_by_document = reduce_noise(term_by_document)


if do_noise_reduction:
    np.save('./priv/engine/indices/term_by_document_noise_reduction', term_by_document)
    np.save('./priv/engine/indices/bag_of_words_noise_reduction', bag_v)
    np.save('./priv/engine/indices/files_order_noise_reduction', np.array(files))
else:
    np.save('./priv/engine/indices/term_by_document', term_by_document)
    np.save('./priv/engine/indices/bag_of_words', bag_v)
    np.save('./priv/engine/indices/files_order', np.array(files))
