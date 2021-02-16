# -*- coding: utf-8 -*-
###---------------------------------------------------------------------------------------------------

###                                Simple Dialogue System Based on Context (SDSBC)

###---------------------------------------------------------------------------------------------------
'''
 @ Firstly edit: Manfred Lee ( Xingchen Lee)
 @ File:         main.py
 
 python 3.5.1

 Unreleased Versions:
 Version 0.1.1 ---->  Feb 23rd , 2018 : A brief structure(M.Lee)
 Version 0.1.2 ---->  Feb 24th , 2018 : File search was added(M.Lee)
 Version 0.1.3 ---->  Feb 25th , 2018 : Situation of names was added(M.Lee)
 Version 0.1.4 ---->  Feb 27th , 2018 : Situation of places and time were added
                                        Structure of single-context-situation was built(M.Lee)
 Version 0.1.5 ---->  Feb 28th , 2018 : Judgement of Topic Range ( W*7 + how) (M.Lee)
 Version 0.1.6 ---->  Mar 3rd  , 2018 : Fixed some Bugs (M.Lee)
                                        Database Establisher is Developed (M.Lee)
 Version 0.1.7 ---->  Mar 4th  , 2018 : Function matrix_equation_solver() added ( M.Lee)
                                        --- be used to find the best weights of three training methods
 Version 0.1.8 ---->  Mar 7th  , 2018:  The Structure of Rate_Marker is added,
                                        --- two other methods of marking is still unadded
 Version 0.1.9 ---->  Mar 12th , 2018:  Dataset is created with 352 lines
                                        --- change into 330 lines
               ---->  Mar 13th , 2018:  100 sentences tagged
                                       
 Released Versions:
 No Rights Reserved Currently
'''
###---------------------------------------------------------------------------------------------------


### Libs and Packets
from __future__ import print_function
import nltk
from nltk import *
from nltk.tokenize import RegexpTokenizer 
from nltk.corpus import stopwords
from nltk.tag import UnigramTagger
from nltk.metrics import *
import string
import replacer
from replacer import RegexpReplacer
from replacer import RepeatReplacer
import linecache

###----------------------------------------------------------------------------

### Corpus
from nltk.corpus import brown
from nltk.corpus import webtext
from nltk.corpus import names

###----------------------------------------------------------------------------

### Function Definition
def all_lower(L1):        # To lowercate a List
     return [s.lower() for s in L1]

