# coding: utf-8
"""
Country related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle
from dsl import IsCountry, IncumbentOf, CapitalOf, \
    LabelOf, LanguageOf, PopulationOf, PresidentOf, CurrencyOf
import pronouns

question_mark = Pos('.')


class Country(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsCountry() + HasKeyword(name)


class test(QuestionTemplate):
    """

    """
    regex = Token('hello')

    def interpret(self, match):
        print 'parsed'
        return


class PresidentOfQuestion(QuestionTemplate):
    """
    Regex for questions about the president of a country.
    Ex: "Who is the president of Argentina?"
    """
    default = Pos("WP") + Token("is") + Question(Pos("DT")) + \
              Lemma("president") + Pos("IN") + Country()
    president_country = Lemma('president') + Pos('IN') + Country()
    country_president = Country() + Lemma('president')
    regex = default | default + Question(Pos(".")) | president_country | \
            president_country + question_mark | country_president | country_president + question_mark

    def interpret(self, match):
        president = PresidentOf(match.country)
        incumbent = IncumbentOf(president)
        label = LabelOf(incumbent)
        pronouns.fetchHisFromAnswers = True
        return label, "enum"


class CapitalOfQuestion(QuestionTemplate):
    """
    TO DO
    Regex for questions about the capital of a country.
    Ex: "What is the capital of Bolivia?"
        "Capital of India?"
        "India capital?"
    """

    opening = Pos('WP') + Token("is")
    capital_country = Lemma('capital') + Pos('IN') + Country()
    country_capital = Country() + Lemma('capital')
    regex = opening + Pos("DT") + capital_country + question_mark | \
            opening + Pos("DT") + capital_country | capital_country | (capital_country + question_mark) | \
            country_capital | (country_capital + question_mark)

    def interpret(self, match):
        capital = CapitalOf(match.country)
        label = LabelOf(capital)
        pronouns.fetchItsFromAnswers = True
        return label, "enum"


# FIXME: the generated query needs FILTER isLiteral() to the head
# because dbpedia sometimes returns different things
class LanguageOfQuestion(QuestionTemplate):
    """
    Regex for questions about the language spoken in a country.
    Ex: "What is the language of Argentina?"
        "what language is spoken in Argentina?"
        "laguage of India?"
        "India Language?"
    """

    openings = (Lemma("what") + Token("is") + Pos("DT") +
                Question(Lemma("official")) + Lemma("language")) + Pos('IN') | \
               (Lemma("what") + Lemma("language") + Token("is") + \
                Lemma("speak")) + Pos('IN')
    country_language = Country() + Lemma('language')
    language_of_country = Lemma('language') + Pos('IN') + Country()
    regex = openings + Country() | openings + Country() + Question(Pos(".")) | \
            country_language | country_language + question_mark | language_of_country | \
            language_of_country + question_mark

    def interpret(self, match):
        language = LanguageOf(match.country)
        label = LabelOf(language)
        return label, "enum"


class PopulationOfQuestion(QuestionTemplate):
    """
    Regex for questions about the population of a country.
    Ex: "What is the population of China?"
        "How many people live in China?"
        TO DO
        "What is country population"
        "country population"
        "population country"
    """
    what_is = Pos('WP') + Token('is')
    openings =  Pos("DT") + Lemma("population") + Pos("IN") | \
               (Pos("WRB") + Lemma("many") + Lemma("people") + \
                Token("live") + Pos("IN")) | \
               (Token("population") + Pos("IN"))

    regex = what_is + openings + Country() | what_is + openings + Country() + question_mark | \
            Country() + Lemma('population') + question_mark | (Country() + Lemma('population'))
    # openings + Country() + Question(Pos("."))

    def interpret(self, match):
        population = PopulationOf(match.country)
        return population, "literal"


class CurrencyofQuestion(QuestionTemplate):
    """
    Regex for questions about currency of a country.
        Ex: "what is the currency of India?"
            "Currency of India?"
            "India Currency?"
    """

    what_is_opening = Pos('WP') + Token("is") + Question(Pos("DT"))
    currency_of_country = Lemma('currency') + Pos('IN') + Country()
    regex = what_is_opening + currency_of_country + question_mark| currency_of_country + question_mark | \
            what_is_opening + currency_of_country | currency_of_country

    def interpret(self, match):
        currency = CurrencyOf(match.country)
        label = LabelOf(currency)
        return label, "enum"


class PlaceOfCountry(QuestionTemplate):
    """
    TODO Place defination
    Regex for question like where is Place?
        Ex: "where is Agra?"
            "Agra Location?"
    """
    regex1 = Pos('WRB') + Token("is") + Pos('VBZ')
    country_s = Country() + Pos('POS') + Lemma('area')
    regex = regex1 | regex1 + Pos(".") | Pos('NNP') + Lemma('location') | \
            country_s | country_s + question_mark

    def interpret(self, match):
        print 'parsed PlaceOfCountry'
        return


class AreaofCountry(QuestionTemplate):
    """
    Regex for What is the Area of India?
    """
    regex1 = Pos('WP') + Token('is') + Pos('DT')
    regex2 = Lemma('area') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.')

    def interpret(self, match):
        print 'Parsed AreaOfCountry'
        return


class StateNames(QuestionTemplate):
    """
        CHECK this
       Regex for What are States of India?
    """
    regex1 = Pos('WP') + Pos('VBP')
    regex2 = Pos('NNS') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex2 | regex2 + Pos('.') | regex1 + regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed StateName'
        return


class RiversInCountry(QuestionTemplate):
    """
    regex for which River flows in India?
    """
    regex1 = Pos('WDT')
    regex2 = Lemma('river') + Plus(Pos('VBZ') | Pos('VBP')) + Pos('IN') + Country()
    regex = regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.') | regex1 + regex2

    def interpret(self, match):
        print 'parsed RiverInCountry'
        return


class WhatIsGDP(QuestionTemplate):
    """
    Regex for what is GDP of India?
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Lemma('GDP') + Pos('IN') + Country()
    regex = regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.') | regex1 + regex2

    def interpret(self, match):
        print 'parsed WhatIsGDP'
        return


class WhatIsTime(QuestionTemplate):
    """
    Regex for What is time in India?
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Lemma('time') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex2 | regex2 + Pos('.') | regex1 + regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed WhatIsTime'
        return


class NationalAnimal(QuestionTemplate):
    """
    Regex for What is National animal of India?
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Pos('NNP') + Lemma('animal') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed NationalAnimal'
        return


class NationalBird(QuestionTemplate):
    """
        Regex for What is National bird of India?
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Pos('NNP') + Lemma('bird') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed NationalBird'
        return


class NationalFruit(QuestionTemplate):
    """
        Regex for What is National fruit of India?
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Pos('NNP') + Lemma('fruit') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed NationalFruit'
        return


class NationalTree(QuestionTemplate):
    """
        Regex for What is National Tree of India?
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Pos('NNP') + Lemma('tree') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed NationalTree'
        return


class ListOfCities(QuestionTemplate):
    """
    Regex for List of cities in India?
    """
    regex1 = Pos('NN') + Pos('IN')
    regex2 = Lemma('city') + Pos('IN') + Country()
    regex = regex1 + regex2 | regex2 | regex2 + Pos('.') | regex1 + regex2 + Pos('.')

    def interpret(self, match):
        print 'parsed ListOfCities'
        return
