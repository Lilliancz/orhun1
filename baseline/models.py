# -*- coding: cp1252 -*-
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
    name_in_url = 'BaselineTask'
    pageTimeout = 120

    # Do not change
    players_per_group = None
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
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    # number of correct answers in baseline task
    baseline_score = models.IntegerField()

    baseline_bonus = models.CurrencyField()

    # number of problems attempted
    attempted = models.IntegerField()

    # arrival times
    time_Instructions = models.StringField()
    time_Baseline = models.StringField()
    time_ResultsBL = models.StringField()
    time_Survey1 = models.StringField()

    q1 = models.IntegerField()



"""
Baseline Score Task
Single player baseline performance collection
Arithmetic Task: Three word-number addition
e.g., twenty-five plus five plus thirteen
Everyone gets same sequence of questions
Complete as many of these arithmetic problems as possible within 2 minutes
Each page has one question, they submit each page and then get another page until timeout
Answer input box integer, forced response
Score is the number of correct answers within 2 minutes
Save “BaselineScore” as participant variable (fixed variable)
No payment for baseline task
See own score after finishing Baseline Task 
you attempted 18 questions and 12 were right, so your score is 12

Game 1 
Once 12 MTurkers have finished the baseline task, start Game 1
4 groups of 3 people
Player 1 in each group will see the following:
Would you like to choose Firm A (see opponent scores) or would you like to choose Firm B (do not see opponent scores)?
If Firm A, Player 1’s group type is A, and Player 2 and 3 are also of group type A
If Firm B, Player 1’s group type is B, and Player 2 and 3 are also of group type B
Players 2 and 3 will wait until Player 1 makes the choice then see: 
You have been assigned to Firm A/B

Each player sees or does not see baseline performance scores of others in group based on Person 1’s choice
Your score in the baseline task was: 
Opponent 1’s score was:
Opponent 2’s score was:

All players then play same task as in baseline
Work in task alone single player
Calculate the relative rank of each player but don’t display to the participants yet
Relative performance scale for each 3 person group - most correct gets $2 bonus, 2nd gets $1, last gets nothing in contest round

Game 2
Groups are re-formed. 
Player 1 is always assigned to the other group type in Game 2 (if they chose FirmA in Game 1, they will now play FirmB, and vice versa),
Players 2 and 3 are randomly mixed to be the players 2 and 3 of any of the 4 groups
Player 1 determines group type, player 2 and 3 always get whatever player 1 determined. 

Each player sees or does not see baseline performance scores of others in group based on group type
Your score in the baseline task was: 
Opponent 1’s score was:
Opponent 2’s score was:

All players then play same task as in baseline
Work in task alone single player
Calculate the relative rank of each player but don’t display to the participants yet
Relative performance scale for each 3 person group - most correct gets $2 bonus, 2nd gets $1, last gets nothing in contest round

END
In the baseline task, you attempted X out of X questions. Your baseline score was X. 
In Game 1, you attempted X out of X questions. Your score for Game 1 was X. 
In Game 2, you attempted X out of X questions. Your score for Game 2was X. 

In Game 1, you ranked X out of 3 players. Your bonus for Game 1 is $$
In Game 2, you ranked X out of 3 players. Your bonus for Game 2 is $$

Your total payment is $$

The top scoring player of each game will get a $2 bonus. The second highest score in each game will receive a $1 bonus. The third score (lowest) in each game will not receive a bonus.

"""
