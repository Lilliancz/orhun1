from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import inflect
from django.conf import settings

# wait page before game 1
class Game1WaitPage(WaitPage):
    group_by_arrival_time = True
    
    def after_all_players_arrive(self):
        pass

class WhatHappensNextA(Page):
    form_model = 'player'
    timeout_seconds = Constants.pageTimeout
	
    def is_displayed(self):
        return self.player.id_in_group == 1

class WhatHappensNextB(Page):
    form_model = 'player'
    timeout_seconds = Constants.pageTimeout

    def is_displayed(self):
        return self.player.role() == 'notchooser'


#Comprehension Questions for everyone
class Comprehension(Page):
     form_model = 'player'
     timeout_seconds = Constants.pageTimeout

     def is_displayed(self):
         self.player.game1_problems=Constants.problems
         self.player.get_wait1()
         return True

     def get_form_fields(self):
         #Show questions based on role
        if self.player.id_in_group == 1:
            return ['q2', 'q3', 'q4']
        else:
            return ['q2', 'q3']

class CompResults(Page):
    timeout_seconds = Constants.pageTimeout


# one player in each group chooses firm A or firm B
class ChooseFirm(Page):
    form_model = 'player'

    timeout_seconds = Constants.pageTimeout
    timeout_submission = {'firm': 'B'}

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'choice': self.player.participant.vars['choice'],
            'rval': random.randrange(5, 55, 5),
        }

    def get_form_fields(self):
        if self.player.participant.vars['choice'] == 2:
            return ['firm', 'time_ChooseFirm', 'c5', 'c10', 'c15', 'c20', 'c25', 'c30', 'c35', 'c40', 'c45', 'c50', 'switch']
        else:
            return ['firm', 'time_ChooseFirm']

    def before_next_page(self):
        for p in self.group.get_players():
            p.participant.vars['firm'] = self.player.firm
            p.firm = self.player.firm


# Ask why player 1 chose Firm
class WhyFirm(Page):
    form_model = 'player'
    timeout_seconds = Constants.pageTimeout

    def is_displayed(self):
        return self.player.id_in_group == 1

    def get_form_fields(self):
        if self.player.id_in_group == 1:
            return ['q6']
        else:
            return []

    def vars_for_template(self):
        return {
            'firm': self.player.participant.vars['firm']
        }

# wait page for all 3 group members
class Game1FirmWaitPage(WaitPage):
    body_text = "Please wait while other participants are finishing up. You will begin the competition \
    when all three participants have arrived to this page. Please do not leave, the wait should not be long. \
    If you are inactive for a while (not on a wait page), you will be kicked out of the study and not get any bonus."



# Show firm for game 1
class Game1Firm(Page):
    form_model = 'player'
    form_fields = ['time_Game1Firm']
    timeout_seconds = Constants.pageTimeout

    def is_displayed(self):
        self.player.get_wait1Firm()
        return True

    def vars_for_template(self):
        you = self.player.id_in_group
        opponent1 = self.group.get_player_by_id((you) % 3 + 1)
        opponent2 = self.group.get_player_by_id((you + 1) % 3 + 1)

        return {
            'firm': self.player.participant.vars['firm'],
            'baseline': self.player.participant.vars['baseline_score'],
            'opponent1': opponent1.participant.vars['baseline_score'],
            'opponent2': opponent2.participant.vars['baseline_score']
        }

# game 1 task
class Game1(Page):
    form_model = 'player'
    form_fields = ['game1_score', 'attempted', 'time_Game1']

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
        self.player.participant.vars['game1_attempted'] = self.player.attempted
        self.player.participant.vars['game1_score'] = self.player.game1_score

