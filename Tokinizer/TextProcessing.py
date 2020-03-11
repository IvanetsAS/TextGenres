import os

import Tokinizer.CorpusTokenizer
import Tokinizer.TextProcessor
import GoogleExporter.GoogleTableExporter as GE


def calc_all_texts_in_dir(path):
    """Trying to open directory"""
    try:
        file_list = os.listdir(path)
    except FileNotFoundError:
        print("Директория не найдена")
        return
    surprisal_string = ""
    exporter = GE.Exporter()
    for file in file_list:
        current_processing = Tokinizer.TextProcessor.TextProcessor(path, file)
        metrics = current_processing.getMetrics()
        print(file.title())
        print("Character count", metrics.charactersCount)
        print("Vowels count", metrics.vowelsCount)
        print("Words count", metrics.wordCount)
        print("Sentences count", metrics.sentencesCount, "\n")

        print("FRE", metrics.FRE)
        print("FKRA", metrics.FKRA)
        print("ARI", metrics.ARI, "\n")
        # current_surprisal = current_processing.calc_surprisal()
        # print("Surprisal", current_surprisal)
        # surprisal_string += file.title() + " " + current_surprisal + "\n"
        exporter.addData(metrics, file.title())
    print(surprisal_string)
    exporter.rewriteTable()


calc_all_texts_in_dir("/home/ivanetsas/Документы/Linguistic/ReadabilityCorpus/Children/School/")
