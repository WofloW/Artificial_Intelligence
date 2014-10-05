import argparse,string,sys,os,math,heapq
import cPickle as pickle
from os.path import join
from weifang_5 import *
import random

directory = "D:/usf/20_newsgroups"

files={}


random.seed()
n= int(sys.argv[-1])

num=0
correct_num=0


category20 = pickle.load(open('20category','rb'))
DFandD = pickle.load(open('DFandD','rb'))
DF = DFandD[0]
D = DFandD[1]


for (dirpath, dirnames, filenames) in os.walk(directory):
	L1 = dirnames
	break

while num<n:
	category = random.choice(L1)

	L2=[]
	for (dirpath, dirnames, filenames) in os.walk(join(directory,category)):
		for j in filenames:
			if '_' not in j:
				L2.append(j)
		break

	filename = random.choice(L2)
	demo=article(None,None,None,{})
	demo.load_and_TF(join(directory,category,filename))
	demo.computeTFIDF(DF,D)
	similar_category = classify(demo, category20)
	if similar_category == category:
		correctness = 'correct'
	else:
		correctness = 'wrong'
	print correctness.center(10),(category+'/'+filename).ljust(34),'is in',similar_category
	if category == similar_category:
		correct_num += 1
	num+=1
print "correct/total: %d / %d = %f %% " %(correct_num,num, float(correct_num)/num*100)