def matrix_equation_solver( L1R,L1W,L2R,L2W,L3R,L3W ):  # To Find the Best Weight of Three Training Methods, Returns the Weights
    eq_s_A = 0
    eq_s_B = 0
    eq_s_C = 0

    z_Ave_2 = 0
    z_S2_total = 0
    z_S2 = [1000]
    eq_z = [None]*5

    eq_s_X = [0]
    eq_s_Y = [0]
    eq_s_Z = [0]
    Ave=[0]

    list_divi1 = [None]*5
    list_divi2 = [None]*5
    list_divi3 = [None]*5

    eq_s_count=0
    while eq_s_count<5:
        list_divi1[eq_s_count] = L1R[eq_s_count]-L1W[eq_s_count]
        list_divi2[eq_s_count] = L2R[eq_s_count]-L2W[eq_s_count]
        list_divi3[eq_s_count] = L3R[eq_s_count]-L3W[eq_s_count]
        eq_s_count=eq_s_count+1

    j=0
    while j<5:
        eq_s_A = list_divi1[j]+eq_s_A
        eq_s_B = list_divi2[j]+eq_s_B
        eq_s_C = list_divi3[j]+eq_s_C
        j = j+1

    eq_s_x1 = 0
    eq_s_x2 = 0
    eq_s_x3 = 10
    while eq_s_x1<=10:
        while eq_s_x2<=10-eq_s_x1:
            eq_s_x3 = 10-eq_s_x2-eq_s_x1
            i=0
            z_S2_total = 0
            z_Ave_2 = (eq_s_x1*eq_s_A+eq_s_x2*eq_s_B+eq_s_x3*eq_s_C)/5
            while i<5:
                eq_z[i] = eq_s_x1*list_divi1[i]+eq_s_x2*list_divi2[i]+eq_s_x3*list_divi3[i]
                z_S2_total = z_S2_total+(eq_z[i]-z_Ave_2)*(eq_z[i]-z_Ave_2)
                i=i+1
            eq_s_x2 = eq_s_x2+1
            if(z_S2_total/5)<0.8:
                z_S2.append(z_S2_total/5)
                eq_s_X.append(eq_s_x1)
                eq_s_Y.append(eq_s_x2)
                eq_s_Z.append(eq_s_x3)
                Ave.append(z_Ave_2)
        eq_s_x1 = eq_s_x1+1
        eq_s_x2 = 0
        eq_s_x3 = 10-eq_s_x2-eq_s_x1

    eq_s_a = 0
    eq_s_b = 0
    eq_s_c = 0
    
    Ave_cache = 0
    eq_s_count_2 = 0

    while eq_s_count_2<len(z_S2):
        if Ave_cache<Ave[eq_s_count_2]:
            eq_s_a = eq_s_X[eq_s_count_2]
            eq_s_b = eq_s_Y[eq_s_count_2]
            eq_s_c = eq_s_Z[eq_s_count_2]
            Ave_cache = Ave[eq_s_count_2]
        eq_s_count_2 = eq_s_count_2+1

    return([eq_s_a,eq_s_b,eq_s_c])

###----------------------------------------------------------------------------

### Global Variables
male_names = all_lower(names.words('male.txt'))
female_names = all_lower(names.words('female.txt'))
rep_1=RepeatReplacer()    # Object of RepeatReplacer (Main Circuit, PART 1)
rep_2=RegexpReplacer()    # Object of RegexpReplacer (Main Circuit, PART 1)
count=0                   # The Number of Found Result， TEMPORARY
tag=0                     # Flag1: if find aim in database, tag=1
con_count = 0
cit_count = 0
mon_count = 0
sit_count = 0

weigh_method_1=0          # Weigh1: method1
weigh_method_2=0          # Weigh2: method2
weigh_method_3=0          # Weigh3: method3
weigh_list=[None]*3       # List1 : Cache list



editdis=1000              # Param1: the result of edit_distance (Main Circuit, PART 2)
line_num=0                # Param2: line number of the most possible answer (Main Circuit, PART 2)
rate=0                    # Index1: rate=(len(line)-editdis)/len(line) (Main Circuit, PART 2)

lc_male_name=None         # Index2: the latest male name that occured (Main Circuit, PART 3, Filter 1)
lc_female_name=None       # Index3: the latest female name that occured (Main Circuit, PART 3, Filter 1)

lc_country=None           # Index4: the latest country name that occured (Main Circuit, PART 3, Filter 2)
lc_city=None              # Index5: the latest city name that occured (Main Circuit, PART 3, Filter 2)

lc_year=None              # Index6: the latest year that occured (Main Circuit, PART 3, Filter 3)
lc_month=None             # Index7: the latest month name that occured (Main Circuit, PART 3, Filter 3)
lc_date=None              # Index8: the latest date name that occured (Main Circuit, PART 3, Filter 3)

situation=['None','what','when','why','how','which','where','who','whose']
                          # Param3: 6 situations that might occur in a round of dialogue (Main Circuit, PART 3, Filter 4)
cur_situ=0                # Index9: current situation, the count number in the list (Main Circuit, PART 3, Filter 4)


editdis_2=1000            # Param4: the result of edit_distance on searching after filter (Main Circuit, PART 3, Filter 5)
line_num_2=0              # Param5: line number of the most possible answer on searching after filter (Main Circuit, PART 3, Filter 5)
rate_2=0                  # Index10: rate_2=(len(linenn)-editdis)/len(linenn) (Main Circuit, PART 3, Filter 5)

