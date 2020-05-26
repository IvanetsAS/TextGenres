splitter = " <_!_> "

def loadMyFile(myFile, daniels_file):
    my_corpus_file = open(myFile)
    corpus_file_content = my_corpus_file.read()

    my_corpus = []
    updated_corpus = []

    for text_line in corpus_file_content.split("\n"):
        my_corpus.append(text_line)

    daniel_corpus = open(daniels_file)

    for line in daniel_corpus.read().split("\n"):
        metrics = line.split(",")

        for my_corpus_line in my_corpus:
            if metrics[0] in my_corpus_line and metrics[0] is not "":
                updated_corpus.append( my_corpus_line + "<_!_> " + metrics[9] + "<_!_> " + metrics[10] + "<_!_>")
    my_new_file = open("/corpus_new_file.txt", "w")
    for line in updated_corpus:
        my_new_file.write(line + "\n")
    my_new_file.close()
    print("FINISHED")


loadMyFile("/home/ivanetc/PycharmProjects/Readability/GenreCorpus/corpus_file.txt", "/data_copy.csv")
