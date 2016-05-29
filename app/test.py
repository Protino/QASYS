import qa
from dbpedia import pronouns
from nltk import pos_tag, word_tokenize

if __name__ == "__main__":
    # qa.q2a(str(raw_input()))
    for __ in range(0, 10, 1):
        question = str(raw_input())

        tagged_text = pos_tag(word_tokenize(question))
        print tagged_text
        nn = [word for word, pos in tagged_text if pos == 'NN']
        nnp = [word for word, pos in tagged_text if pos == 'NNP']
        prp = [word for word, pos in tagged_text if pos == 'PRP$' or pos == 'PRP']

        if prp:
            question.replace("his", pronouns.his)
            question.replace("her", pronouns.her)
            question = question.replace("he", pronouns.his)
            question.replace("she", pronouns.her)

        try:
            qa.q2a(question)
        except:
            print ""


