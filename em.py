from math import log
from pprint import pprint
import random

from casino import Casino
from utils import Dice

EPS = 10 ** -10
MAX_IT = 100

def possible_range(observation):
    """Returns the minimum and the maximum possible result of one dice given
    that the sum is equal to observation"""

    return max(1,observation-6),min(6,observation-1)+1


def initialize_parameters(n_players, n_tables):
    """Returns intial parameters all set to uniform distributions"""
    fair_dice = [1/6.0 for i in range(1,7)]

    tables = [fair_dice for i in range(n_tables)]
    players = [fair_dice for i in range(n_players)]

    return {'table' : tables, 'player' : players}


def joint_probability(table, table_dice,
                      player, player_dice, parameters):
    """Returns the joint probability of table=table returning table_dice and
    player=player giving player_dice"""

    return parameters['table'][table][table_dice-1] *\
        parameters['player'][player][player_dice-1]


def responsability(player, player_dice, table, table_dice,
                   observed_sum, parameters):
    """Returns the responsability variable for the given input. Defined as:
    player_dice -> Ni
    player_result -> g

    table_dice -> Xk
    table_result -> t

    observed_sum -> sik

    P(Ni=g, Xk=t | sik, parameters)
    """

    if player_dice + table_dice != observed_sum:
        return 0

    joint_prob = joint_probability(table, table_dice,
                                   player, player_dice, parameters)

    observed_sum_prob = 0
    for player_d in range(*possible_range(observed_sum)):
        table_d = observed_sum - player_d
        observed_sum_prob += joint_probability(table, table_d,
                                               player, player_d, parameters)

    return joint_prob / observed_sum_prob

def expected_complete_loglikelihood(observations, parameters):
    """Returns the expected complete log likelihood of the observations given
    the parameters.

    l(parameters; D)
    """

    log_likelihood = 0
    for player,player_results in enumerate(observations):
        for table,observed_sum in enumerate(player_results):
            #marginalize on the hidden
            likelihood = 0
            for player_dice in range(*possible_range(observed_sum)):
                table_dice = observed_sum - player_dice
                likelihood += joint_probability(table, table_dice,
                                               player, player_dice, parameters)

            log_likelihood += log(likelihood)

    return log_likelihood

def expected_complete_loglikelihood_v2(observations, parameters):
    """Returns the expected complete log likelihood of the observations given
    the parameters.

    l(parameters; D)
    """

    log_likelihood = 0
    for player,player_results in enumerate(observations):
        for table,observed_sum in enumerate(player_results):
            #compute q term
            q_term = 0
            for player_dice in range(*possible_range(observed_sum)):
                table_dice = observed_sum - player_dice

                r = responsability(player, player_dice, table, table_dice,
                                   observed_sum, parameters)
                if r < EPS:
                    continue

                joint = log(joint_probability(table, table_dice,
                                              player, player_dice, parameters))


                q_term += r*joint

            #compute r term
            r_term = 0
            for player_dice in range(*possible_range(observed_sum)):
                table_dice = observed_sum - player_dice
                r = responsability(player, player_dice, table, table_dice,
                                   observed_sum, parameters)

                if r>0:
                    r_term += r * log(r)

            log_likelihood += q_term - r_term

    return log_likelihood


def get_responsabilities(observations, parameters):
    """Compute the responsabilities variables for the observations given
    the parameters. The return value is a four dimensional list: the
    first index dimension refers to the players, the second to the tables,
    the third to the result of the player's dice, the fourth to the result
    of the table's dice"""

    return [[[[responsability(player, player_dice, table, table_dice,
                              observations[player][table], parameters)
               for table_dice in range(1,7)]
              for player_dice in range(1,7)]
             for table in range(len(observations[0]))]
            for player in range(len(observations))]

def normalize(dice):
    """Normalize a list to add up to 1"""

    normalized = [e/float(sum(dice)) for e in dice]
    return normalized


def optimize_player_dice(player,
                         players_number, tables_number, responsabilities):
    """Optimize the player dice using MLE for categorical distributions"""

    dice = []
    for player_dice in range(1,7):
        cumulated_r = sum(
            [responsabilities[player][table][player_dice-1][table_dice-1]
             for table in range(tables_number)
             for table_dice in range(1,7)])

        dice.append(cumulated_r)

    return normalize(dice)


def optimize_table_dice(table,
                        players_number, tables_number, responsabilities):
    """Optimize the player dice using MLE for categorical distributions"""

    dice = []
    for table_dice in range(1,7):
        cumulated_r = sum(
            [responsabilities[player][table][player_dice-1][table_dice-1]
             for player in range(players_number)
             for player_dice in range(1,7)])

        dice.append(cumulated_r)

    return normalize(dice)


def maximize(players_number, tables_number, responsabilities):
    """Gives a new set of parameters obtained maximizing the expected log
    likelihood."""

    parameters = {'table' : [], 'player' : []}

    for i in range(players_number):
        optimized_dice = optimize_player_dice(i,
                                              players_number, tables_number,
                                              responsabilities)
        parameters['player'].append(optimized_dice)

    for i in range(tables_number):
        optimized_dice = optimize_table_dice(i,
                                             players_number, tables_number,
                                             responsabilities)
        parameters['table'].append(optimized_dice)

    return parameters


def em_algorithm(observations):
    """Runs the EM algorithm to find the parameters that maximizes the
    probability of the given observations. The observations parameter
    is a list of length equal to the number of players observed: at position
    corresponding to player i, the list contains a list of length k containing
    the sum observed for player i at table k.

    The maximized probability is:
    P(S1i,...,SKi|parameters)
    """

    players_number = len(observations)
    tables_number = len(observations[0])
    parameters = initialize_parameters(players_number,tables_number)

    likelihood = expected_complete_loglikelihood(observations, parameters)
    converged = False
    it = 0
    while not converged:
        print "Log Likelihood"
        print likelihood

        responsabilities = get_responsabilities(observations, parameters)

        parameters = maximize(players_number, tables_number, responsabilities)

        old_likelihood = likelihood
        likelihood = expected_complete_loglikelihood(observations, parameters)
        assert likelihood >= old_likelihood

        if likelihood - old_likelihood < 10 ** -25 or it>MAX_IT:
            converged = True

        it +=1

    return parameters


def main():
    random.seed(3)
    parameters = {}

    K = 5
    N = 5
    parameters['table'] = [normalize([random.random() for i in range(6)])
                           for i in range(K)]
    parameters['player'] = [normalize([random.random() for i in range(6)])
                            for i in range(N)]

    table_dices = [(Dice(e),Dice(e)) for e in parameters['table']]
    c = Casino(K, table_dices)

    observations = []
    for i in range(N):
        player_dice = Dice(parameters['player'][i])
        results,_,_ = c.simulate_player(player_dice)
        observations.append(results)

    #print observations

    estimated_parameters = em_algorithm(observations)

    for table in range(K):
        print "Table "+str(table)
        print "Real dice"
        print parameters['table'][table]
        print "Estimated dice"
        print estimated_parameters['table'][table]

    for player in range(K):
        print "Player "+str(player)
        print "Real dice"
        print parameters['player'][player]
        print "Estimated dice"
        print estimated_parameters['player'][player]

if __name__ == '__main__':
    main()
