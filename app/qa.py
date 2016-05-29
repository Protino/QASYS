#!/usr/bin/env python
# coding: utf-8
"""
Main script for DBpedia quepy.
"""

import sys
import time
import random
import datetime
import urllib2

import quepy
from SPARQLWrapper import SPARQLWrapper, JSON
from dbpedia import pronouns

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia = quepy.install("dbpedia")
output = ""


# quepy.set_loglevel("DEBUG")


def print_define(results, target, metadata=None):
    global output
    for result in results["results"]["bindings"]:
        if result[target]["xml:lang"] == "en":
            # print
            output += result[target]["value"] + "\n"


def print_enum(results, target, metadata=None):
    used_labels = []
    global output

    for result in results["results"]["bindings"]:
        if result[target]["type"] == u"literal":
            if result[target]["xml:lang"] == "en":
                label = result[target]["value"]
                if label not in used_labels:
                    used_labels.append(label)
                    output += label + "\n"  # print label


def print_literal(results, target, metadata=None):
    global output
    for result in results["results"]["bindings"]:
        literal = result[target]["value"]
        if metadata:
            output += metadata.format(literal) + "\n"
        else:
            output += literal + "\n"


def print_time(results, target, metadata=None):
    global output
    gmt = time.mktime(time.gmtime())
    gmt = datetime.datetime.fromtimestamp(gmt)

    for result in results["results"]["bindings"]:
        offset = result[target]["value"].replace(u"−", u"-")

        if ("to" in offset) or ("and" in offset):
            if "to" in offset:
                connector = "and"
                from_offset, to_offset = offset.split("to")
            else:
                connector = "or"
                from_offset, to_offset = offset.split("and")

            from_offset, to_offset = int(from_offset), int(to_offset)

            if from_offset > to_offset:
                from_offset, to_offset = to_offset, from_offset

            from_delta = datetime.timedelta(hours=from_offset)
            to_delta = datetime.timedelta(hours=to_offset)

            from_time = gmt + from_delta
            to_time = gmt + to_delta

            location_string = random.choice(["where you are",
                                             "your location"])

            output += "Between %s %s %s, depending on %s" % \
                      (from_time.strftime("%H:%M"),
                       connector,
                       to_time.strftime("%H:%M on %A"),
                       location_string)

        else:
            offset = int(offset)

            delta = datetime.timedelta(hours=offset)
            the_time = gmt + delta

            output += the_time.strftime("%H:%M on %A")


def print_age(results, target, metadata=None):
    global output
    assert len(results["results"]["bindings"]) == 1

    birth_date = results["results"]["bindings"][0][target]["value"]
    year, month, days = birth_date.split("-")

    birth_date = datetime.date(int(year), int(month), int(days))

    now = datetime.datetime.utcnow()
    now = now.date()

    age = now - birth_date
    output += "{} years old".format(age.days / 365)


def wikipedia2dbpedia(wikipedia_url):
    """
    Given a wikipedia URL returns the dbpedia resource
    of that page.
    """

    query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT * WHERE {
        ?url foaf:isPrimaryTopicOf <%s>.
    }
    """ % wikipedia_url

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        print "Snorql URL not found"
        sys.exit(1)
    else:
        return results["results"]["bindings"][0]["url"]["value"]


def q2a(question):
    global output
    output = ""
    """

    Given a nl question provide the answer
    if debug == true return the generated query too.
    """

    print_handlers = {
        "define": print_define,
        "enum": print_enum,
        "time": print_time,
        "literal": print_literal,
        "age": print_age,
    }
    print "-" * len(question)

    target, query, metadata = dbpedia.get_query(question)

    if isinstance(metadata, tuple):
        query_type = metadata[0]
        metadata = metadata[1]
    else:
        query_type = metadata
        metadata = None

    if query is None:
        return "Query could not be generated for that question:(\n", -1

    print "Query Generated"
    print query

    if target.startswith("?"):
        target = target[1:]
    if query:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        try:
            results = sparql.query().convert()
            if not results["results"]["bindings"]:
                return "No answer found in database:(", -1

            print "Results in JSON format"
            print results

            print_handlers[query_type](results, target, metadata)

            if pronouns.fetchHisFromAnswers:
                pronouns.his = pronouns.her = output
            if pronouns.fetchItsFromAnswers:
                print "YEAY"
                pronouns.its = output

            print pronouns.fetchItsFromAnswers
            print "Cleaned Answer"
            print output
            print "State of pronouns : "
            print "its : " + pronouns.its + "his" + pronouns.his

            # print results["results"]["bindings"][0]["x2"]["value"]
            # return print_handlers[query_type](results, target, metadata)
            return output, 1
        except urllib2.HTTPError, err:
            if err.code == 502:
                return "Cannot reach the database \n Looks like DBpedia SPARQL Endpoint is under maintenance. Please try again later. ", -1
        except:
            return "Network error", -1


if __name__ == "__main__":
    default_questions = [
        "What is a car?",
        "Who is Tom Cruise?",
        "Who is George Lucas?",
        "Who is Mirtha Legrand?",
        # "List Microsoft software",
        "Name Fiat cars",
        "time in argentina",
        "what time is it in Chile?",
        "List movies directed by Martin Scorsese",
        "How long is Pulp Fiction",
        "which movies did Mel Gibson starred?",
        "When was Gladiator released?",
        "who directed Pocahontas?",
        "actors of Fight Club",
    ]

    if "-d" in sys.argv:
        quepy.set_loglevel("DEBUG")
        sys.argv.remove("-d")

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])

        if question.count("wikipedia.org"):
            print wikipedia2dbpedia(sys.argv[1])
            sys.exit(0)
        else:
            questions = [question]
    else:
        questions = default_questions

    print_handlers = {
        "define": print_define,
        "enum": print_enum,
        "time": print_time,
        "literal": print_literal,
        "age": print_age,
    }

    for question in questions:
        print question
        print "-" * len(question)

        target, query, metadata = dbpedia.get_query(question)

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            print "Query not generated :(\n"
            continue

        print query

        if target.startswith("?"):
            target = target[1:]
        if query:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            if not results["results"]["bindings"]:
                print "No answer found :("
                continue

        print_handlers[query_type](results, target, metadata)
        print
