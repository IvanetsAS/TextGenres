import os


def tokenize(file_path, file_name):

    with open(file_path + '/' + file_name) as file:
        text = file.read()
        tokenized_text = []

        """Creating FSM"""
        is_word = False
        word = ""
        sentence = []

        for ch in text:

            """Checking every symbol"""
            if ch.isalpha():
                word += ch
                is_word = True
            else:
                if is_word:
                    sentence.append(Token(word.lower(), "word"))
                    is_word = False
                    word = ""
                if ch in [".", "!", "?"]:
                    sentence.append(Token(ch, "end_snt"))
                    tokenized_text.append(sentence)
                    sentence = []
                elif not ch.isspace():
                    sentence.append(Token(ch, "inter_snt"))

        return tokenized_text


def print_tokenized_text(tokenized_text):
    for sentence in tokenized_text:
        for token in sentence:
            print(token)
        print()
        print("{END SNT}")
        print()


class Token:

    def __init__(self, value, group):
        self.value = value
        self.group = group

    def __str__(self):
        return self.value + " " + self.group
