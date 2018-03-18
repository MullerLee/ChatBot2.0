import nltk
#from nltk import tokenizer
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger
from nltk.tag import BigramTagger
from nltk.corpus import treebank
from nltk.metrics import *
import linecache


Edit_Dis = [None] * 10

Means_Result = [None] * 5

Rou_Count  = 0
Line_Count = 0
Total_Line = 0
Corre_Line = 0

Ques = [None] * 10
Answ = [None] * 10
Accu = [None] * 10

while Rou_Count <5:
  while Line_Count < 10:
    Line_Count=Line_Count+1
    Total_Line=Rou_Count*10+Line_Count
    line=linecache.getline('data\\QAbase.txt',Total_Line)
    start1=0
    search1='['
    search2=']'
    index1 = line.find(search2, start1)
    start2 = index1+1
    index2 = line.find(search2, start2)

    Ques[Line_Count-1] = line[start1+1:index1]
    Answ[Line_Count-1] = line[start2+1:index2]
    Accu[Line_Count-1] = line[index2+2]

    if Accu[Line_Count-1]=='1':
        Corre_Line=Line_Count-1

    Edit_Dis[Line_Count-1]=(len(line)-(edit_distance(Ques[Line_Count-1],Answ[Line_Count-1])))/len(line)

  i=0
  Edit_total=0
  while i<10:
    if i!=Corre_Line:
      Edit_total=Edit_total+Edit_Dis[i]
    i=i+1
  Edit_Ave=Edit_total/9
  
  #print(Edit_Ave)
  #print(Edit_Dis[Corre_Line])

  Means_Result[Rou_Count]=Edit_Dis[Corre_Line]-Edit_Ave
  
  Rou_Count=Rou_Count+1
  Line_Count=0
  Corre_Line=0

print(Means_Result)
