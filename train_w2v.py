#-*- encoding: utf-8 -*-
# read and augment sentences then create word2vec model
# test items are for checking how well the model is

import pdb, sys, os
import random
import pickle
from gensim.models import Word2Vec, KeyedVectors

test_items = [
    '@brunch_141',
    '@tenbody_1305',
    '@jooyoon_51',
    '@speralist_228',
    '@lesreports_26',
    '@longthumb_36',
    ]

def read_basic_sentences():
  print("reading sentences")
  fpath = "session_sentences_2h.txt"
  fpath = "session_sentences_1h.txt"
  fp = open(fpath, 'r')
  cnt = 0
  while True:
    cnt += 1
    if cnt % 100000 == 0: print(cnt)

    line = fp.readline().strip()
    if not line: break
    words = line.split(' ')
    if len(words) < 1: pdb.set_trace()
    elif len(words) < 2: continue
    sentences.append(words)

    '''
    if len(words) > 9:  # augment
      i = 4
      while i < len(words):
        aug_sent = []
        for i in range(i, min(i+9, len(words))):
          aug_sent.append(words[i])
        sentences.append(aug_sent)
        i += 5
    '''

  fp.close()

def train_w2v():
  print("train w2v model and save vectors with", len(sentences), "sentences")
  #model = Word2Vec(sentences, size=100, min_count=1, window=5, iter=20, sample=1e-5, sg=1, workers=4)
  model = Word2Vec(sentences, size=150, min_count=1, window=1, iter=20, sample=1e-5, sg=1, workers=4)
  model.save("model/views_wv.model")
  model.wv.save("model/views_wv.kv")

  print("check similarity")
  for test_item in test_items:
    try:
      top9 = model.wv.most_similar(test_item, topn=9)
    except:
      continue
    print(test_item)
    
    for item in top9:
      print("    ", item[0], item[1])

def check_w2v():
  print("load w2v model")
  model = Word2Vec.load("model/views_wv.model")

  print("check similarity")
  for test_item in test_items:
    try:
      top9 = model.wv.most_similar(test_item, topn=9)
    except:
      continue
    print(test_item)
    
    for item in top9:
      print("    ", item[0], item[1])

  pdb.set_trace()

if __name__ == "__main__":

  sentences = []
  if len(sys.argv) > 1 and sys.argv[1] == "train":
    read_basic_sentences()
    train_w2v()
  else:
    check_w2v()
