import pickle

from CorpusProcessor import Corpus
from keras import models
from keras import layers
import numpy as np


def print_genres(genres):
    for genre_val in genres:
        print(" " + str(genre_val))


# CONSTANTS
class_count = 3
model_path_to_save = "/home/ivanetc/PycharmProjects/Readability/Resources/Artefacts/Perceptron_" + str(
    class_count) + "_classes_08.05.20"

# LOADING CORPUS
corpus = Corpus()
corpus.loadCorpusFromFile(
    "/home/ivanetc/PycharmProjects/Readability/Resources/corpus_file/vectorized_updated_corpus_file.txt")
corpus.shuffle()

train_textes, train_genres = corpus.get_training_set_perceptron(class_count)
test_textes, test_genres = corpus.get_testing_set_perceptron(class_count)

# TRAINING MODEL NEURAL NETWORK

network = models.Sequential()
network.add(layers.Dense(507, activation='sigmoid', input_shape=(507,)))
network.add(layers.Dense(250, activation='sigmoid'))
network.add(layers.Dense(class_count, activation='sigmoid'))
network.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

network.fit(np.array(train_textes), np.array(train_genres), epochs=1500, batch_size=32)

from tensorflow.keras.models import load_model

network.save(model_path_to_save)  # creates a HDF5 file 'my_model.h5'
network.save_weights(model_path_to_save + "_weights.h5")
# del model  # deletes the existing model

# # returns a compiled model
# # identical to the previous one
# model = load_model('my_model')


test_loss, test_acc = network.evaluate(np.array(test_textes), np.array(test_genres))
print('test_acc:', test_acc, 'test_loss', test_loss)

# SAVING MODEL
# with open(model_path_to_save, 'wb') as file:
#     pickle.dump(network, file)

ponedelnik = np.array([np.array([
                                    corpus.ponedelnik.middle_word_length_by_chars,
                                    corpus.ponedelnik.middle_word_length_by_vowels,
                                    corpus.ponedelnik.middle_sentence_length_by_words,
                                    corpus.ponedelnik.lemmata_statistic.get_nouns_percent(),
                                    corpus.ponedelnik.lemmata_statistic.get_adj_percent(),
                                    corpus.ponedelnik.lemmata_statistic.get_verb_percent(),
                                    corpus.ponedelnik.lemmata_statistic.get_spro_percent()
                                ] + corpus.ponedelnik.vector)])

ponedelnik_classes = network.predict(ponedelnik)
print("Понедельник начинается в субботу")
print_genres(ponedelnik_classes)

tom8 = np.array([np.array([
                              corpus.tom8.middle_word_length_by_chars,
                              corpus.tom8.middle_word_length_by_vowels,
                              corpus.tom8.middle_sentence_length_by_words,
                              corpus.tom8.lemmata_statistic.get_nouns_percent(),
                              corpus.tom8.lemmata_statistic.get_adj_percent(),
                              corpus.tom8.lemmata_statistic.get_verb_percent(),
                              corpus.tom8.lemmata_statistic.get_spro_percent()
                          ] + corpus.tom8.vector)])

avengo_classes = network.predict(tom8)
print("Айвенго ")
print_genres(avengo_classes)

soer = np.array([np.array([
                              corpus.soer.middle_word_length_by_chars,
                              corpus.soer.middle_word_length_by_vowels,
                              corpus.soer.middle_sentence_length_by_words,
                              corpus.soer.lemmata_statistic.get_nouns_percent(),
                              corpus.soer.lemmata_statistic.get_adj_percent(),
                              corpus.soer.lemmata_statistic.get_verb_percent(),
                              corpus.soer.lemmata_statistic.get_spro_percent()
                          ] + corpus.soer.vector)])

soer_result = network.predict(soer)
print("Том Сойер ")
print_genres(soer_result)

