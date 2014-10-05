import argparse,string,sys,os,math,heapq
import cPickle as pickle
from os.path import join
from weifang_5 import *
import random

def combine(dict1, dict2):
	for word in dict2:
		if word not in dict1:
			dict1[word] = dict2[word]
		else:
			dict1[word] = dict1[word] + dict2[word]
	return dict1


category20 = pickle.load(open('20category','rb'))
DFandD = pickle.load(open('DFandD','rb'))
dict_20_TFIDF=[]
category_record=[]



for category in category20:
	dict_20_TFIDF.append(category20[category])
	category_record.append(category)





while len(dict_20_TFIDF)>1:
	max_value = 0
	for i in range(len(dict_20_TFIDF)):
		for j in range(i+1,len(dict_20_TFIDF)):
			temp = cosineSimilarity(dict_20_TFIDF[i],dict_20_TFIDF[j])
			if temp > max_value:
				max_value = temp
				pair = [i,j]
	i = pair[0]
	j = pair[1]
	dict_20_TFIDF[i] = combine(dict_20_TFIDF[i],dict_20_TFIDF[j])
	dict_20_TFIDF.remove(dict_20_TFIDF[j])


	category_record[i] = '{'+category_record[i] + ' U ' + category_record[j] + '}'
	category_record.remove(category_record[j])

	
print category_record[0]



