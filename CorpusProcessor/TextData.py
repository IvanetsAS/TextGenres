class TextData:
    def __init__(self):
        self.words_count = 0
        self.characters_count = 0
        self.sentence_count = 0
        self.vowels_count = 0
        self.ari = 0.0
        self.fre = 0.0
        self.fkra = 0.0

        self.lemmata_statistic = None

        self.middle_word_length_by_vowels = None
        self.middle_word_length_by_chars = None
        self.middle_sentence_length_by_words = None

        self.genre = ""
        self.author = ""
        self.name = ""

        self.vector = []
        self.lemmata_text = []
        self.text_string = ""
        self.path = ""
        self.prediction_result = []
        self.max_surence = 0

    def add_readability_metrics(self, metric):
        self.words_count = int(metric.wordCount)
        self.sentence_count = int(metric.sentencesCount)
        self.characters_count = int(metric.charactersCount)
        self.vowels_count = int(metric.vowelsCount)
        self.fre = float(metric.FRE)
        self.fkra = float(metric.FKRA)
        self.ari = float(metric.ARI)

    def calc_derived_metric(self):

        if self.words_count != 0:
            self.middle_word_length_by_chars = self.characters_count / self.words_count

        if self.words_count != 0:
            self.middle_word_length_by_vowels = self.vowels_count / self.words_count

        if self.sentence_count != 0:
            self.middle_sentence_length_by_words = self.words_count / self.sentence_count

    def get_genre6_as_int(self):
        if self.genre.lower() == "Фэнтези (сложное)".lower():
            return [0.9, 0.2, 0.2, 0.2, 0.2, 0.2]

        if self.genre.lower() == "Фэнтези (простое)".lower():
            return [0.2, 0.9, 0.2, 0.2, 0.2, 0.2]

        if self.genre.lower() == "Фантастика (сложное)".lower():
            return [0.2, 0.2, 0.9, 0.2, 0.2, 0.2]

        if self.genre.lower() == "Фантастика (простое)".lower():
            return [0.2, 0.2, 0.2, 0.9, 0.2, 0.2]

        if self.genre.lower() == "Приключенческая (простое)".lower():
            return [0.2, 0.2, 0.2, 0.2, 0.9, 0.2]

        if self.genre.lower() == "Приключенческая (сложное)".lower():
            return [0.2, 0.2, 0.2, 0.2, 0.2, 0.9]

        return [0.16, 0.16, 0.16, 0.16, 0.16, 0.16]

    def get_genre3_as_int(self):
        if "Фэнтези".lower() in self.genre.lower():
            return [0.92, 0.04, 0.04]

        if "Фантастика".lower() in self.genre.lower():
            return [0.04, 0.92, 0.04]

        if "Приключенческая".lower() in self.genre.lower():
            return [0.04, 0.04, 0.92]

        return [0.33, 0.33, 0.33]

    def get_genre2_as_int(self):
        if "простое".lower() in self.genre.lower():
            return [0.99, 0.01]

        if "сложное".lower() in self.genre.lower():
            return [0.01, 0.99]

        return [0.5, 0.5]

    def get_genre3_as_label(self):
        if "Фэнтези".lower() in self.genre.lower():
            return 1

        if "Фантастика".lower() in self.genre.lower():
            return 2

        if "Приключенческая".lower() in self.genre.lower():
            return 3
        return 0

    def get_genre2_as_label(self):
        if "простое".lower() in self.genre.lower():
            return 1

        if "сложное".lower() in self.genre.lower():
            return 2

        return 0

    def get_genre6_as_label(self):
        if self.genre.lower() == "Фэнтези (сложное)".lower():
            return 1

        if self.genre.lower() == "Фэнтези (простое)".lower():
            return 2

        if self.genre.lower() == "Фантастика (сложное)".lower():
            return 3

        if self.genre.lower() == "Фантастика (простое)".lower():
            return 4

        if self.genre.lower() == "Приключенческая (простое)".lower():
            return 5

        if self.genre.lower() == "Приключенческая (сложное)".lower():
            return 6

        return 0