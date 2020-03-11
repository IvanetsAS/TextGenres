import os
import sys
import traceback
import random
import numpy as np

import Tokinizer.CorpusTokenizer
import Tokinizer.TextProcessor

# import GoogleExporter.GoogleTableExporter
from CorpusProcessor.TextData import TextData
from MyStemer import MyStemmer
from MyStemer.MyStemmer import lemmata_statistic

splitter = " <_!_> "

class Corpus:
    def __init__(self):
        self.corpus = []
        self.exportToGoogleTable = False

    def setGoogleTableExporter(self):
        print("sorry")

    def processText(self, corpus_path, genre_dir, author_dir_path, text):
        print("        " + text)
        path = corpus_path + "/" + genre_dir + "/" + author_dir_path

        try:
            current_processing = Tokinizer.TextProcessor.TextProcessor(path, text)
            metric = current_processing.getMetrics()

            text_data = TextData()
            text_data.lemmata_statistic = MyStemmer.get_lemmata_statistic(path + "/" + text)

            text_data.name = text
            text_data.genre = genre_dir
            text_data.author = author_dir_path
            text_data.add_readability_metrics(metric)
            text_data.calc_derived_metric()

            if self.exportToGoogleTable:
                self.exporter.addData([
                    text_data.genre,
                    text_data.author,
                    text_data.name,
                    text_data.words_count,
                    text_data.sentence_count,
                    text_data.characters_count,
                    text_data.vowels_count,
                    round(text_data.lemmata_statistic.get_nouns_percent(), 2),
                    round(text_data.lemmata_statistic.get_verb_percent(), 2),
                    round(text_data.lemmata_statistic.get_adj_percent(), 2),
                    round(text_data.lemmata_statistic.get_spro_percent(), 2),
                    round(text_data.fre, 2),
                    round(text_data.fkra, 2),
                    round(text_data.ari, 2)
                ])

            self.corpus.append(text_data)
        except Exception as err:
            print("ERRor" + str(err))
            traceback.format_exc()
            print(sys.exc_info()[2])

    def shuffle(self):
        random.shuffle(self.corpus)

    def get_training_set_perceptron(self):
        training_corpus = self.corpus[: round(len(self.corpus) * 0.75)]

        return [
                   [
                       text.middle_word_length_by_chars,
                       text.middle_word_length_by_vowels,
                       text.middle_sentence_length_by_words,
                       text.lemmata_statistic.get_nouns_percent(),
                       text.lemmata_statistic.get_adj_percent(),
                       text.lemmata_statistic.get_verb_percent(),
                       text.lemmata_statistic.get_spro_percent()
                   ] for text in training_corpus], [text.get_genre3_as_int() for text in training_corpus]

    def get_training_set_bayes(self):
        training_corpus = self.corpus[: round(len(self.corpus) * 0.75)]

        return np.array([
                   np.array([
                       text.middle_word_length_by_chars,
                       text.middle_word_length_by_vowels,
                       text.middle_sentence_length_by_words,
                       text.lemmata_statistic.get_nouns_percent(),
                       text.lemmata_statistic.get_adj_percent(),
                       text.lemmata_statistic.get_verb_percent(),
                       text.lemmata_statistic.get_spro_percent()
                   ]) for text in training_corpus]), np.array([text.get_genre6_as_label() for text in training_corpus])

    def get_testing_set_perceptron(self):
        testing_corpus = self.corpus[round(len(self.corpus) * 0.75):]

        return [
                   [
                       text.middle_word_length_by_chars,
                       text.middle_word_length_by_vowels,
                       text.middle_sentence_length_by_words,
                       text.lemmata_statistic.get_nouns_percent(),
                       text.lemmata_statistic.get_adj_percent(),
                       text.lemmata_statistic.get_verb_percent(),
                       text.lemmata_statistic.get_spro_percent()
                   ] for text in testing_corpus], [text.get_genre6_as_int() for text in testing_corpus]

    def get_testing_set_bayes(self):
        testing_corpus = self.corpus[round(len(self.corpus) * 0.75):]

        return np.array([
                   np.array([
                       text.middle_word_length_by_chars,
                       text.middle_word_length_by_vowels,
                       text.middle_sentence_length_by_words,
                       text.lemmata_statistic.get_nouns_percent(),
                       text.lemmata_statistic.get_adj_percent(),
                       text.lemmata_statistic.get_verb_percent(),
                       text.lemmata_statistic.get_spro_percent()
                   ]) for text in testing_corpus]), np.array([text.get_genre6_as_label() for text in testing_corpus])


    def loadCorpus(self, corpus_path):
        file_list = os.listdir(corpus_path)

        for genre_dir in file_list:
            print(genre_dir)

            file_list = os.listdir(corpus_path + "/" + genre_dir)

            for author_dir in file_list:
                print("    " + author_dir)

                file_list = os.listdir(corpus_path + "/" + genre_dir + "/" + author_dir)

                for text in file_list:
                    self.processText(corpus_path, genre_dir, author_dir, text)

    def writeMetricsFile(self, file):
        my_file = open(file, "w")

        for text in self.corpus:
            my_file.write(
                text.genre + splitter +
                text.author + splitter +
                text.name + splitter +
                str(text.words_count) + splitter +
                str(text.sentence_count) + splitter +
                str(text.characters_count) + splitter +
                str(text.vowels_count) + splitter +
                str(text.middle_word_length_by_chars) + splitter +
                str(text.middle_word_length_by_vowels) + splitter +
                str(text.middle_sentence_length_by_words) + splitter +
                str(text.fre) + splitter +
                str(text.fkra) + splitter +
                str(text.ari) + splitter +
                str(text.lemmata_statistic.nouns_count) + splitter +
                str(text.lemmata_statistic.adj_count) + splitter +
                str(text.lemmata_statistic.verbs_count) + splitter +
                str(text.lemmata_statistic.spro_count) + "\n"
            )
        my_file.write("Мне нравится Python!\nЭто классный язык!")
        my_file.close()

    def loadCorpusFromFile(self, file):
        self.corpus = []
        corpus_file = open(file)
        corpus_file_content = corpus_file.read()

        for text_line in corpus_file_content.split("\n"):
            metrics = text_line.split(splitter)

            text = TextData()
            text.genre = metrics[0]
            text.author = metrics[1]
            text.name = metrics[2]
            text.words_count = float(metrics[3])
            text.sentence_count = float(metrics[4])
            text.characters_count = float(metrics[5])
            text.vowels_count = float(metrics[6])
            text.middle_word_length_by_chars = float(metrics[7])
            text.middle_word_length_by_vowels = float(metrics[8])
            text.middle_sentence_length_by_words = float(metrics[8])
            text.fre = float(metrics[9])
            text.fkra = float(metrics[10])
            text.ari = float(metrics[11])

            text.lemmata_statistic = lemmata_statistic(
                {
                    "S": float(metrics[12]),
                    "A": float(metrics[13]),
                    "V": float(metrics[14]),
                    "SPRO": float(metrics[15])
                },
                text.words_count
            )

            if "Poniediel_nik nachinaietsia v subbotu" in text.name:
                self.ponedelnik = text
            else:
                if "Val_tier Skott. Sobraniie sochinienii v dvadtsati tomakh. Tom 8".lower() in text.name.lower():
                    self.tom8 = text
                else:
                    if "Tom 4. Prikliuchieniia Toma Soiiera".lower() in text.name.lower():
                        self.soer = text
                    else:
                        self.corpus.append(text)
        corpus_file.close()