###----------------------------------------------------------------------------

### Train Tagger ( Unitagger )
#Attempt to use the bigram-callout annotation identifier
#If the Bigram callout cannot find the tag, try Unigram the callout
#If the Unigram callout cannot find the tag, use the default callout
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger
from nltk.tag import BigramTagger
from nltk.corpus import treebank
print("Preparing, please wait\nLoading...")
train=treebank.tagged_sents()[:7000]
t0=DefaultTagger('NN')
t1=UnigramTagger(train,backoff=t0)
t2=BigramTagger(train,backoff=t1)

### Train Rate_Marker
'''
Sear_Edit_Dis = [None] * 10

Sear_Means1_Right = [None] * 5
Sear_Means1_Wrong = [None] * 5

Sear_Rou_Count  = 0
Sear_Line_Count = 0
Sear_Total_Line = 0
Sear_Corre_Line = 0

Sear_Ques = [None] * 10
Sear_Answ = [None] * 10
Sear_Accu = [None] * 10

while Sear_Rou_Count <34:
  while Sear_Line_Count < 10:
    Sear_Line_Count=Sear_Line_Count+1
    Sear_Total_Line=Sear_Rou_Count*10+Sear_Line_Count
    Sear_line=linecache.getline('data\\OA_base_recover.txt',Sear_Total_Line)
    Sear_start1=0
    Sear_search1='['
    Sear_search2=']'
    Sear_index1 = Sear_line.find(Sear_search2, Sear_start1)
    Sear_start2 = Sear_index1+1
    Sear_index2 = Sear_line.find(Sear_search2, Sear_start2)

    Sear_Ques[Sear_Line_Count-1] = Sear_line[Sear_start1+1:Sear_index1]
    Sear_Answ[Sear_Line_Count-1] = Sear_line[Sear_start2+1:Sear_index2]
    Sear_Accu[Sear_Line_Count-1] = Sear_line[Sear_index2+2]

    if Sear_Accu[Sear_Line_Count-1]=='1':
        Sear_Corre_Line=Sear_Line_Count-1
    Sear_Edit_Dis[Sear_Line_Count-1]=(len(Sear_line)-(edit_distance(Sear_Ques[Sear_Line_Count-1],Sear_Answ[Sear_Line_Count-1])))/len(Sear_line)
  Sear_i=0
  Sear_Edit_total=0
  while Sear_i<10:
    if Sear_i!=Sear_Corre_Line:
      Sear_Edit_total=Sear_Edit_total+Sear_Edit_Dis[Sear_i]
    Sear_i=Sear_i+1
  Edit_Ave=Sear_Edit_total/9
  
  #print(Edit_Ave)
  #print(Sear_Edit_Dis[Sear_Corre_Line])

  Sear_Means1_Right[Sear_Rou_Count]=Sear_Edit_Dis[Sear_Corre_Line]
  Sear_Means1_Wrong[Sear_Rou_Count]=Edit_Ave
  
  Sear_Rou_Count=Sear_Rou_Count+1
  Sear_Line_Count=0
  Sear_Corre_Line=0

#print(Sear_Means1_Right,Sear_Means1_Wrong)
#Use data from train_base to find a best weigh
'''
print("Successfully loaded, now let's chat")
###----------------------------------------------------------------------------

### Main Circuit
while 1:
## 1.The part of input
 print("----------------------------------------")
 tag=0
 ques=input()  #Enter your question
 ques=ques.lower()
 if ques[-1]=='?' or ques[-1]=='.' or ques[-1]=='!' or ques[-1]==';' or ques[-1]==':':
     ques=ques[:-1]
 rep_22=rep_2.replace(ques)
 #rep_22=rep_22[:-1]
 #rep_11=rep_1.replace(rep_22)

