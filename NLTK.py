#This Parts aim to give an example on string dividing.
#Input 1
import nltk
text = "NLTK is a leading platform for building Python programs to work with human language data. 
It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, 
along with a suite of text processing libraries for classification, tokenization, 
stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum."
from nltk.tokenize import sent_tokenize
sent_tokenize(text)
#Input 2
french_tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
text = "Sois toujours l'coute de tes plus profonds dsirs. Tiens eux comme tu tiens la vie, car sans eux, la vie n'est rien. "
french_tokenizer.tokenize(text)
#Input 3
text = nltk.word_tokenize("NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.")
print(text)
#Input 4
from nltk import word_tokenize
r = input("Please write a text")
print("The length of text is",len(word_tokenize(r)),"words")
#Input 5
from nltk.tokenize import TreebankWordTokenizer
tokenizer  = TreebankWordTokenizer()
tokenizer.tokenize("Have a nice day. I hope you find the book interesting!")
#Input 6
text = nltk.word_tokenize("Don't hesitate to ask questions.")
print(text)
#Input 7
from nltk.tokenize import WordPunctTokenizer
tokenizer = WordPunctTokenizer()
tokenizer.tokenize("Don't hesitate to ask questions.")

