#-*- coding:utf-8 -*-
###---------------------------------------------------------------------------------------------------

###                 Simple Dialogue System Based on Context -- Database Establisher (SDSBC-DE)

###---------------------------------------------------------------------------------------------------
### Firstly edit by Manfred Lee ( Xingchen Lee)
### python 3.5
###
### Unreleased Versions:
### Version 0.1.1 ---->  Feb 23rd , 2018 : A brief structure(M.Lee)
### Version 0.1.2 ---->  Feb 24th , 2018 : File search was added(M.Lee)
### Version 0.1.3 ---->  Feb 25th , 2018 : Situation of names was added(M.Lee)
### Version 0.1.4 ---->  Feb 27th , 2018 : Situation of places and time were added
###                                        Structure of single-context-situation was built(M.Lee)
### Version 0.1.5 ---->  Feb 28th , 2018 : Judgement of Topic Range ( W*7 + how) (M.Lee)
### Version 0.1.5.brabch  Database Establisher (M.Lee)
### Released Versions:
### No Rights Reserved Currently
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

###----------------------------------------------------------------------------

### Global Variables
male_names = all_lower(names.words('male.txt'))
female_names = all_lower(names.words('female.txt'))
rep_1=RepeatReplacer()    # Object of RepeatReplacer (Main Circuit, PART 1)
rep_2=RegexpReplacer()    # Object of RegexpReplacer (Main Circuit, PART 1)
count=0                   # The Number of Found Result， TEMPORARY
tag=0                     # Flag1: if find aim in database, tag=1
con_count=0
cit_count=0
stu_count=0
mon_count=0
sit_count=0

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

situation=[None,'what','when','why','how','which','where','who','whose']
                          # Param3: 6 situations that might occur in a round of dialogue (Main Circuit, PART 3, Filter 4)
cur_situ=0                # Index9: current situation, the count number in the list (Main Circuit, PART 3, Filter 4)
situ_list = [None]*7
check_list = [None]


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
print("Successfully loaded, now let's chat")

###----------------------------------------------------------------------------

Ques_Count=0

### Main Circuit
while 1:
## 1.The part of input
 situ_list = [None]*7
 lc_male_name=None         
 lc_female_name=None     

 lc_country=None         
 lc_city=None            

 lc_year=None              
 lc_month=None           
 lc_date=None             
 print("----------------------------------------")
 tag=0
 Ques_Count=Ques_Count+1
 ques=linecache.getline('data\\Questions_will_be_asked.txt', Ques_Count) #Enter your question
 if(Ques_Count>52):
     break
 ques=ques.lower()
 ques=ques[:-1]
 #if ques[-1]=='?' or ques[-1]=='.' or ques[-1]=='!' or ques[-1]==';':
 #    ques=ques[:-1]
 rep_22=rep_2.replace(ques)
 #rep_22=rep_22[:-1]
 #rep_11=rep_1.replace(rep_22)

## 2.The part of searching in database
 n=0
 ques_l=rep_22+'\n'
 while n<80:
  n=n+1
  line=linecache.getline('data\\dataset-Q.txt', n)
  if edit_distance(ques_l,line)<editdis:
    editdis=edit_distance(ques_l,line)
    line_num=n
    linelen=len(line)
    if len(line)==0:
        linelen=10000
    rate=(len(line)-editdis)/linelen
 if rate>0.8:# rate larger than 0.8
  reline=linecache.getline('data\\dataset-A.txt', line_num)
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
  print(cont_tagged)

## 4.Answer Filter
# First Filter: Find names in the input
  for tupl_1 in cont_tag:
      if tupl_1[1]=='NN' or tupl_1[1]=='NNP':
          if tupl_1[0] in male_names:
              lc_male_name = tupl_1[0]
          elif tupl_1[0] in female_names:
              lc_female_name = tupl_1[0]

# Second Filter: Find places in the input
  for tupl_2 in cont_tag:
      if tupl_2[1]=='NN' or tupl_2[1]=='NNP':
          while con_count<80:
              con_cach=linecache.getline('data\\countries.txt',con_count)
              con_cach=con_cach[:-1]
              con_cach_l=con_cach.lower()
              con_count=con_count+1
              if con_cach_l==tupl_2[0]:
                  lc_country=con_cach_l
          while cit_count<80:
              cit_cach=linecache.getline('data\\places.txt',cit_count)
              cit_cach=cit_cach[:-1]
              cit_cach_l=cit_cach.lower()
              cit_count=cit_count+1
              if cit_cach_l==tupl_2[0]:
                  lc_city=cit_cach_l
          while stu_count<80:
              stu_cach=linecache.getline('data\\stuff.txt',stu_count)
              stu_cach=stu_cach[:-1]
              stu_cach_l=stu_cach.lower()
              stu_count=stu_count+1
              if stu_cach_l==tupl_2[0]:
                  lc_female_name=stu_cach_l
          con_count=0
          cit_count=0
          stu_count=0
  
# Third Filter: Find date in the input
  for tupl_3 in cont_tag:
      if tupl_3[1]=='CD':
          if tupl_3[0]>'1000' and tupl_3[0]<'2100':
              lc_year=tupl_3[0]
      if tupl_3[1]=='NN':
          tail_date=(tupl_3[0])[-2:]
          if tail_date=='st' or tail_date=='nd' or tail_date=='th':
              lc_date=tupl_3[0]
          while mon_count<25:
              mon_cach=linecache.getline('data\\month.txt',mon_count)
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
  situ_list=[lc_female_name,lc_male_name,lc_city,lc_country,lc_month,lc_date,lc_year]
  print(situ_list) 
  
# Fifth Filter: Find Context_linked Sentences in wikidata.txt
  count=1
  while count<200:
    if cont_tagged==[]:
       print("Sorry, there's too little information, I cannot amswer that.")
       break
    linenn=linecache.getline('data\\wikidata.txt', count)
    linenn=linenn.lower()
    linenns=nltk.word_tokenize(linenn)
    #lines_tag=t2.tag(linenns)
    count_list=0
    count_Cont=0
    count_UnNone=0
    while count_list<7:
       if situ_list[count_list] !=None:
         count_UnNone=count_UnNone+1
         print(situ_list[count_list])
         if situ_list[count_list] in linenns:
           count_Cont=count_Cont+1
       count_list=count_list+1
    #print(count,linenns)
    if count_Cont>0:
       print(count,linenns)
       linenn=linenn[:-1]
       strwrite=str(situ_list)+'['+rep_22+']'+'['+linenn+']'+'\n'
       strwrite=strwrite.encode('utf-8').decode('utf-8')
       check_list.append(strwrite)
    count=count+1


#print(check_list)
f=open(r'data\\OA_base_recover.txt','w',encoding='utf-8')
print("+++++++++")
f.writelines(check_list[1:])
f.close()

    