## 2.The part of searching in database
 n=0
 ques_l=rep_22+'\n'
 while n<80:
  n=n+1
  line=linecache.getline('D:\\CollegeActivities\\MainSubjects\\NLP\\ChatSys\\data\\dataset-Q.txt', n)
  if edit_distance(ques_l,line)<editdis:
    editdis=edit_distance(ques_l,line)
    line_num=n
    rate=(len(line)-editdis)/len(line)
 if rate>0.8:# rate larger than 0.8
  reline=linecache.getline('D:\\CollegeActivities\\MainSubjects\\NLP\\ChatSys\\data\\dataset-A.txt', line_num)
  print(reline)
  tag=1
  editdis=1000           
  line_num=0
  rate=0
        
## 3.The part of Standardize and NER
 if tag==0:
  stopwords=nltk.corpus.stopwords.words('english')
  cont=nltk.word_tokenize(rep_22)
  # Name Standardize
  cont=[ lc_male_name if x == 'he' else x for x in cont]
  cont=[ lc_male_name if x == 'his' else x for x in cont]
  cont=[ lc_female_name if x == 'she' else x for x in cont]
  cont=[ lc_female_name if x == 'her' else x for x in cont]
  # Place Standardize
  
  cont_tag=t2.tag(cont)
  cont_unstop=[word for word in cont if word not in stopwords]
  cont_tagged=t2.tag(cont_unstop)# Final result of NER

## 4.Answer Filter
# First Filter: Find names in the input
  for tupl_1 in cont_tag:
      if tupl_1[1]=='NN':
          if tupl_1[0] in male_names:
              lc_male_name = tupl_1[0]
          elif tupl_1[0] in female_names:
              lc_female_name = tupl_1[0]

# Second Filter: Find places in the input
  for tupl_2 in cont_tag:
      if tupl_2[1]=='NN':
          while con_count<80:
              con_cach=linecache.getline('D:\\CollegeActivities\\MainSubjects\\NLP\\ChatSys\\data\\countries.txt',con_count)
              con_cach=con_cach[:-1]
              con_cach_l=con_cach.lower()
              con_count=con_count+1
              if con_cach_l==tupl_2[0]:
                  lc_country=con_cach_l
          while cit_count<80:
              cit_cach=linecache.getline('D:\\CollegeActivities\\MainSubjects\\NLP\\ChatSys\\data\\cities.txt',cit_count)
              cit_cach=cit_cach[:-1]              cit_cach_l=cit_cach.lower()
              cit_count=cit_count+1
              if cit_cach_l==tupl_2[0]:
                  lc_city=cit_cach_l
          con_count=0
          cit_count=0
  
# Third Filter: Find date in the input
  for tupl_3 in cont_tag:
      if tupl_3[1]=='CD' or tupl_3[1]=='NN':
          if tupl_3[0]>'1000' and tupl_3[0]<'2100':
              lc_year=tupl_3[0]
      if tupl_3[1]=='NN':
          tail_date=(tupl_3[0])[-2:]
          print(tail_date)
          if tail_date=='st' or tail_date=='nd' or tail_date=='rd' or tail_date=='th':
              lc_date=tupl_3[0]
          while mon_count<25:
              mon_cach=linecache.getline('D:\\CollegeActivities\\MainSubjects\\NLP\\ChatSys\\data\\month.txt',mon_count)
              mon_cach=mon_cach[:-1]
              mon_cach_l=mon_cach.lower()
              mon_count=mon_count+1
              if mon_cach_l==tupl_3[0]:
                  lc_month=mon_cach
          mon_count=0

# Forth Filter: Estabilish the Situation
  cur_situ=0
  for tupl_4 in cont_tag:
      if tupl_4[1][0]=='W':
          while sit_count<8:
           sit_count=sit_count+1
           if situation[sit_count]==tupl_4[0]:
               cur_situ=sit_count
      sit_count=0

  print('current situation:',situation[cur_situ],lc_female_name,lc_male_name,lc_city,lc_country,lc_month,lc_date,lc_year)
