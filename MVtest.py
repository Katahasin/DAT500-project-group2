#!/usr/bin/env python3

import sys
import pickle
import json


superArray = []


for line in sys.stdin: # read input from STDIN
  line = line.strip() # remove leading and trailing whitespace
  converted_object = json.loads(line)

  superArray.append(converted_object)
  #print(converted_object)

data = json.dumps(superArray)















import pandas as pd
import numpy as np
import nltk
from collections import Counter
from scipy.sparse import csr_matrix
import random
import matplotlib.pyplot as plt


from nltk import ngrams
from nltk.tokenize import word_tokenize
nltk.download('punkt')


import copy

# Import articles

df = pd.read_json(data)


def createNgrams(articles):

    id = 0
    ngramm_array = []

    for x in articles["content-oneline"]:

        tokens = word_tokenize(x)
        filtered_data = ' '.join([y for y in tokens]) #cachedStopWords change?
        grams = ngrams(filtered_data.split(), 3)
        processed_ngrams = []

        for n in grams:
            token = n[0] + " " + n[1] + " " + n[2]
            processed_ngrams.append(token)
        id += 1
        ngramm_array.append(processed_ngrams)
    
    articles['Trigrams'] = ngramm_array
    
    return articles

df_ngram = createNgrams(df)

def getFrequentNgrams(articles):
    data = (" ").join(articles["content-oneline"])
    data_tokens = word_tokenize(data)
    filtered_data = ' '.join([y for y in data_tokens]) #cachedStopWords change?
    
    n = 3
    created_grams = ngrams(filtered_data.split(), n)
    created_grams_count = Counter(created_grams)
    created_grams_count = created_grams_count.most_common(10000)
    
    created_ngrams = []
    for n, m in created_grams_count:
        token = n[0] + " " + n[1] + " " + n[2]
        created_ngrams.append(token)
    return created_ngrams

freq_gram = getFrequentNgrams(df)
#print (np.shape(freq_gram))
freq_gram


#Preparing the input files
docs = df_ngram["Trigrams"]
docs = docs.apply(lambda row: np.intersect1d(row, freq_gram))

def getBinaryMatrix(docs):
    
    indentpoint = [0]
    indexes = []
    data_array = []
    vocabulary_dict = {}

    for line in docs:

        for x in line:

            index = vocabulary_dict.setdefault(x, len(vocabulary_dict))
            indexes.append(index)
            data_array.append(1)

        indentpoint.append(len(indexes))
        
    binary_matrix = np.transpose(csr_matrix((data_array, indexes, indentpoint), dtype=int).toarray())
    
    return binary_matrix

binary_matrix = getBinaryMatrix(docs)
#print(np.shape(binary_matrix))
binary_matrix


def getHashFunctionValues(numrows, numhashfunctions):

    hash_mat = []

    for x in range(numhashfunctions):

        row = []
        randomInt = int(random.getrandbits(32))

        for y in range(numrows):

            row.append((hash(y)^randomInt))

        hash_mat.append(row)
        
    return np.array(hash_mat)

hash_val_matrix = getHashFunctionValues(binary_matrix.shape[0], 200)


def getMinHashSignatureMatrix(binary_matrix, hash_val_matrix):

    sign_matrix = np.full((hash_val_matrix.shape[0], binary_matrix.shape[1]), np.inf)

    for i in range(binary_matrix.shape[0]):

        for j in np.where(binary_matrix[i] == 1)[0]:

            for h in range(hash_val_matrix.shape[0]):

                if sign_matrix[h][j] == np.inf or sign_matrix[h][j] > hash_val_matrix[h][i]:

                    sign_matrix[h][j] = hash_val_matrix[h][i]
                    
    return sign_matrix


signature_matrix = getMinHashSignatureMatrix(binary_matrix, hash_val_matrix)


def getLSH(signature_matrix, num_bands, num_buckets):
    
    local_sHash = {}

    ran = int(signature_matrix.shape[0]/num_bands)

    for x in range(num_bands):

        rInt = int(random.getrandbits(32))

        for y in range(signature_matrix.shape[1]):

            hashValue = hash(tuple(signature_matrix[x*ran:(x+1)*ran,y]))^rInt

            if hashValue not in local_sHash:

                local_sHash[hashValue] = set()
                
            local_sHash[hashValue].add(y)
    
    return local_sHash
    


locality_sensitive_hash = getLSH(signature_matrix, 20, 1e6)



def plotProbability(s, b, r):

    fig = plt.figure()
    ax = plt.axes()
    ax.set_title(f"LIMIT: {np.round(s, 1)}")

    plt.axvline(x=s)

    for i in range(len(b)):
        x = np.sort(np.random.uniform(0,1,1000), axis=0)
        y = 1 - (1-x**r[i])**b[i]
        ax.plot(x,y, label =f"b={b[i]}, r={r[i]}")
        
    ax.legend()
   
def getJaccardSimilarityScore(C1, C2):
    u = np.sum(np.bitwise_or(C1, C2))
    A = np.sum(np.bitwise_and(C1, C2))
    if u == 0: return 0
    else: return A/u

nearest_neighbors = {}

for bucket, article_numbers in locality_sensitive_hash.items():
    
    for article in article_numbers:

        if article not in nearest_neighbors:

            nearest_neighbors[article] = set()

        nearest_neighbors[article].update([i for i in article_numbers if i != article])
        

threshold = 0.7

data = pd.DataFrame()
n_copy = copy.deepcopy(nearest_neighbors)
submission_id = []
submission_nid = []

for articleId, neighborId in n_copy.items():

    for nid in neighborId:

        Jscore = getJaccardSimilarityScore(binary_matrix[:, articleId], binary_matrix[:, nid])

        if Jscore < threshold:
            nearest_neighbors[articleId].remove(nid)
        else:
            submission_id.append(articleId)
            submission_nid.append(nid)


data['site_id'] = submission_id
data['neighbor_id'] = submission_nid
data.sort_values(by=['site_id', 'neighbor_id'], inplace=True)

print(data)

















