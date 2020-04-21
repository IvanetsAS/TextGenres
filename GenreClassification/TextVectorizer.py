from gensim.models import Word2Vec
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import KeyedVectors

class TextVectorizer:
    def __init__(self):
        science_model = 'jetbrains://pycharm/navigate/reference?project=NLP_researches&path=baseline/science.model'
        fiction_model = 'jetbrains://pycharm/navigate/reference?project=NLP_researches&path=baseline/fiction.model'

        self.model = Word2Vec.load(fiction_model)

    def get_text_vector(self, text):
        print(text)