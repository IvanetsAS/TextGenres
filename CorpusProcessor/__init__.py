import os
import sys
import traceback
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import Tokinizer.CorpusTokenizer
import Tokinizer.TextProcessor

# import GoogleExporter.GoogleTableExporter
from CorpusProcessor.TextData import TextData
from GenreClassification import TextVectorizer
from MyStemmer.LemmataStatisticsClass import lemmata_statistic
from MyStemmer.MyStemmerClass import Stemmer

splitter = " <_!_> "
empty_text_data = TextData()


def get_text_features(text):
    return [
               text.middle_word_length_by_chars,
               text.middle_word_length_by_vowels,
               text.middle_sentence_length_by_words,
               text.lemmata_statistic.get_nouns_percent(),
               text.lemmata_statistic.get_adj_percent(),
               text.lemmata_statistic.get_verb_percent(),
               text.lemmata_statistic.get_spro_percent()
           ] + text.vector


def convert_to_lemmata_string(lemmata_text):
    result_string = ""
    for lemmata in lemmata_text:
        result_string += str(lemmata).lower() + " "
    return result_string


class Corpus:
    def __init__(self):
        self.file_to_write = open("/home/ivanetc/PycharmProjects/Readability/Resources/corpus_file/vectorized_updated_corpus_file.txt",
                    'a')
        self.corpus = []
        self.exportToGoogleTable = False

    def setGoogleTableExporter(self):
        print("sorry")

    def calc_tf_idf_vector(self):
        print("TF_IDF")

        file = open("/home/ivanetc/PycharmProjects/Readability/Resources/corpus_file/tf_idf_vectorized_corpus_file.txt",
                    'a')

        documents = [convert_to_lemmata_string(text_data.lemmata_text) for text_data in self.corpus]

        tfidf_vectorizer = TfidfVectorizer()
        values = tfidf_vectorizer.fit_transform(documents)
        feature_names = tfidf_vectorizer.get_feature_names()

        text_number = 0
        for text_data in self.corpus:
            print("TF_IDF: " + text_data.name)
            text_data.vector = TextVectorizer.get_text_vector(text_data.lemmata_text, values, feature_names,
                                                              text_number)
            self.write_text_data_in_file(file, text_data)
            text_number += 1

            self.corpus.remove(text_data)

        file.close()

    def processText(self, corpus_path, genre_dir, author_dir_path, text):
        print("        " + text)
        path = corpus_path + "/" + genre_dir + "/" + author_dir_path

        try:
            current_processing = Tokinizer.TextProcessor.TextProcessor(path, text)
            metric = current_processing.getMetrics()

            text_data = TextData()
            text_data.path = path

            text_my_stemmer = Stemmer(path + "/" + text)
            text_data.lemmata_statistic = text_my_stemmer.lemmata_statistic
            text_data.lemmata_text = text_my_stemmer.lemmata_text
            text_data.vector = TextVectorizer.get_simple_text_vector(text_my_stemmer.lemmata_text)

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

            #self.corpus.append(text_data)
            self.write_text_data_in_file(self.file_to_write, text_data)
        except Exception as err:
            print("ERRor" + str(err))
            traceback.format_exc()
            print(sys.exc_info()[2])

    def shuffle(self):
        random.shuffle(self.corpus)

    def get_training_set_perceptron(self, class_count):
        training_corpus = self.corpus[: round(len(self.corpus) * 0.75)]

        return self.get_perceptron_set(class_count, training_corpus)

    def get_testing_set_perceptron(self, class_count):
        testing_corpus = self.corpus[round(len(self.corpus) * 0.75):]

        return self.get_perceptron_set(class_count, testing_corpus)

    @staticmethod
    def get_perceptron_set(class_count, training_corpus):
        if class_count == 2:
            labels = [text.get_genre2_as_int() for text in training_corpus]
        else:
            if class_count == 3:
                labels = [text.get_genre3_as_int() for text in training_corpus]
            else:
                labels = [text.get_genre6_as_int() for text in training_corpus]
        return [get_text_features(text) for text in training_corpus], labels

    def get_training_set_bayes(self, classes_count):
        training_corpus = self.corpus[: round(len(self.corpus) * 0.75)]

        if classes_count == 2:
            training_labels = np.array([text.get_genre2_as_label() for text in training_corpus])
        else:
            if classes_count == 3:
                training_labels = np.array([text.get_genre3_as_label() for text in training_corpus])
            else:
                training_labels = np.array([text.get_genre6_as_label() for text in training_corpus])

        return np.array([np.array(get_text_features(text)) for text in training_corpus]), training_labels



    def get_testing_set_bayes(self, classes_count):
        testing_corpus = self.corpus[round(len(self.corpus) * 0.75):]

        if classes_count == 2:
            training_labels = np.array([text.get_genre2_as_label() for text in testing_corpus])
        else:
            if classes_count == 3:
                training_labels = np.array([text.get_genre3_as_label() for text in testing_corpus])
            else:
                training_labels = np.array([text.get_genre6_as_label() for text in testing_corpus])

        return np.array([np.array(get_text_features(text)) for text in testing_corpus]), training_labels

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

        self.file_to_write.close()

    def writeMetricsFile(self, file):
        my_file = open(file, "w")

        for text in self.corpus:
            self.write_text_data_in_file(my_file, text)

        my_file.write("FINISH!!!")
        my_file.close()

    def write_text_data_in_file(self, my_file, text):
        text_data_string = text.genre + splitter
        text_data_string += text.author + splitter
        text_data_string += text.name + splitter
        text_data_string += str(text.words_count) + splitter
        text_data_string += str(text.sentence_count) + splitter
        text_data_string += str(text.characters_count) + splitter
        text_data_string += str(text.vowels_count) + splitter
        text_data_string += str(text.middle_word_length_by_chars) + splitter
        text_data_string += str(text.middle_word_length_by_vowels) + splitter
        text_data_string += str(text.middle_sentence_length_by_words) + splitter
        text_data_string += str(text.fre) + splitter
        text_data_string += str(text.fkra) + splitter
        text_data_string += str(text.ari) + splitter
        text_data_string += str(text.lemmata_statistic.nouns_count) + splitter
        text_data_string += str(text.lemmata_statistic.adj_count) + splitter
        text_data_string += str(text.lemmata_statistic.verbs_count) + splitter
        text_data_string += str(text.lemmata_statistic.spro_count)
        for vector_point in text.vector:
            text_data_string += splitter + str(vector_point)
        text_data_string += "\n"
        my_file.write(text_data_string)

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
            text.middle_sentence_length_by_words = float(metrics[9])
            text.fre = float(metrics[10])
            text.fkra = float(metrics[11])
            text.ari = float(metrics[12])

            text.lemmata_statistic = lemmata_statistic(
                {
                    "S": float(metrics[13]),
                    "A": float(metrics[14]),
                    "V": float(metrics[15]),
                    "SPRO": float(metrics[16])
                },
                text.words_count
            )
            text.vector = [float(metric) for metric in metrics[17:517]]

            if "Poniediel_nik nachinaietsia v subbotu" in text.name:
                self.ponedelnik = text
            else:
                if "Айвенго".lower() in text.name.lower():
                    self.tom8 = text
                else:
                    if "Приключения Тома".lower() in text.name.lower():
                        self.soer = text
                    else:
                        if "Игра престолов".lower() in text.name.lower():
                            self.got = text
                        else:
                            self.corpus.append(text)
        corpus_file.close()

    def convert_corpus_for_w2v(self, corpus_input_path, corpuse_output_path):
        file_list = os.listdir(corpus_input_path)

        for genre_dir in file_list:
            print(genre_dir)

            file_list = os.listdir(corpus_input_path + "/" + genre_dir)

            for author_dir in file_list:
                print("    " + author_dir)

                file_list = os.listdir(corpus_input_path + "/" + genre_dir + "/" + author_dir)

                for text in file_list:
                    print("        " + text)
                    path = corpus_input_path + "/" + genre_dir + "/" + author_dir
                    text_my_stemmer = Stemmer(path + "/" + text)

                    output_file = open(corpuse_output_path + "/" + text,'w')

                    for lemmata in text_my_stemmer.lemmata_text:
                        if "._prep" in lemmata:
                            output_file.write("\n")
                        else:
                            output_file.write(" " + lemmata)
                    output_file.close()