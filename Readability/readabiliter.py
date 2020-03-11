import string
import re
import codecs
from Readability.tokenizer3 import Tokenizer
from Readability.segmentizer3 import Segmentizer

class Readabiliter(object):
    def __init__(self):
        self.vowels = set('ёуеыаоэяию')
        self.ctr_w = 0
        self.ctr_s = 0
        self.ctr_v = 0
        self.ctr_c = 0
        self.FKRA = 0
        self.ARI = 0
        self.FRE = 0


    def calcReadability(self, tempFilePath, textName, text):
        tokensPath = tempFilePath + '\\' + textName + '.tokens'
        tokensTempFile = codecs.open(tokensPath, 'w', 'utf-8')
        tok_r = Tokenizer()
        tokens = tok_r.tokenize(text)

        def isRus(word):
            if (re.match(r'[a-zA-Z]', word)):
                return False
            else:
                return True

        mySegmentizer = Segmentizer()
        sentences = mySegmentizer.segmentize(tokens)
        for sentence in sentences:
            tokensTempFile.write("<S>\n")
            for x in sentence:
                if isRus(x[1]):
                    tokensTempFile.write(x[1] + '\n')
            tokensTempFile.write("</S>\n")
        tokensTempFile.close()

        with open(tokensPath, 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.strip()
                if line == '<S>':  # начало предложения
                    self.ctr_s += 1
                    continue
                if line == '</S>':  # конец предложения
                    continue
                word = line.strip(string.punctuation)
                word = word.strip(' ')
                self.ctr_c += len(word)
                if word.isdigit():
                    word = ''
                if word:
                    self.ctr_w += 1
                    vow = [x for x in word.lower() if x in self.vowels]
                    self.ctr_v += len(vow)

        print('Sentences:', self.ctr_s)
        print('Words:', self.ctr_w)
        print('Vowels:', self.ctr_v)
        print('Characters:', self.ctr_c)

        self.ARI = 4.71 * (float(self.ctr_c) / self.ctr_w) + 0.5 * (float(self.ctr_w) / self.ctr_s) - 21.43
        self.FRE = 206.835 - 1.3 * (float(self.ctr_w) / self.ctr_s) - 60.1 * (float(self.ctr_v) / self.ctr_w)
        self.FKRA = 0.39 * float(self.ctr_w) / self.ctr_s + 11.8 * float(self.ctr_v) / self.ctr_w - 10.59

        #print('wl:', self.ctr_w / self.ctr_s)
        #print('sl:', self.ctr_v / self.ctr_w)
        print('ReadabilityFKRA:', self.FKRA)
        print('ReadabilityFRE:', self.FRE)
        print('ReadabilityARI:', self.ARI)