class Results1WaitPage(WaitPage):
    
    def after_all_players_arrive(self):

        # in case 2 players have a tied score, chance decides how bonuses are distributed
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)

        # sorted() is guaranteed to be stable, so the list is shuffled first to ensure randomness
        players = sorted(random.sample([p1, p2, p3], k=3), key=lambda x: x.game1_score, reverse = True)

        for i in range(3):
            #if score is zero, auto rank 3rd, no bonus
            if players[i].game1_score == 0:
                players[i].game1_rank = 3
                players[i].participant.vars['game1_rank'] = 3
                players[i].game1_bonus = 0
                players[i].participant.vars['game1_bonus'] = 0
            #if not score of zero, then rank in order of highest score in game 1
            else:
                players[i].game1_rank = i + 1
                players[i].participant.vars['game1_rank'] = i + 1
                #need to change bonus structure here
                if players[i].game1_rank == 1:
                    players[i].game1_bonus = Constants.first_place_bonus
                    players[i].participant.vars['game1_bonus'] = Constants.first_place_bonus
                    players[i].participant.payoff += Constants.first_place_bonus
                if players[i].game1_rank == 2:
                    players[i].game1_bonus = Constants.second_place_bonus
                    players[i].participant.vars['game1_bonus'] = Constants.second_place_bonus
                    players[i].participant.payoff += Constants.second_place_bonus
                if players[i].game1_rank == 3:
                    players[i].game1_bonus = 0
                    players[i].participant.vars['game1_bonus'] = 0

# game 1 results
class Results1(Page):
    form_model = 'player'
    form_fields = ['time_Results1']
    timeout_seconds = Constants.pageTimeout

    def is_displayed(self):
        self.player.get_wait1Results()
        return True

    # variables that will be passed to the html and can be referenced from html or js
    def vars_for_template(self):
        self.player.participant.vars['total_bonus'] = self.player.participant.vars['baseline_bonus'] + self.player.participant.vars['game1_bonus']
        self.player.total_bonus = self.player.participant.vars['total_bonus']
        return {
            'attempted': self.player.attempted,
            'correct': self.player.game1_score,
            'baseline_attempted': self.player.participant.vars['baseline_attempted'],
            'baseline_score': self.player.participant.vars['baseline_score'],
            'baseline_bonus': self.player.participant.vars['baseline_bonus'],
            'total_bonus': self.player.participant.vars['total_bonus'],

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted)
        }

class FinalSurvey(Page):
    form_model = 'player'
    form_fields =['time_FinalSurvey', 'q8', 'q10','q11','q12']
    timeout_seconds = Constants.pageTimeout

class FinalSurveyA(Page):
    form_model = 'player'
    form_fields =['q7_choice', 'q7']
    timeout_seconds = Constants.pageTimeout
    def is_displayed(self):
        return self.player.id_in_group == 1
    def vars_for_template(self):
        firm = self.player.participant.vars['firm']
        return {
            'changefirm_label': 'You chose Firm '+firm+' in the contest. \
        If given the choice again, would you still choose Firm '+firm+' or would you change your choice?'
        }

class PerformancePayment(Page):
    form_model = 'player'
    form_fields = ['time_PerformancePayment']
    timeout_seconds = Constants.pageTimeout
    def vars_for_template(self):
        return {
            'attempted': self.player.attempted,
            'correct': self.player.game1_score,
            'baseline_bonus': c(self.player.participant.vars['baseline_bonus']),
            'total_bonus': c(self.player.participant.vars['total_bonus']),

            # automoatically pluralizes the word 'problem' if necessary
            'problems': inflect.engine().plural('problem', self.player.attempted)
        }

class Debrief(Page):
    form_model = 'player'
    form_fields = ['debriefComments','time_Debrief']
    timeout_seconds = Constants.pageTimeout

class copyMturkCode(Page):
    pass




page_sequence = [
    Game1WaitPage,
	WhatHappensNextA,
	WhatHappensNextB,
    Comprehension,
    CompResults,
    ChooseFirm,
    WhyFirm,
    Game1FirmWaitPage,
    Game1Firm,
    Game1,
    Results1WaitPage,
    Results1,
    FinalSurvey,
    FinalSurveyA,
    PerformancePayment,
    Debrief,
    copyMturkCode

]
