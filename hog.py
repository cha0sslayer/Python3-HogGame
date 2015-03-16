"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
#    Declare our counter and start it at the number of roles
    i = num_rolls
#    Declare our total variable and set it equal to zero to start
#    Declare our is_pigout variable and set it equal to False to start
    is_pigout = False
    total = 0
    while i > 0:
#        Call our dice function
        roll = dice()
#        Add our value to the current running total of all the rolls
        total += roll
#        Set a flag if a one is rolled
        if roll == 1:
            is_pigout = True
#        Decrease the counter by one after each run
        i = i - 1
#    Check if a 1 was rolled, if so return 1 (pigout)
    if is_pigout:
        return 1
#    Good news for the player, a one wasn't rolled. Return the total of all the dice rolls
    else:
        return total



def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
#    Implement the free bacon rule (check to see if there are 0 rolls)
    if num_rolls == 0:
        if len(str(opponent_score)) == 1:
            return opponent_score + 1
        else:
            return abs(int(str(opponent_score)[:1]) - int(str(opponent_score)[-1])) + 1
    score = roll_dice(num_rolls, dice)
    return score


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided

def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"

    # The buggy code is below:
    if bid0 == bid1:
        return goal, goal, 0
    if bid0 == bid1 - 5:
        return 0, 0, 0
    if bid1 == bid0 + 5:
        return 10, 0, 1
    if bid1 > bid0:
        return bid1, bid0, 0
    else:
        return bid0, bid1, 1

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    while score0 < goal and score1 < goal:
#        Which player is playing?
        if who == 0:
#            Select our dice
            dice = select_dice(score0, score1)
#            How may roles is this player making?
            num_roles = strategy0(score0, score1)
#            Finally we can calculate the score
            score0 += take_turn(num_roles, score1, dice)
#            Wahoo let's make sure it is the next player's turn now
            who = 1
#            Check to see if the score is greater than or equal to the goal score
            if score0 >= goal:
#                Wahoo we have a winner. Let's return the scores.
                return score0, score1
        if who == 1:
            dice = select_dice(score1, score0)
            num_roles = strategy1(score1, score0)
            score1 += take_turn(num_roles, score0, dice)
            who = 0
#        Implement the swine swap role
        if 2 * score0 == score1 or 2 * score1 == score0:
#            Grr we need to swap scores
            s0 = score0
            score0 = score1
            score1 = s0
    return score0, score1

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=50000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"

    def myfunction(*args):
        i, total = 0, 0
        while i < num_samples:
            total += fn(*args)
            i += 1
        average = total / i
        return average
    return myfunction


def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
#    Start with one roll
    num_rolls = 1
#    Declare our max average variable
    max_average = 0
#    Implement our loop
    while num_rolls <= 10:
#        Call the make averaged function (which subsequently calls roll_dice(num_rolls, dice) multiple times and calculates the average
        average = make_averaged(roll_dice)(num_rolls, dice)
#        Check to see if we have a newer high
        if average > max_average:
            max_average, nm = average, num_rolls
#        Increment our counter
        num_rolls += 1
    return nm



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
#    Set our demo score to 0 to start
    demo_score = 0
#    Start our loop. Don't get dizzy readers. It helps to try to stare at one spot

    if len(str(opponent_score)) == 1:
        bacon_score = opponent_score + 1
    else:
        bacon_score = abs(int(str(opponent_score)[:1]) - int(str(opponent_score)[-1])) + 1
    demo_score += bacon_score
    if demo_score >= margin:
        return 0
    else:
        return num_rolls



def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
#    Calculate the opponent_score if a zero is rolled
    if len(str(opponent_score)) == 1:
        bacon_score = opponent_score + 1
    else:
        bacon_score = abs(int(str(opponent_score)[:1]) - int(str(opponent_score)[-1])) + 1
    bacon_score, original_bacon_score = score + bacon_score, bacon_score

    if (bacon_score == opponent_score * 2) or (opponent_score == bacon_score * 2):
        if opponent_score > bacon_score:
#            roll 0
            return 0
        else:
            return num_rolls

    elif original_bacon_score >= margin:
        return 0
    else:
        return num_rolls




def final_strategy(score, opponent_score):
    """
    The strategy uses four functions which are described below
        
        function is_winning()
            Returns True if the current player is ahead in score, else returns false
        function get_bacon_score
            Returns the would be bacon score should the player role 0
        function force_four_sided_dice()
            Returns true if utilizing the free bacon rule would allow the player to force 4 sided dice for the opponent
        function get_strategic_num_rolls()
            Returns an optimal number of rolls to use depending on the current score situation
        function win_with_free_bacon()
            Returns true if utilizing free bacon would allow the player to win the game in that roll

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
#    Are we winning?
    def is_winning(score=score, opponent_score=opponent_score):
        if score > opponent_score:
            return True
        return False
#    Calculate our would be bacon score
    def get_bacon_score(score=score, opponent_score=opponent_score, raw=False):
        if len(str(opponent_score)) == 1:
            bacon_score = opponent_score + 1
        else:
            bacon_score = abs(int(str(opponent_score)[:1]) - int(str(opponent_score)[-1])) + 1
        if raw:
            return bacon_score
        bacon_score = score + bacon_score
        return bacon_score
    
#    Create a function that checks to see if we can force 4 sided dice
    def force_four_sided_dice(score=score, opponent_score=opponent_score):
#        Get our bacon score
        bacon_score = get_bacon_score()
        if (bacon_score + opponent_score) % 7 == 0:
#            Great, this was successful. Return true
            return True
#        Darn no luck. Return false
        return False
#    Depending on the number score position determine what number of dice to roll
    def get_strategic_num_rolls(score=score, opponent_score=opponent_score):
        range = abs(score - opponent_score)
        if is_winning():
            if range < 10 and not range >= 20:
                return 5
            if range < 30 and not range >= 40:
                return 4
            if range < 50 and not range >= 60:
                return 3
#            This would be a great time to try to force 4 sided dice since we have such a large lead
            if force_four_sided_dice:
                return 0
            return 3
        if not is_winning():
            if range < 5 and not range >= 10:
                return 5
            if range < 10 and not range >= 20:
                return 6
            if range < 30 and not range >= 40:
                return 7
            return 7
#    Create a function that checks to see if a free bacon roll would allow us to win
    def win_with_free_bacon(score=score, opponent_score=opponent_score):
        bacon_score = get_bacon_score(score, opponent_score, True)
        if not force_four_sided_dice() and bacon_score >= 100 - score:
            return True
        return False

    if not swap_strategy(score, opponent_score) or win_with_free_bacon():
        return 0
    else:
        return get_strategic_num_rolls()


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
