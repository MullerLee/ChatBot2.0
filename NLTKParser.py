>>> import nltk
>>> sent=[('Pierre', 'NNP'), ('Vinken', 'NNP'), (',', ','), ('61', 'CD'), ('years', 'NNS'), ('old', 'JJ'), (',', ','), ('will', 'MD'), ('join', 'VB'), ('the', 'DT'), ('board', 'NN'), ('as', 'IN'), ('a', 'DT'), ('nonexecutive', 'JJ'), ('director', 'NN'), ('Nov.', 'NNP'), ('29', 'CD'), ('.', '.')]
>>> grammar="NP:{<DT>?<JJ>*<NN><IN>?<NN>*}"
##the regulat expression of parser might be wrong!!!!
>>> find=nltk.RegexpParser(grammar)
>>> res=find.parse(sent)
>>> print(res)
(S
  Pierre/NNP
  Vinken/NNP
  ,/,
  61/CD
  years/NNS
  old/JJ
  ,/,
  will/MD
  join/VB
  (NP the/DT board/NN as/IN)
  (NP a/DT nonexecutive/JJ director/NN)
  Nov./NNP
  29/CD
  ./.)
>>> res.draw()
##the extra output is in the file of Parser.jpg
