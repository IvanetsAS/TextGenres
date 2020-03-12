# from keras import models
# from keras import layers
import numpy as np

genres6 = {1: "Фэнтези (сложное)", 2: "Фэнтези (простое)", 3:"Фантастика (сложное)", 4:"Фантастика (простое)", 5:"Приключенческая (простое)", 6:"Приключенческая (сложное)"}
genres3 = {1: "Фэнтези", 2: "Фантастика", 3:"Приключенческая"}
genres2 = {1: "Простое", 2: "Сложное"}

import CorpusProcessor
corpus = CorpusProcessor.Corpus()
corpus.loadCorpusFromFile("/home/ivanetc/PycharmProjects/Readability/GenreCorpus/corpus_file.txt")
corpus.shuffle()
train_textes, train_genres = corpus.get_training_set_perceptron()
test_textes, test_genres = corpus.get_testing_set_perceptron()


# network = models.Sequential()
# network.add(layers.Dense(7, activation='sigmoid', input_shape=(7,)))
# network.add(layers.Dense(7, activation='sigmoid'))
# network.add(layers.Dense(3, activation='sigmoid'))
# network.compile(optimizer='adam',
#                 loss='categorical_crossentropy',
#                 metrics=['accuracy'])
#
# network.fit(np.array(train_textes), np.array(train_genres), epochs=10000, batch_size=64)
#
# test_loss, test_acc = network.evaluate(np.array(test_textes), np.array(test_genres))
# print('test_acc:', test_acc, 'test_loss', test_loss)
# ponedelnik = np.array([np.array([
#     corpus.ponedelnik.middle_word_length_by_chars,
#     corpus.ponedelnik.middle_word_length_by_vowels,
#     corpus.ponedelnik.middle_sentence_length_by_words,
#     corpus.ponedelnik.lemmata_statistic.get_nouns_percent(),
#     corpus.ponedelnik.lemmata_statistic.get_adj_percent(),
#     corpus.ponedelnik.lemmata_statistic.get_verb_percent(),
#     corpus.ponedelnik.lemmata_statistic.get_spro_percent()
# ])])
#
#
# potter = np.array([np.array([
#     5.3062,
#     2.29677,
#     12.1126,
#     0.26314,
#     0.07961,
#     0.19501,
#     0.10071
# ])])
# potter_classes = network.predict(potter)
#
# print("potter")
# for genre in potter_classes:
#     print(genre)
#
#
# # ponedelnik_classes = network.predict_classes(ponedelnik)
# ponedelnik_classes = network.predict(ponedelnik)
#
# print("ponedelnik")
# for genre in ponedelnik_classes:
#     print(genre)
#
#
#
# tom8 = np.array([np.array([
#     corpus.tom8.middle_word_length_by_chars,
#     corpus.tom8.middle_word_length_by_vowels,
#     corpus.tom8.middle_sentence_length_by_words,
#     corpus.tom8.lemmata_statistic.get_nouns_percent(),
#     corpus.tom8.lemmata_statistic.get_adj_percent(),
#     corpus.tom8.lemmata_statistic.get_verb_percent(),
#     corpus.tom8.lemmata_statistic.get_spro_percent()
# ])])
# tom8_classes = network.predict(tom8)
#
# print("tom8")
# for genre in tom8_classes:
#     print(genre)
#
#
# soer = np.array([np.array([
#     corpus.soer.middle_word_length_by_chars,
#     corpus.soer.middle_word_length_by_vowels,
#     corpus.soer.middle_sentence_length_by_words,
#     corpus.soer.lemmata_statistic.get_nouns_percent(),
#     corpus.soer.lemmata_statistic.get_adj_percent(),
#     corpus.soer.lemmata_statistic.get_verb_percent(),
#     corpus.soer.lemmata_statistic.get_spro_percent()
# ])])
# soer_classes = network.predict(soer)
#
# print("soer")
# for genre in soer_classes:
#     print(genre)

