import codecs
import string
import nltk

tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
inDirection = 'D:\\myStudyFiles\\1course\\лингвистика\\художественные тексты\\polish.txt'
outDirection = 'D:\\myStudyFiles\\1course\\лингвистика\\Rreadability\\polish.txt.tokens'
income = codecs.open(inDirection, 'r', 'utf-8')
output = codecs.open(outDirection, 'w', 'utf-8')
j = 0
text = income.read()
toks = nltk.word_tokenize(text)
sents = nltk.sent_tokenize(text)
for tok in toks:
    output.write(tok.lower() + '\n')
income.close()
output.close()
print(len(sents))