from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import inflect
from django.conf import settings

# wait page before game 1
class Game2WaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)
        p1.firm = 'B' if p1.participant.vars['firm'] == 'A' else 'A'
        p2.firm = p1.firm
        p3.firm = p1.firm

# instructions for game 2
class Instructions2(Page):
    form_model = 'player'
    form_fields = ['time_Instructions2']
    timeout_seconds = 60
    
    def vars_for_template(self):
        you = self.player.id_in_group
        opponent1 = self.group.get_player_by_id((you) % 3 + 1)
        opponent2 = self.group.get_player_by_id((you + 1) % 3 + 1)

        return {
            'firm': self.player.firm,
            'baseline': self.player.participant.vars['baseline_score'],
            'opponent1': opponent1.participant.vars['baseline_score'],
            'opponent2': opponent2.participant.vars['baseline_score']
        }

# game 1 task
class Game2(Page):
    form_model = 'player'
    form_fields = ['game2_score', 'attempted', 'time_Game2']

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
        self.player.participant.vars['game2_score'] = self.player.game2_score

class Results2WaitPage(WaitPage):
    
    def after_all_players_arrive(self):

        # in case 2 players have a tied score, chance decides how bonuses are distributed
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)

        # sorted() is guaranteed to be stable, so the list is shuffled first to ensure randomness
        players = sorted(random.sample([p1, p2, p3], k=3), key=lambda x: x.game2_score, reverse=True)

        for i in range(3):
            if players[i].game2_score == 0:
                players[i].game2_rank = 3
                players[i].game2_bonus = 0
            else:
                players[i].game2_rank = i + 1
                players[i].game2_bonus = 2 - i
                if i == 0:
                    players[i].participant.payoff += 2.5
                else:
                    players[i].payoff = c(2 - i)


# game 2 results
class Results2(Page):
    form_model = 'player'
    form_fields = ['time_Results2']
    timeout_seconds = 60
    
    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        return {
            'attempted': self.player.attempted,
            'correct': self.player.game2_score,

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted)
        }

# overall results
class Results(Page):
    form_model = 'player'
    form_fields = ['time_Results']
    timeout_seconds = 60

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        bl_attempted = self.player.participant.vars['baseline_attempted']
        bl_score = self.player.participant.vars['baseline_score']
        bl_problems = inflect.engine().plural('problem', bl_attempted)

        g1_attempted = self.player.participant.vars['game1_attempted']
        g1_score = self.player.participant.vars['game1_score']
        g1_problems = inflect.engine().plural('problem', g1_attempted)
        g1_rank = self.player.participant.vars['game1_rank']
        g1_bonus = self.player.participant.vars['game1_bonus']

        g2_attempted = self.player.attempted
        g2_score = self.player.game2_score
        g2_problems = inflect.engine().plural('problem', g2_attempted)
        g2_rank = self.player.game2_rank
        g2_bonus = self.player.game2_bonus

        # should there be a uniform participation fee on top of this?
        # doing it this way bc mturk pays participants the participation_fee defined in settings
        # settings.SESSION_CONFIGS[0]['participation_fee'] = g1_bonus + g2_bonus

        return {
            'bl_attempted': bl_attempted,
            'bl_score': bl_score,
            'bl_problems': bl_problems,
            'g1_attempted': g1_attempted,
            'g1_score': g1_score,
            'g1_problems': g1_problems,
            'g1_rank': g1_rank,
            'g1_bonus': g1_bonus,
            'g2_attempted': g2_attempted,
            'g2_score': g2_score,
            'g2_problems': g2_problems,
            'g2_rank': g2_rank,
            'g2_bonus': g2_bonus,
            'total_bonus': self.participant.payoff
        }

class Survey7(Page):
    form_model = 'player'
    form_fields = ['time_Survey7', 'q7_choice', 'q7']

    def is_displayed(self):
        return self.player.participant.vars['choice'] == 1 and self.player.id_in_group == 1

class Survey8(Page):
    form_model = 'player'
    form_fields = ['time_Survey8', 'q8', 'q9']

class Survey10(Page):
    form_model = 'player'
    form_fields = ['time_Survey10', 'q10', 'q11']

class Survey12(Page):
    form_model = 'player'
    form_fields = ['time_Survey12', 'q12']


page_sequence = [
    Game2WaitPage,
    Instructions2,
    Game2,
    Results2WaitPage,
    Results2,
    Survey7,
    Survey8,
    Survey10,
    Survey12,
    Results
]
