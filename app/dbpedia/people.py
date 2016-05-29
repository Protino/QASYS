# coding: utf-8

"""
People related regex

 TO-DO
  What is the birthdate of ___?
  Tell me about Tom Cruise

"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, Token, QuestionTemplate, Particle
from dsl import IsPerson, LabelOf, DefinitionOf, BirthDateOf, BirthPlaceOf
import pronouns

question_mark = Question(Pos("."))


class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS") | Pos("JJ"))

    def interpret(self, match):
        name = match.words.tokens
        pronouns.his = name
        pronouns.her = name
        return IsPerson() + HasKeyword(name)


class WhoIs(QuestionTemplate):
    """
    Ex: "Who is Tom Cruise?"
    """

    regex = Lemma("who") + Lemma("be") + Person() + \
            Question(Pos("."))

    def interpret(self, match):
        definition = DefinitionOf(match.person)
        return definition, "define"


class HowOldIsQuestion(QuestionTemplate):
    """
    Ex: "How old is Bob Dylan".
        "What is his/her age?"
        "person age"
        "age of person"
    """

    regex = (Pos("WRB") + Lemma("old") + Lemma("be") + Person() + \
             Question(Pos("."))) | (Pos("What") + Lemma("be") + Pos("PPR$") + Lemma("age") + Question(Pos(".")))

    def interpret(self, match):
        birth_date = BirthDateOf(match.person)
        return birth_date, "age"


class WhereIsFromQuestion(QuestionTemplate):
    """
    Ex: "Where is Bill Gates from?"
    Ex: birthplace of person
    person birthplace
    """

    wherebe = Lemmas('where be')

    regex1 = wherebe + Person() + Lemma("from") + question_mark
    regex2 = Person() + Lemma('birthplace') + question_mark
    regex3 = Lemma('birthplace') + Pos('IN') + Person() + question_mark

    regex = regex1 | regex2 | regex3

    def interpret(self, match):
        birth_place = BirthPlaceOf(match.person)
        label = LabelOf(birth_place)
        return label, "enum"


class BirthDate(QuestionTemplate):
    """
    Regex for what is the birthDate of Person?
    Ex :
    when was person born
    birthdate of Person
    person birthdate
    person birthday
    """
    regex1 = Pos('WP') + Pos('VBZ') + Pos('DT')
    regex2 = Lemma('birthDate') + Pos('IN') + Person()
    regex = regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.') | regex1 + regex2

    def interpret(self, match):
        print 'parsed BirthDate'
        return


class PersonSpouse(QuestionTemplate):
    """
    Regex for who is spouse of Narendra Modi?
    Ex :
    Narendra Modi spouse - regex3
    wife of Narendra Modi
    """
    regex1 = Pos('WP') + Token('is')
    regex2 = Lemma('spouse') + Pos('IN') + Person()
    regex = regex1 + regex2 + Pos('.') | regex2 | regex2 + Pos('.') | regex1 + regex2

    def interpret(self, match):
        print 'parsed PersonSpous'
        return


        # class BirthPlacce(QuestionTemplate):
        # """
        # Regex for birthplace of Person?
        # Ex: birthplace of Narendra Modi
        # What is the birthplace of Narendra Modi?
        # Where was Narendra Modi born?

        # """
        # where_be = Pos('WP') + Lemma('be')
        # what_is = Pos()
