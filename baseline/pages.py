from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import inflect
from django.conf import settings
from otree_mturk_utils.pages import CustomMturkPage, CustomMturkWaitPage


# overall instructions & baseline instructions
class General(Page):

    def vars_for_template(self):
        self.player.baseline_answers = ', '.join(str(x) for x in self.session.vars['baseline_answers'])
        return {
            'problems': self.session.vars['baseline_problems'],
            'answers': self.session.vars['baseline_answers'],
            'pageTimeoutWord': self.session.config.get('pageTimeoutWord')
        }


class Instructions(Page):
    form_model = 'player'
    form_fields = ['time_Instructions']

    def vars_for_template(self):
        return {
            'gameDuration': self.session.config.get('gameDuration')
        }


# baseline task
class Baseline(Page):
    form_model = 'player'
    form_fields = ['baseline_score', 'attempted', 'time_Baseline']
    timeout_seconds = settings.SESSION_CONFIGS[0]['time_limit']

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'problems': self.session.vars['baseline_problems'],
            'answers': self.session.vars['baseline_answers']
        }

    # is called after the timer runs out and this page's forms are submitted
    # sets the participant.vars to transfer to next round
    def before_next_page(self):
        self.player.participant.vars['baseline_attempted'] = self.player.attempted
        self.player.participant.vars['baseline_score'] = self.player.baseline_score
        self.player.baseline_bonus = 0.05 * self.player.baseline_score
        self.player.participant.vars['baseline_bonus'] = self.player.baseline_bonus
        self.player.payoff = self.player.baseline_bonus
        print(self.player.payoff)
        if self.timeout_happened:
            self.player.TimeoutBaseline = 1


# baseline results
class ResultsBL(Page):

    form_model = 'player'
    form_fields = ['time_ResultsBL']

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'baseline_bonus': self.participant.payoff,
            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted),
            'gameDuration': self.session.config.get('gameDuration')
        }


class Survey1(Page):
    form_model = 'player'
    form_fields = ['time_Survey1', 'q1']


class IntroPart2(Page):

    def vars_for_template(self):
        return {
            'gameDuration': self.session.config.get('gameDuration')
        }


# sequence in which pages are displayed
page_sequence = [
    General,
    Instructions,
    Baseline,
    ResultsBL,
    Survey1,
    IntroPart2
]