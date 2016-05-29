from flask import Flask, render_template, request, redirect
import quepy
import sys
import qa
import re
from dbpedia import pronouns
from nltk import pos_tag, word_tokenize

app = Flask(__name__)
debug_question = ""
debug = False

cache = {}

@app.route('/')
def home():
    if debug:
        query()
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/query', methods=['POST'])
def query():
    if debug:
        question = debug_question
    else:
        question = request.form['question']
    # form validation remaining js or here itself



    if question == "":
        return redirect('/')

    print "Received question : " + question

    tagged_text = pos_tag(word_tokenize(question))

    print "POS Tagged question"
    print tagged_text

    # FIXME add more rules to resolve anaphora
    # TO-DO * resolve its, their and him
    #       * also fetch pronouns from answers!
    nn = [word for word, pos in tagged_text if pos == 'NN']
    nnp = [word for word, pos in tagged_text if pos == 'NNP']
    prp = [word for word, pos in tagged_text if pos == 'PRP$' or pos == 'PRP']

    if prp:
        if pronouns.his:
            question = re.sub(r'\bhe\b', pronouns.his, question)
        else:
            print "Who does that person refer to?"

    # search within cache first
    if question in cache.keys():
        answer = cache[question]
    else:
        # send the question to qa module and retrieve answer back.
        answer = qa.q2a(question)

    # cache the results
    cache[question] = answer
    if not debug:
        return render_template('home.html', answer=answer)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug = True
        debug_question = str(raw_input())
        query()
    else:
        app.run(debug=True)
