import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer=RegexpTokenizer("[\w]+")
tokenizer.tokenize("Don't heisitate to ask questions.")

import nltk
from nltk.tokenize import regexp_tokenize
sent="Don't heisitate to ask questions."
print(regexp_tokenize(sent,pattern='\w+|\$[\d\.]+|\S+'))

import nltk
from nltk.tokenize import RegexpTokenizer
tokenizer=RegexpTokenizer('\s+',gaps=True)
tokenizer.tokenize("Don't heisitate to ask questions")
