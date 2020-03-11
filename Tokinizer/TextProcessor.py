import math
import Tokinizer.CorpusTokenizer

CONTEXT = 2


class TextProcessor:
    def __init__(self, text_file_path, text_file_name):
        self.corpus = Tokinizer.CorpusTokenizer.tokenize(text_file_path, text_file_name)

    def len_syl_to_len_symb(self):
        accumulator = 0
        corp_len = 0
        vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]

        for sentence in self.corpus:
            for token in [token.value for token in sentence if token.group == "word"]:
                vow = 0
                for ch in token:
                    if ch in vowels:
                        vow += 1
                accumulator += vow / len(token)
                corp_len += 1
        return accumulator / corp_len

    def average_len(self):
        accumulator = 0
        corp_len = 0
        vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
        for sentence in self.corpus:
            for token in [token.value for token in sentence if token.group == "word"]:
                vow = 0
                for ch in token:
                    if ch in vowels:
                        vow += 1
                accumulator += vow
                corp_len += 1
        return accumulator / corp_len

    def average_sent_len(self):
        accumulator = 0
        corp_len = 0
        for sentence in self.corpus:
            accumulator += len([token.value for token in sentence if token.group == "word"])
            corp_len += 1
        return accumulator / corp_len

    def printTokens(self):
        for sentence in self.corpus:
            for token in sentence:
                print(token)
        print()
        print("{END SNT}")
        print()

    def getMetrics(self):
        metrics = TextMetrics()
        vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
        for sentence in self.corpus:
            for token in [token.value for token in sentence if token.group == "word"]:
                for ch in token:
                    if ch in vowels:
                        metrics.vowelsCount += 1
                metrics.wordCount += 1
                metrics.charactersCount += len(token)
            metrics.sentencesCount += 1

        metrics.countHighLevelMetrics()
        return metrics


    def calc_surprisal(self):
        return surprisal(self.corpus)


class TextMetrics:

    def __init__(self):
        self.vowelsCount = 0
        self.wordCount = 0
        self.sentencesCount = 0
        self.charactersCount = 0

        self.FRE = None
        self.FKRA = None
        self.ARI = None

    def countHighLevelMetrics(self):
        self.FKRA = 0.39 * self.wordCount / self.sentencesCount \
                    + 11.8 * self.vowelsCount / self.wordCount - 10.59
        self.ARI = 4.71 * self.charactersCount / self.wordCount \
                   + 0.5 * self.wordCount / self.sentencesCount - 21.43
        self.FRE = 206.835 - 1.3 * (self.wordCount / self.sentencesCount) - 60.1 * (self.vowelsCount / self.wordCount)


def flatting_corpus(corpus):
    return [token.value for sentence in corpus for token in sentence if
            token.group == "word"]


def freq_dict(corpus):
    flatted_corpus = flatting_corpus(corpus)
    dictionary = {}
    for token in flatted_corpus:
        if token in dictionary:
            dictionary[token] = dictionary[token] + 1
        else:
            dictionary[token] = 1
    return dictionary


def surprisal(corpus):
    flatted_corpus = flatting_corpus(corpus)
    i = CONTEXT
    accumulator = 0
    while i < len(flatted_corpus):
        j = i - CONTEXT
        local_context = []
        while j < i:
            local_context.append(flatted_corpus[j])
            j += 1
        local_context_count = 0
        word_in_context = 0
        j = 0
        while j < len(flatted_corpus) - 1:
            if flatted_corpus[j] == local_context[CONTEXT - 1]:
                f = True
                k = 0
                while k < CONTEXT:
                    if not flatted_corpus[j - k] == local_context[CONTEXT - k - 1]:
                        f = False
                        break
                    k += 1
                if f:
                    local_context_count += 1
                    if flatted_corpus[j + 1] == flatted_corpus[i]:
                        word_in_context += 1
            j += 1
        p_x_context = (word_in_context / len(flatted_corpus)) / (local_context_count / len(flatted_corpus))
        accumulator += math.log2(1 / p_x_context)
        if int(i) % 150 == 0:
            print(str(i) + " from " + str(len(flatted_corpus)))
        i += 1
    return accumulator / len(flatted_corpus)
