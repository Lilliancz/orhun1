from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random as r


class PlayerBot(Bot):

    def play_round(self):
        score = r.randint(0,5)
        att = score + r.randint(0,5)
        yield (pages.Instructions2, {'time_Instructions2': 'test'})
        yield Submission(pages.Game2, 
            {'time_Game2': 'test', 'game2_score': score, 'attempted': att},
            check_html=False)
        yield (pages.Results2, {'time_Results2': 'test'})
        yield (pages.Results, {'time_Results': 'test'})
