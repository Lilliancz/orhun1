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
    name_in_url = 'Game1'
    pageTimeout = 60
    first_place_bonus = 2.5
    second_place_bonus = 1
    gameDuration = "90 seconds"
    pageTimeoutWording = "1 minute"

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

# this controls if the offer to switch will be made.
# if choice = 1 then
        for p in self.get_players():
            #p.participant.vars['choice'] = (1 if random.random() >= 0.5 else 2)
            p.participant.vars['choice'] = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def getFirm(self):
        return self.participant.vars['firm']

    def role(self):
        if self.id_in_group == 1:
            return 'chooser'
        else:
            return 'notchooser'
    
    # number of correct answers in game1 task
    game1_score = models.IntegerField()

    # problems from game1 task
    game1_problems = models.StringField()

    # player's rank out of 3
    game1_rank = models.IntegerField()

    # player's bonus for game 1
    game1_bonus = models.CurrencyField()

    # combined bonus for game 1 and baseline
    total_bonus = models.CurrencyField()

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
    time_Game1Firm = models.StringField()
    time_Game1 = models.StringField()
    time_Results1 = models.StringField()
    time_Comprehension = models.StringField()
    time_Debrief = models.StringField()
    time_FinalSurvey = models.StringField()
    time_PerformancePayment = models.StringField()
    # time_Survey2 = models.StringField()
    # time_Survey45 = models.StringField()


    q2 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['2 others', '3 others', '4 others'],
        label='How many other players will you be evaluated against?')

    q3 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['True', 'False'],
        label='In Firm B, all players know each others\' scores before they compete.')

    q4 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Yes', 'No', 'I\'m not sure'],
        label = 'Will your opponents also make a choice between Firm A and Firm B?')

    # q5 = models.StringField(
    #     widget=widgets.RadioSelect,
    #     choices=['Firm A', 'Firm B'],
    #     label='Please wait while we randomly assign you to two other participants in either \
    #     Firm A or Firm B for the next round. If you could choose, which Firm would you prefer \
    #     to compete in? Your answer will not affect the assignment in any way.')

    q6 = models.StringField(label='Why did you choose this firm?')



    q7_choice = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Keep Firm', 'Change Firm'])
    q7 = models.LongStringField(label='Why?')
    q8 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Won', 'Came Second', 'Lost'],
        label='Do you think you won, came second, or lost the contest?')

    q10 = models.PositiveIntegerField(label='Age')
    q11 = models.StringField(
        widget=widgets.RadioSelect,
        choices=['Man', 'Woman', 'Non-binary', 'Other'],
        label='Gender')
    q12 = models.LongStringField(label='Was there any part of the study that was confusing? Please help us improve our study by providing feedback.',blank=True)

    debriefComments = models.LongStringField(label='Comments',blank=True)

    #Thanks to Philipp Chapkovski for the "Record time taken on waitpage" post
    Game1WaitPageSec = models.IntegerField()
    Game1FirmWaitPageSec = models.IntegerField()
    Game1ResultsWaitPageSec = models.IntegerField()

    def get_wait1(self):
        waiting_pages1 = ['Game1WaitPage']
        self.Game1WaitPageSec = sum(PageCompletion.objects.filter(participant=self.participant,
                                                          page_name__in=waiting_pages1).values_list(
            'seconds_on_page',
            flat=True))

    def get_wait1Firm(self):
        waiting_pages1Firm = ['Game1FirmWaitPage']
        self.Game1FirmWaitPageSec = sum(PageCompletion.objects.filter(participant=self.participant,
                                                          page_name__in=waiting_pages1Firm).values_list(
            'seconds_on_page',
            flat=True))

    def get_wait1Results(self):
        waiting_pages1Results = ['Results1WaitPage']
        self.Game1ResultsWaitPageSec = sum(PageCompletion.objects.filter(participant=self.participant,
                                                          page_name__in=waiting_pages1Results).values_list(
            'seconds_on_page',
            flat=True))
