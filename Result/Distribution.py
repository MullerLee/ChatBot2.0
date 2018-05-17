#-*- coding:utf-8 -*-
"""

@author: M.Lee
@file: Distribution.py
@time: 2018/5/17
"""

import nltk
from nltk.corpus import webtext as web
from nltk import *
from nltk.tokenize import RegexpTokenizer 
from nltk.corpus import stopwords
from nltk.tag import UnigramTagger
from nltk.metrics import *
import string
'''import replacer
from replacer import RegexpReplacer
from replacer import RepeatReplacer'''
import linecache
import matplotlib.pyplot as plt


'''
Train Tagger
'''
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger
from nltk.tag import BigramTagger
from nltk.corpus import treebank
train=treebank.tagged_sents()[:10000]
t0=DefaultTagger('NN')
t1=UnigramTagger(train,backoff=t0)
t2=BigramTagger(train,backoff=t1)


'''
Initialize
'''
my_corp=web.sents(fileids='overheard.txt')
sent_count=0
ques_count=0
All_count=1
NN_count=0
NNS_count=0
NNP_count=0
VB_count=0
VBN_count=0
VBG_count=0
VBD_count=0
VBZ_count=0
JJ_count=0
WP_count=0
NN_Num=0
NNS_Num=0
NNP_Num=0
VB_Num=0
VBN_Num=0
VBG_Num=0
VBD_Num=0
VBZ_Num=0
JJ_Num=0
WP_Num=0

Possibility=[0]

#rep=RegexpReplacer()
i=1
plt.axis([0, 1, 0, 0.15])
plt.xlabel("Possible")
plt.ylabel("Rate")
'''
Main
'''
for eve_sent in my_corp:
	ques_count=ques_count+1
	#print(my_corp[sent_count])
	#init in cur
	All_count=1
	NN_count=0
	NNP_count=0
	JJ_count=0
	WP_count=0
	VBD_count=0
	VBZ_count=0
	wordcount=0
	flag1=0
	#end init
	#pre Operate
	for word in my_corp[sent_count]:
		if my_corp[sent_count][wordcount]==':':
			flag1=1
			break
		wordcount=wordcount+1
	if flag1==1:
		#print(my_corp[sent_count][wordcount+1:-1])
		curr_sent=my_corp[sent_count][wordcount+1:-1]
	else:
		#print(my_corp[sent_count])
		curr_sent=my_corp[sent_count]
	#curr_sent=rep.replace(curr_sent)
	#end pre Operate
	tag_curr_sent=t2.tag(curr_sent)
	#print(tag_curr_sent)
	for words_tup in tag_curr_sent:
		if words_tup[1]!=(',' or '?' or '!' or '.'):
			All_count=All_count+1
		if words_tup[1]=='NN':
			NN_count=NN_count+1
			#NN_Num=NN_Num+1
		if words_tup[1]=='NNP':
			NNP_count=NNP_count+1
			NNP_Num=NNP_Num+1
		if words_tup[1]=='JJ':
			JJ_count=JJ_count+1
			JJ_Num=JJ_Num+1
		#if words_tup[1]=='VB':
		#	VB_count=VB_count+1
		if words_tup[1]=='WP':
			WP_count=WP_count+1
			WP_Num=WP_Num+1
		if words_tup[1]=='VBD':
			VBD_count=VBD_count+1
			VBD_Num=VBD_Num+1
		if words_tup[1]=='VBZ':
			VBZ_count=VBZ_count+1
			VBZ_Num=VBZ_Num+1

	#print("--------------------------------\nIt is the ",sent_count," 's line\n-----------------------------")
	#print("NN:",NN_count/All_count)
	#print("NNP:",NNP_count/All_count)
	#print("JJ:",JJ_count/All_count)
	#print("VB:",VB_count/All_count)
	#print("WP:",WP_count/All_count)
	#print("VBD:",VBD_count/All_count)
	#print("VBZ:",VBZ_count/All_count)

	NNPList=[float(VBZ_count/All_count)]

	Possibility.extend(NNPList)

	#type1=plt.scatter(NN_count/All_count,NN_Num,s=1,edgecolors='none',c='red')
	#plt.pause(0.001)
	#plt.legend((type1),(u'NN'),loc='upper right')
	sent_count=sent_count+1
	if sent_count>15000:
		break
print("Done first")
print(type(Possibility[5]))
"""
The Operation of List Possibility
"""
elemList=[[0,0]]
for elements in Possibility:
		if [elements,0] not in elemList:
			elemList.extend([[elements,0]])

print("Done Second")

#elemList[1][0]=int(elemList[1][0])
#print(elemList[:30])
#print(type(elemList[10][0]))

for elements_2 in Possibility:
		for contag in range(0,len(elemList)-1) :
			if elements_2==elemList[contag][0]:
				elemList[contag][1]=elemList[contag][1]+1
#print(elemList)
print("Done Third")

Expect=0 # Expect=SUM(XxP(X))
Expect_squ=0 # Expect_squ=SUM(X^2xP(X))
Variance=0 # Variance = E(X^2)-E(X)^2
for virab in elemList:
        Expect=Expect+virab[0]*virab[1]/15000
        Expect_squ=Expect_squ+virab[0]*virab[0]*virab[1]/15000
Variance=Expect_squ-Expect*Expect
print("Done Fifth")
print("This is Type VBZ","\nExpect=",Expect,"\nVar=",Variance)

'''
xbr=[0]
ybr=[0]

for reload in elemList:
		xbr.extend([reload[0]])
		ybr.extend([reload[1]/15000])
print("Done Fourth")

plt.scatter(xbr,ybr,s=10,edgecolors='none',c='purple')
plt.show()

	type2=plt.scatter(NNP_count/All_count,NNP_Num,s=1,edgecolors='none',c='blue')
	type3=plt.scatter(JJ_count/All_count,JJ_Num,s=1,edgecolors='none',c='yellow')
	#type4=plt.scatter(VB_count/All_count,s=1,edgecolors='none',c='black')
	#type6=plt.scatter(VBN_count/All_count,s=1,edgecolors='none',c='purple')
	type7=plt.scatter(WP_count/All_count,WP_Num,s=1,edgecolors='none',c='green')
	type8=plt.scatter(VBD_count/All_count,VBD_Num,s=1,edgecolors='none',c='red')
	type9=plt.scatter(VBZ_count/All_count,VBZ_Num,s=1,edgecolors='none',c='#00008B')
	plt.pause(0.001)
	plt.legend((type1,type2, type3,type7,type8,type9), ( u'NN', u'NNP',u'JJ',u'WP',u'VBD',u'VBZ'),loc='upper right')
'''



