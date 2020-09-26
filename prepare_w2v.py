#-*- encoding: utf-8 -*-
# prepration process for word2vec

import os, sys 
import pdb 
import tqdm
import json
import datetime
from util import iterate_data_files

def make_sentence():
  session_sentences = []
  prev_hour_reads = {}

  of1 = open("session_sentences_1h.txt", "w")
  of2 = open("session_sentences_2h.txt", "w")
  print("read reads for the test set")
  num_noread = 0
  files = sorted([path for path, _ in iterate_data_files('2018100100', '2019030100')])
  for path in tqdm.tqdm(files, mininterval=1):
    datehour = path[11:21]
    hour_reads = {}
    for line in open(path):
      tokens = line.strip().split()
      user_id = tokens[0]
      reads = tokens[1:]
      if len(reads) == 0:
          num_noread += 1
          continue
      ureads = [] # remove continuously doubled article
      prev_read = None
      for read in reads:
        if prev_read == None or read != prev_read:
          ureads.append(read)
        prev_read = read
      hour_reads[user_id] = ureads

      if len(ureads) > 1:
        of1.write(" ".join(ureads) + "\n")
    
    curr_hour_reads = hour_reads.copy()

    for user_id in hour_reads:
      if user_id in prev_hour_reads:
        if len(prev_hour_reads[user_id]) + len(hour_reads[user_id]) > 1:
          of2.write(" ".join(prev_hour_reads[user_id]) + " " + " ".join(hour_reads[user_id]) + "\n")
        del prev_hour_reads[user_id]
        del curr_hour_reads[user_id]

    for user_id in prev_hour_reads:
      if len(prev_hour_reads[user_id]) > 1:
        of2.write(" ".join(prev_hour_reads[user_id]) + "\n")

    prev_hour_reads = curr_hour_reads.copy()
    

  of1.close()
  of2.close()
  print("no read:", num_noread)


if __name__ == "__main__":

  make_sentence()
