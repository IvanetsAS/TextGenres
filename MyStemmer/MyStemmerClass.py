import re
import subprocess

from MyStemmer.LemmataStatisticsClass import lemmata_statistic


class Stemmer(object):

    def __init__(self, text_dir):

        cmd = ["/home/ivanetc/PycharmProjects/Readability/Resources/utils/mystem", "-nlicg", text_dir]
        output = subprocess.check_output(cmd).decode("utf-8")

        lemmata = {}
        lemmata_text = []

        word_count = 0

        for line in output.split("\n"):
            word_match = re.search("[а-яА-Я]+=[a-zA-ZА]+[,=]", line)

            if word_match:
                # if word_match and "PR" not in word_match[0]:
                word = word_match[0].replace(",", "").split("=")

                if word[1] in lemmata.keys():
                    lemmata[word[1]] += 1
                else:
                    lemmata[word[1]] = 1

                lemmata_text.append(word[0] + "_" + word[1])
                word_count += 1

            else:
                if "." in line or "!" in line or "?" in line:
                    lemmata_text.append("._prep")

        self.lemmata_statistic = lemmata_statistic(lemmata, word_count)
        self.lemmata_text = lemmata_text