#Bayes
# from sklearn.naive_bayes import GaussianNB
# gnb_model = GaussianNB()
#
# train_textes, train_genres = corpus.get_training_set_bayes()
# test_textes, test_genres = corpus.get_testing_set_bayes()
#
# y_pred = gnb_model.fit(train_textes, train_genres).predict(test_textes)
# print("Number of mislabeled points out of a total %d points : %d" % (test_textes.shape[0], (test_genres != y_pred).sum()))
#
# potter = np.array([np.array([
#     5.3062,
#     2.29677,
#     12.1126,
#     0.26314,
#     0.07961,
#     0.19501,
#     0.10071
# ])])
# potter_result = gnb_model.predict(potter)
# print("potter " + genres6[potter_result[0]])
#
#
# ponedelnik = np.array([np.array([
#     corpus.ponedelnik.middle_word_length_by_chars,
#     corpus.ponedelnik.middle_word_length_by_vowels,
#     corpus.ponedelnik.middle_sentence_length_by_words,
#     corpus.ponedelnik.lemmata_statistic.get_nouns_percent(),
#     corpus.ponedelnik.lemmata_statistic.get_adj_percent(),
#     corpus.ponedelnik.lemmata_statistic.get_verb_percent(),
#     corpus.ponedelnik.lemmata_statistic.get_spro_percent()
# ])])
#
# ponedelnik_result = gnb_model.predict(ponedelnik)
# print("ponedelnik " + genres6[ponedelnik_result[0]])
#
#
# tom8 = np.array([np.array([
#     corpus.tom8.middle_word_length_by_chars,
#     corpus.tom8.middle_word_length_by_vowels,
#     corpus.tom8.middle_sentence_length_by_words,
#     corpus.tom8.lemmata_statistic.get_nouns_percent(),
#     corpus.tom8.lemmata_statistic.get_adj_percent(),
#     corpus.tom8.lemmata_statistic.get_verb_percent(),
#     corpus.tom8.lemmata_statistic.get_spro_percent()
# ])])
#
# tom8_result = gnb_model.predict(tom8)
# print("tom8 " + genres6[tom8_result[0]])
#
# soer = np.array([np.array([
#     corpus.soer.middle_word_length_by_chars,
#     corpus.soer.middle_word_length_by_vowels,
#     corpus.soer.middle_sentence_length_by_words,
#     corpus.soer.lemmata_statistic.get_nouns_percent(),
#     corpus.soer.lemmata_statistic.get_adj_percent(),
#     corpus.soer.lemmata_statistic.get_verb_percent(),
#     corpus.soer.lemmata_statistic.get_spro_percent()
# ])])
#
# soer_result = gnb_model.predict(soer)
# print("soer_result " + genres6[soer_result[0]])


#ОПОРНЫЕ ВЕКТОРА
from sklearn.svm import SVC
svc_model = SVC(gamma='auto')

train_textes, train_genres = corpus.get_training_set_bayes(2)
test_textes, test_genres = corpus.get_testing_set_bayes(2)

svc_model.fit(train_textes, train_genres)

print("Score " + str(svc_model.score(test_textes, test_genres)))

potter = np.array([np.array([
    5.3062,
    2.29677,
    12.1126,
    0.26314,
    0.07961,
    0.19501,
    0.10071
])])
potter_result = svc_model.predict(potter)
print("potter " + genres6[potter_result[0]])

ponedelnik = np.array([np.array([
    corpus.ponedelnik.middle_word_length_by_chars,
    corpus.ponedelnik.middle_word_length_by_vowels,
    corpus.ponedelnik.middle_sentence_length_by_words,
    corpus.ponedelnik.lemmata_statistic.get_nouns_percent(),
    corpus.ponedelnik.lemmata_statistic.get_adj_percent(),
    corpus.ponedelnik.lemmata_statistic.get_verb_percent(),
    corpus.ponedelnik.lemmata_statistic.get_spro_percent()
])])

ponedelnik_result = svc_model.predict(ponedelnik)
print("ponedelnik " + genres6[ponedelnik_result[0]])


tom8 = np.array([np.array([
    corpus.tom8.middle_word_length_by_chars,
    corpus.tom8.middle_word_length_by_vowels,
    corpus.tom8.middle_sentence_length_by_words,
    corpus.tom8.lemmata_statistic.get_nouns_percent(),
    corpus.tom8.lemmata_statistic.get_adj_percent(),
    corpus.tom8.lemmata_statistic.get_verb_percent(),
    corpus.tom8.lemmata_statistic.get_spro_percent()
])])

tom8_result = svc_model.predict(tom8)
print("tom8 " + genres6[tom8_result[0]])

soer = np.array([np.array([
    corpus.soer.middle_word_length_by_chars,
    corpus.soer.middle_word_length_by_vowels,
    corpus.soer.middle_sentence_length_by_words,
    corpus.soer.lemmata_statistic.get_nouns_percent(),
    corpus.soer.lemmata_statistic.get_adj_percent(),
    corpus.soer.lemmata_statistic.get_verb_percent(),
    corpus.soer.lemmata_statistic.get_spro_percent()
])])

soer_result = svc_model.predict(soer)
print("soer_result " + genres6[soer_result[0]])


cor_data = []
for text_data in corpus.corpus:
    decision_func_arr = svc_model.decision_function([np.array(CorpusProcessor.get_text_features(text_data))])
    #genres2[svc_model.predict([np.array(CorpusProcessor.get_text_features(text_data))])[0]]
    cor_data.append([decision_func_arr[0], text_data.fre, text_data.fkra, text_data.ari ])

np.corrcoef(cor_data)