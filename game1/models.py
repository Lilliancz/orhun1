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
    name_in_url = 'Game1'

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
        self.group_randomly()

        for p in self.get_players():
            p.participant.vars['choice'] = (1 if random.random() >= 0.5 else 2)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    # number of correct answers in baseline task
    game1_score = models.IntegerField()

    # player's rank out of 3
    game1_rank = models.IntegerField()

    # player's bonus for game 1
    game1_bonus = models.IntegerField()

    # number of problems attempted
    attempted = models.IntegerField()

    # firm chosen
    firm = models.StringField(
        # choices=['A', 'B'],
        # widget=widgets.RadioSelect
    )

    # whether the switch was made
    # Yes, No, N/A (not offered)
    switch = models.StringField()

    # these will be offered to 1/6 of all players, for others the fields will be left blank
    c5 =  models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c10 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c15 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c20 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c25 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c30 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c35 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c40 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c45 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    c50 = models.StringField(widget=widgets.RadioSelectHorizontal, choices=["Yes", "No"])
    
    # arrival times
    time_ChooseFirm = models.StringField()
    time_Instructions1 = models.StringField()
    time_Game1 = models.StringField()
    time_Results1 = models.StringField()
    # time_Survey2 = models.StringField()
    # time_Survey45 = models.StringField()


    # q2 = models.StringField(
    #     widget=widgets.RadioSelect,
    #     choices=['2 others', '3 others', '4 others'],
    #     label='How many other players will you be evaluated against?')

    # q3 = models.StringField(
    #     widget=widgets.RadioSelect,
    #     choices=['True', 'False'],
    #     label='In Firm B, all players\' know each others\' scores before they compete.')
    
    # q4 = models.StringField(
    #     widget=widgets.RadioSelect,
    #     choices=['Yes', 'No', 'I\'m not sure'],
    #     label='How many other players will you be evaluated against?')

    # q5 = models.StringField(
    #     widget=widgets.RadioSelect,
    #     choices=['Firm A', 'Firm B'],
    #     label='Please wait while we randomly assign you to two other participants in either \
    #     Firm A or Firm B for the next round. If you could choose, which Firm would you prefer \
    #     to compete in? Your answer will not affect the assignment in any way.')

    q6 = models.StringField(label='Why did you choose this firm?')

