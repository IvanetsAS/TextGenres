import os


class lemmata_statistic:
    def __init__(self, lemmata, words_count):

        if "S" in lemmata.keys():
            self.nouns_count = lemmata["S"]
        else:
            self.nouns_count = 0

        if "A" in lemmata.keys():
            self.adj_count = lemmata["A"]
        else:
            self.adj_count = 0

        if "V" in lemmata.keys():
            self.verbs_count = lemmata["V"]
        else:
            self.verbs_count = 0

        if "SPRO" in lemmata.keys():
            self.spro_count = lemmata["SPRO"]
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
