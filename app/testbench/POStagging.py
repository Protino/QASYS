from nltk import pos_tag, word_tokenize
import json

if __name__ == "__main__":
    # qa.q2a(str(raw_input()))
    for __ in range(0, 10, 1):
        question = str(raw_input())

        if question == 'exit':
            break

        tagged_text = pos_tag(word_tokenize(question))
        print tagged_text

        pronouns = {}
        pronouns['its'] = ""
        pronouns['person'] = ""
        pronouns['fetchIts'] = False
        pronouns['fetchPerson'] = False

        json_data = json.dumps(pronouns)
        with open('pronouns.json', 'w') as outfile:
            json.dump(json_data, outfile)


