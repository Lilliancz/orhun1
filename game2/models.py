from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import inflect
import random
from django.conf import settings

author = 'Eli Pandolfo'

''' notes

'''
class Constants(BaseConstants):

    # can be changed to anything
    name_in_url = 'Game2'

    # Do not change
    players_per_group = 3
    num_rounds = 1

    # these are variable and can be set to anything by the person running the experiment.
    # 0 and 100 are the default values
    lower_bound = settings.SESSION_CONFIGS[0]['lower_bound']
    upper_bound = settings.SESSION_CONFIGS[0]['upper_bound']

    problems = []
    
    # create list of problems.
    # this is done serverside instead of clientside because everyone has the same problems, and
    # because converting numbers to words is easier in python than in JS.
    
    # JSON converts python tuples to JS lists, so this data structure is a list
    # of pairs, each holding a triple and its sum. 
    # [ ( ('two', 'fifteen', 'forty four'), 61 )... ]
    
    # numbers are randomly generated between lower_bound and upper_bound, both inclusive.
    # inflect is used to convert numbers to words easily
    n2w = inflect.engine()
    
    # assuming no one can do more than 500 problems in 2 minutes 
    for n in range(500):
        v1 = random.randint(lower_bound, upper_bound)
        v2 = random.randint(lower_bound, upper_bound)
        v3 = random.randint(lower_bound, upper_bound)
        
        answer = v1 + v2 + v3
        
        s1 = n2w.number_to_words(v1).capitalize()
        s2 = n2w.number_to_words(v2)
        s3 = n2w.number_to_words(v3)

        words = (s1, s2, s3)
        entry = (words, answer)

        problems.append(entry)


class Subsession(BaseSubsession):
    
    def creating_session(self):

        self.group_randomly(fixed_id_in_group=True)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    # number of correct answers in baseline task
    game2_score = models.IntegerField()

    # player's rank out of 3
    game2_rank = models.IntegerField()

    # player's bonus for game 2
    game2_bonus = models.IntegerField()

    # number of problems attempted
    attempted = models.IntegerField()

    # firm chosen
    firm = models.StringField()

    # arrival times for pages
    time_Instructions2 = models.StringField()
    time_Game2 = models.StringField()
    time_Results2 = models.StringField()
    time_Results = models.StringField()
    time_Survey7 = models.StringField()
    time_Survey8 = models.StringField()
    time_Survey10 = models.StringField()
    time_Survey12 = models.StringField()

    q7_choice = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Yes', 'No'],
        label='You chose Firm A/B in the first contest. \
        If given the choice again would you still choose Firm A/B or would you change your choice?')

    q7 = models.LongStringField(label='Why?')
    q8 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Won', 'Came Second', 'Lost'],
        label='Do you think you won, came second, or lost the first contest?')
    q9 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Won', 'Came Second', 'Lost'],
        label='Do you think you won, came second, or lost the second contest?')
    q10 = models.PositiveIntegerField(label='Age')
    q11 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Man', 'Woman', 'Non-binary', 'Other'],
        label='Gender')
    q12 = models.LongStringField(label='Was there any part of the study that was confusing? Please help us improve our study by providing feedback.')










