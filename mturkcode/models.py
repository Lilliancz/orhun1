from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import inflect
import random
from django.conf import settings
from otree.models_concrete import PageCompletion

author = 'Eli Pandolfo, modified by Xiaotian Lu and Lillian Chen'

''' notes

'''
class Constants(BaseConstants):

    # can be changed to anything
    name_in_url = 'mturkcode'

    # Do not change
    players_per_group = 1
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass
