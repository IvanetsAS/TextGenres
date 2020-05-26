from gensim.models import Word2Vec
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import KeyedVectors

science_model = 'jetbrains://pycharm/navigate/reference?project=NLP_researches&path=baseline/science.model'
fiction_model = '/home/ivanetc/PycharmProjects/NLP_researches/baseline/fiction.model'
from nltk.corpus import stopwords
ru_stopwords = set(stopwords.words('russian'))
model = Word2Vec.load(fiction_model)
null_vector = [0 for i in range(500)]

def get_text_vector(lemmata_text, tf_idf_values, tf_idf_features_names, text_number):

    vector = null_vector
    useful_lemmata_count = 0

    for lemmata in lemmata_text:
        lemmata_arr = lemmata.split("_")
        if "SPRO" not in lemmata and lemmata in model and str(lemmata_arr[0]).lower() not in ru_stopwords:
            current_lemmata_vector = model[lemmata]

            if lemmata.lower() in tf_idf_features_names:
                useful_lemmata_count += 1
                tf_idf = tf_idf_values[text_number, tf_idf_features_names.index(lemmata.lower())]
                vector = [vi + wi * tf_idf for vi, wi in zip(vector, current_lemmata_vector)]
            else:
                print(lemmata + " not in list")

    return [vi / useful_lemmata_count for vi in vector]

def get_simple_text_vector(lemmata_text):

    vector = null_vector
    useful_lemmata_count = 0

    for lemmata in lemmata_text:
        lemmata_arr = lemmata.split("_")
        if "SPRO" not in lemmata and lemmata in model and str(lemmata_arr[0]).lower() not in ru_stopwords:
            current_lemmata_vector = model[lemmata]
            useful_lemmata_count += 1
            vector = [vi + wi for vi, wi in zip(vector, current_lemmata_vector)]

    return [vi / useful_lemmata_count for vi in vector]

#
#
# from gensim.models import Word2Vec
#
# from MyStemmer.MyStemmerClass import Stemmer
#
#
# # my_stemmer = Stemmer("/home/ivanetc/PycharmProjects/Readability/GenreCorpus/Приключенческая (простое)/Твен/Nalieghkie - Mark Tvien.txt")
# # stat = my_stemmer.lemmata_statistic
# # text = my_stemmer.lemmata_text
#
#
# MODEL_NAME = ''
# model = Word2Vec.load(MODEL_NAME)
# vector = model[text[0]]
