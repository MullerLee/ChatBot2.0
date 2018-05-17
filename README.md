# ChatBot2.0
A  development of chat bot with the tools of statistics and NLTK packages. Mainly use Python.
This is version 2.0+, mianly use python to enhaunse some functions.
#brief introduction
-------------------
Here are instructions of every files:

#folder "1.Context"
-----------------
Folder Context mainly use the corpus of "overheard", which contained more than 20000 conversations online, to analyse which part-of-speech mainly appear in the questioning sentences. 
All the python files in this folder contains the codes of drawing the scatter graphes, which show the frequencies of certain part-of-speeches. All these graphes are contained in the folder as well.
File Analysis contains some standardized statistics and reveals how we choose the certain part-of-speeches to do advanced calculate and analysis.
The specific functions of every files can be seen when you open them.

#folder "Result"
------------------------

#folder "ChatSys"
------------------------
This Folder is the important folder "ChatSys", which is a basic chat system use " Context Vector" to achieve distinguishing the situation of a conversation (mainly questioning sentences). There is a data folder inside which is the used database in the system.
The systems remains some bugs though, but it successfully achieves the function of finding the "Context Vector" to help us analysing a conversation in our chat system as an example
The SDSBC.py file in ChatSys folder is the structure of the system, while others are the supporting files. For instance, file establish_database.py is used to create database that will be used in our system. The specific functions of every files can be seen while you open them.
