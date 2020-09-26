#-*- encoding: utf-8 -*-
# recommend by finding similar articles as the read article by w2v of session sentences

import os, sys 
import pdb 
import sqlite3
import tqdm
import json
import datetime
from util import iterate_data_files
from gensim.models import Word2Vec, KeyedVectors

def find_dup_similar(viewer):
  recommends1 = []
  recommends2 = []
  if viewer in t_followings:
    followings = t_followings[viewer]
  else:
    followings = []

  if viewer in t_reads_dup:
    reads = t_reads_dup[viewer]
    num_reads = len(reads)
    for read in reads:
      if read in model.wv:
        seqs = get_similar_article(read, 3)
        for seq in seqs:
          if seq not in t_reads[viewer]:
            if seq not in recommends1 and seq not in recommends2:
              writer = seq.split("_")[0]
              if writer in followings:
                recommends1.append(seq)
              else:
                recommends2.append(seq)
              if num_reads > 30: break
  return recommends1, recommends2

def read_test_user():
  print("read test user set", user_file)
  with open(user_file, "r") as fp:
    for line in fp:
      viewer_id = line.strip()
      t_users[viewer_id] = 1

def read_followings():
  print("read viewer followings for the test set")
  with open("res/users.json", "r") as fp:
    for line in fp:
      viewer = json.loads(line)
      if viewer['id'] in t_users:
        t_followings[viewer['id']] = viewer['following_list']

# may need to write pickle for this
def read_reads():
  print("read reads for the test set")
  files = sorted([path for path, _ in iterate_data_files('2018100100', '2019030100')])
  for path in tqdm.tqdm(files, mininterval=1):
    date = path[11:19]
    for line in open(path):
      tokens = line.strip().split()
      user_id = tokens[0]
      reads = tokens[1:]
      if len(reads) < 1: continue
      if user_id in t_users:
        if user_id in t_reads:
          t_reads[user_id] += reads
        else:
          t_reads[user_id] = reads
        if date >= "20190222":
          if user_id in t_reads_dup:
            t_reads_dup[user_id] += reads
          else:
            t_reads_dup[user_id] = reads

        reads_set = set(reads)
        for read in reads_set:
          writer = read.split("_")[0]
          if user_id not in t_followings or writer not in t_followings[user_id]:
            if user_id in t_non_follows:
              if writer in t_non_follows[user_id]:
                t_non_follows[user_id][writer] += 1
              else:
                t_non_follows[user_id][writer] = 1
            else:
              t_non_follows[user_id] = {}
              t_non_follows[user_id][writer] = 1

  for user in t_reads:
    if user not in t_reads_dup:
      t_reads_dup[user] = t_reads[user][-10:]

def get_similar_article(article, topn):
  similars = []
  tops = model.wv.most_similar(article, topn=topn)
  for item in tops:
    similars.append(item[0])
  return similars

def determine_non_follow():
  print("sort non follow writers")
  for user in t_non_follows:
    writers = t_non_follows[user]
    writers_sorted = sorted(writers.items(), key=lambda x: x[1], reverse=True)
    if len(writers_sorted) < 3: tops = len(writers_sorted)
    else: tops = 3
    if writers_sorted[0][1] < 5: continue
    t_non_follow[user] = []
    for i in range(tops):
      if writers_sorted[i][1] < 5: break
      t_non_follow[user].append(writers_sorted[i][0])

# may need to write pickle for this
def read_article_meta():
  print("build article id and registration time for each writer")
  with open("res/metadata.json", "r") as fp:
    for line in fp:
      article = json.loads(line)
      article_id = article['id']
      writer_id = article['user_id']
      reg_datetime = datetime.datetime.fromtimestamp(article['reg_ts']/1000).strftime("%Y%m%d%H%M%S")
      if writer_id in writer_articles:
        writer_articles[writer_id].append([article_id, reg_datetime])
      else:
        writer_articles[writer_id] = [[article_id, reg_datetime]]

if __name__ == "__main__":
  if sys.argv[1] == "test":
    user_file = "res/predict/test.users"
  elif sys.argv[1] == "dev":
    user_file = "res/predict/dev.users"
  else:
    sys.exit()

  print("load w2v model")
  model = Word2Vec.load("model/views_wv.model")

  t_users = {}   # all test_users
  t_followings = {}   # following writer list for test users
  t_non_follows = {}   # non-follow but many reads writer list for test users
  t_non_follow = {}   # top3 non-follow but many reads writer list for test users
  t_reads = {}        # read articles for test users
  t_reads_dup = {}    # read articles during dup dates for test users (2/22~)
  writer_articles = {}

  read_test_user()

  read_followings()

  read_reads()

  determine_non_follow()

  read_article_meta()

  of1 = open("recommends_wv.txt", "w")
  print("recommend similar articles of the read article")
  num_recommended = 0
  num_recommends1 = 0

  for viewer in t_users:
    recommends11, recommends12 = find_dup_similar(viewer)
    recommends1 = recommends11 + recommends12
    if len(recommends1) > 0:
      of1.write(viewer + " " + " ".join(recommends1[:100]) + "\n")
      num_recommended += 1
    num_recommend1 = len(recommends1[:100])
    num_recommends1 += num_recommend1

  of1.close()

  print(num_recommended)
  print(num_recommends1)
