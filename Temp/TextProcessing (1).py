import math

CONTEXT = 2


def len_syl_to_len_symb(corpus):
    accumulator = 0
    corp_len = 0
    vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
    for text in corpus.texts:
        for sentence in text:
            for token in [token.value for token in sentence if token.group == "word"]:
                vow = 0
                for ch in token:
                    if ch in vowels:
                        vow += 1
                accumulator += vow / len(token)
                corp_len += 1
    return accumulator / corp_len


def average_len(corpus):
    accumulator = 0
    corp_len = 0
    vowels = ["у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"]
    for text in corpus.texts:
        for sentence in text:
            for token in [token.value for token in sentence if token.group == "word"]:
                vow = 0
                for ch in token:
                    if ch in vowels:
                        vow += 1
                accumulator += vow
                corp_len += 1
    return accumulator / corp_len


def average_sent_len(corpus):
    accumulator = 0
    corp_len = 0
    for text in corpus.texts:
        for sentence in text:
            accumulator += len([token.value for token in sentence if token.group == "word"])
            corp_len += 1
    return accumulator / corp_len


def flatting_corpus(corpus):
    return [token.value for text in corpus.texts for sentence in text for token in sentence if
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
                if f == True:
                    local_context_count += 1
                    if flatted_corpus[j + 1] == flatted_corpus[i]:
                        word_in_context += 1
            j += 1
        p_x_context = (word_in_context / len(flatted_corpus)) / (local_context_count / len(flatted_corpus))
        accumulator += math.log2(1 / p_x_context)
        print(str(i) + " from " + str(len(flatted_corpus)))
        i += 1
    return accumulator / len(flatted_corpus)



