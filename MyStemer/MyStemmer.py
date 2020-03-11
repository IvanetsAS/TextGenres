import os
import re
import subprocess


def get_lemmata_statistic(text_dir):
    cmd = ["/home/ivanetsas/Загрузки/mystem", "-nlicg", text_dir]
    output = subprocess.check_output(cmd).decode("utf-8")

    lemmata = {}
    word_count = 0

    for line in output.split("\n"):
        word_match = re.search("[а-яА-Я]+=[a-zA-ZА]+[,=]", line)

        if word_match:
            # if word_match and "PR" not in word_match[0]:
            word = word_match[0].replace(",", "").split("=")

            if word[1] in lemmata.keys():
                lemmata[word[1]] += 1
            else:
                lemmata[word[1]] = 1

            word_count += 1

            # print(word[0] + "   " + word[1])

    return lemmata_statistic(lemmata, word_count)


class lemmata_statistic:
    def __init__(self, lemmes, words_count):

        if "S" in lemmes.keys():
            self.nouns_count = lemmes["S"]
        else:
            self.nouns_count = 0

        if "A" in lemmes.keys():
            self.adj_count = lemmes["A"]
        else:
            self.adj_count = 0

        if "V" in lemmes.keys():
            self.verbs_count = lemmes["V"]
        else:
            self.verbs_count = 0

        if "SPRO" in lemmes.keys():
            self.spro_count = lemmes["SPRO"]
        else:
            self.spro_count = 0

        self.words_count = words_count

    def get_adj_percent(self):
        return self.adj_count / self.words_count * 100

    def get_verb_percent(self):
        return self.verbs_count / self.words_count * 100

    def get_nouns_percent(self):
        return self.nouns_count / self.words_count * 100

    def get_spro_percent(self):
        return self.spro_count / self.words_count * 100