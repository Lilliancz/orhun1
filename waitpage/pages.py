from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.conf import settings

# the first 12 players that arrive at this page will be grouped together, then a toggle will be
# flipped that prevents others from continuing

class FirstWaitPage(WaitPage):
    group_by_arrival_time = True
    body_text = ('When ' + str(settings.SESSION_CONFIGS[0]['min_players'])
        + ' players finish the baseline task, you will continue.')

page_sequence = [
    FirstWaitPage,
]
