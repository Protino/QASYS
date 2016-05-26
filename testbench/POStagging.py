from nltk import pos_tag, word_tokenize

if __name__ == "__main__":
    # qa.q2a(str(raw_input()))
    for __ in range(0, 10, 1):
        question = str(raw_input())

        tagged_text = pos_tag(word_tokenize(question))
        print tagged_text
