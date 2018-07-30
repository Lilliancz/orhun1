from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import inflect
from django.conf import settings

# overall instructions & baseline instructions

class General(Page):
    timeout_seconds = 60


class Instructions(Page):
    form_model = 'player'
    form_fields = ['time_Instructions']
    timeout_seconds = 60

# baseline task
class Baseline(Page):
    form_model = 'player'
    form_fields = ['baseline_score', 'attempted', 'time_Baseline']

    # timer until page automatically submits itself
    timeout_seconds = settings.SESSION_CONFIGS[0]['time_limit']
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'problems': Constants.problems
        }

    # is called after the timer runs out and this page's forms are submitted
    # sets the participant.vars to transfer to next round
    def before_next_page(self):
        self.player.participant.vars['baseline_attempted'] = self.player.attempted
        self.player.participant.vars['baseline_score'] = self.player.baseline_score
        self.player.baseline_earnings = 0.05 * self.player.baseline_score
        self.participant.payoff = self.player.baseline_earnings
        self.player.participant.vars['baseline_earnings'] = self.player.baseline_earnings

# baseline results
class ResultsBL(Page):
    form_model = 'player'
    form_fields = ['time_ResultsBL']
    timeout_seconds = 60
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'attempted': self.player.attempted,
            'correct': self.player.baseline_score,
            'earnings': self.player.baseline_earnings,

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted)
        }

class Survey1(Page):
    form_model = 'player'
    form_fields = ['time_Survey1', 'q1']

class IntroPart2(Page):
    timeout_seconds = 1200

# sequence in which pages are displayed
page_sequence = [
    General,
    Instructions,
    Baseline,
    ResultsBL,
    Survey1,
    IntroPart2
]