from CorpusProcessor import Corpus
from sklearn.naive_bayes import GaussianNB
import pickle
import numpy as np

# CONSTANTS
genres6 = {1: "Фэнтези (сложное)", 2: "Фэнтези (простое)", 3:"Фантастика (сложное)", 4:"Фантастика (простое)", 5:"Приключенческая (простое)", 6:"Приключенческая (сложное)"}
genres3 = {1: "Фэнтези", 2: "Фантастика", 3:"Приключенческая"}
genres2 = {1: "Простое", 2: "Сложное"}
class_count = 3
if class_count == 2:
    genres = genres2
else:
    if class_count == 3:
        genres = genres3
    else:
        genres = genres6

model_path_to_save = "/home/ivanetc/PycharmProjects/Readability/Resources/Artefacts/Bayes_"+ str(class_count) + "_classes_27.04.20"

# LOADING CORPUS
corpus = Corpus()
corpus.loadCorpusFromFile("/home/ivanetc/PycharmProjects/Readability/Resources/corpus_file/vectorized_updated_corpus_file.txt")
corpus.shuffle()

# TRAINING MODEL Bayes
gnb_model = GaussianNB()

train_textes, train_genres = corpus.get_training_set_bayes(class_count)
test_textes, test_genres = corpus.get_testing_set_bayes(class_count)

y_pred = gnb_model.fit(train_textes, train_genres).predict(test_textes)

print("Number of mislabeled points out of a total %d points : %d" % (test_textes.shape[0], (test_genres != y_pred).sum()))
print("Acc" + str(1 - (test_genres != y_pred).sum() / test_textes.shape[0]))


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


ponedelnik = np.array([np.array([
    corpus.ponedelnik.middle_word_length_by_chars,
    corpus.ponedelnik.middle_word_length_by_vowels,
    corpus.ponedelnik.middle_sentence_length_by_words,
    corpus.ponedelnik.lemmata_statistic.get_nouns_percent(),
    corpus.ponedelnik.lemmata_statistic.get_adj_percent(),
    corpus.ponedelnik.lemmata_statistic.get_verb_percent(),
    corpus.ponedelnik.lemmata_statistic.get_spro_percent()
] + corpus.ponedelnik.vector)])

ponedelnik_result = gnb_model.predict(ponedelnik)
print("Понедельник начинается в субботу " + genres[ponedelnik_result[0]])


tom8 = np.array([np.array([
    corpus.tom8.middle_word_length_by_chars,
    corpus.tom8.middle_word_length_by_vowels,
    corpus.tom8.middle_sentence_length_by_words,
    corpus.tom8.lemmata_statistic.get_nouns_percent(),
    corpus.tom8.lemmata_statistic.get_adj_percent(),
    corpus.tom8.lemmata_statistic.get_verb_percent(),
    corpus.tom8.lemmata_statistic.get_spro_percent()
] + corpus.tom8.vector)])

tom8_result = gnb_model.predict(tom8)
print("Айвенго " + genres[tom8_result[0]])

soer = np.array([np.array([
    corpus.soer.middle_word_length_by_chars,
    corpus.soer.middle_word_length_by_vowels,
    corpus.soer.middle_sentence_length_by_words,
    corpus.soer.lemmata_statistic.get_nouns_percent(),
    corpus.soer.lemmata_statistic.get_adj_percent(),
    corpus.soer.lemmata_statistic.get_verb_percent(),
    corpus.soer.lemmata_statistic.get_spro_percent()
] + corpus.soer.vector)])

soer_result = gnb_model.predict(soer)
print("Том Сойер " + genres[soer_result[0]])

# SAVING MODEL
with open(model_path_to_save, 'wb') as file:
    pickle.dump(gnb_model, file)