import pickle
import numpy as np
from keras import layers

def get_max_surence(classes):
    top_prediction = 0
    for class_prediction in classes[0]:
        if class_prediction > top_prediction:
            top_prediction = class_prediction
    return  top_prediction

def get_min_maxsurence_text(textes):
    min_maxsurence_text = textes[0]
    for text in textes:
        if text.max_surence < min_maxsurence_text.max_surence:
            min_maxsurence_text = text
    return min_maxsurence_text

def get_max_maxsurence_text(textes):
    max_maxsurence_text = textes[0]
    for text in textes:
        if text.max_surence > max_maxsurence_text.max_surence:
            max_maxsurence_text = text
    return max_maxsurence_text



from CorpusProcessor import Corpus
from GenreClassification.PerceptronClassification import print_genres
from keras import models

model_path_to_save = "/home/ivanetc/PycharmProjects/Readability/Resources/Artefacts/Perceptron_3_classes_08.05.20"

network = models.Sequential()
network.add(layers.Dense(507, activation='sigmoid', input_shape=(507,)))
network.add(layers.Dense(250, activation='sigmoid'))
network.add(layers.Dense(3, activation='sigmoid'))
network.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
network.load_weights(model_path_to_save + "_weights.h5")

corpus = Corpus()
corpus.loadCorpusFromFile(
    "/home/ivanetc/PycharmProjects/Readability/Resources/corpus_file/vectorized_updated_corpus_file.txt")
corpus.shuffle()
top_sure = []
top_unsure = []

got = np.array([np.array([
                              corpus.got.middle_word_length_by_chars,
                              corpus.got.middle_word_length_by_vowels,
                              corpus.got.middle_sentence_length_by_words,
                              corpus.got.lemmata_statistic.get_nouns_percent(),
                              corpus.got.lemmata_statistic.get_adj_percent(),
                              corpus.got.lemmata_statistic.get_verb_percent(),
                              corpus.got.lemmata_statistic.get_spro_percent()
                          ] + corpus.got.vector)])



got_classes = network.predict(got)


for text in corpus.corpus:
    text_perceptron_metrics = np.array([np.array([
                              text.middle_word_length_by_chars,
                              text.middle_word_length_by_vowels,
                              text.middle_sentence_length_by_words,
                              text.lemmata_statistic.get_nouns_percent(),
                              text.lemmata_statistic.get_adj_percent(),
                              text.lemmata_statistic.get_verb_percent(),
                              text.lemmata_statistic.get_spro_percent()
                          ] + text.vector)])
    text.prediction_result = network.predict(text_perceptron_metrics)
    text.max_surence = get_max_surence(text.prediction_result)
    print(text.name + " " + str(text.prediction_result))

    if len(top_sure) < 50:
        top_sure.append(text)
    else:
        min_top_sure_text = get_min_maxsurence_text(top_sure)

        if text.max_surence > min_top_sure_text.max_surence:
            top_sure.remove(min_top_sure_text)
            top_sure.append(text)

    if len(top_unsure) < 50:
        top_unsure.append(text)
    else:
        max_min_sure_text = get_max_maxsurence_text(top_unsure)
        if text.max_surence < max_min_sure_text.max_surence:
            top_unsure.remove(max_min_sure_text)
            top_unsure.append(text)

print("_________________________________________________________________________________")
print("Top sure")
for text in top_sure:
    print(text.name + str(text.prediction_result) + text.genre)

print("_________________________________________________________________________________")
print("Top unsure")
for text in top_unsure:
    print(text.name + str(text.prediction_result) + text.genre)





print("Игра престолов ")
print_genres(got_classes)