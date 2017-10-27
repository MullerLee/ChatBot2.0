import nltk
text = "NLTK is a leading platform for building Python programs to work with human language data. 
It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, 
along with a suite of text processing libraries for classification, tokenization, 
stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum."
from nltk.tokenize import sent_tokenize
sent_tokenize(text)




french_tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
text = "Sois toujours l'coute de tes plus profonds dsirs. Tiens eux comme tu tiens la vie, car sans eux, la vie n'est rien. "
french_tokenizer.tokenize(text)
