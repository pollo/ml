from utils import Dice
from forward import Forward

import random

EPS = 10 ** -25

class Viterbi(object):
    def __init__(self, K, table_dices, player_dice):
        """Initialize the viterbi algorithm. K is the number of tables,
        table_dices is a list of length K composed by couple (d,d'):
        d is the dice of the table not primed, d' is the dice of the primed
        table, player_dice is the dice used by the player"""

        self.K = K
        self.table_dices = table_dices
        if (len(table_dices) != K):
            raise ValueError('A list of K couple of dices should be provided '
                             'for the parameter table_dices')
        self.player_dice = player_dice
        #initialize forward algorithm for later use
        self.forward_alg = Forward(K, table_dices, player_dice)

    def run(self, observations):
        """Takes a list of observations S1:K and returns the path through
        the states x1:K which is most likely:

        argmax{x1:K} (p(x1:K | S1:K))"""

        #memoization variable to store dp results.
        #Maps (table,result) to (probability, previous_result)
        self.memoization = {}

        #computes range of possible values for last table given last observed
        observed = observations[-1]
        lower_bound = max(observed-6,1)
        upper_bound = min(observed-1,6)

        max_found = 0
        max_result = 0
        for result in range(lower_bound,upper_bound+1):
            viterbi_var = self.viterbi_variable(self.K, result, observations)

            if viterbi_var > max_found:
                max_found = viterbi_var
                max_result = result

        if max_found < EPS:
            print 'The observations given cannot be produced with given dices'
            return []

        return self.reconstruct_path(self.K, max_result)

    def viterbi_variable(self, table, result, observations):
        """Computes the probability of the dice in table=table k of being equal
        to result=result c, when the most probable path fron 1 to k-1 is taken.
        The probability returned is actually the joint with the probability
        of the path x1:k-1 taken and of the observations up to k.

        Table is the index table, from 1 to K. Result is the result of the
        table's dice, from 1 to 6. Observations are the list of the observed
        sum from table 1 to k.

        max{x1:k-1} (p(x1:k-1, Xk=c, S1:k) )
        """

        assert table>0 and table<=self.K
        assert result>=1 and result<=6
        assert len(observations)==table

        print "viterbi variable:"
        print "table {} result {} observations {}".format(
            table,result,observations)

        #sum observed at table k
        observed = observations[table-1]

        #base case
        if (table == 1):
            #probability of table 1 giving result
            result_probability = self.transition_probability(1, result, [])
            print "result_probability "+str(result_probability)

            #probability of observing the sum given the result
            emission_probability = self.emission_probability(1,
                                                             result,
                                                             observed)
            print "emission_probability "+str(emission_probability)

            return result_probability * emission_probability

        if ((table,result) not in self.memoization):
            #computes range of possible values for previous result based
            #on previous observation
            previous_observation = observations[table-2]
            lower_bound = max(previous_observation-6,1)
            upper_bound = min(previous_observation-1,6)

            max_prob = 0
            max_previous_result = 0
            for previous_result in range(lower_bound,upper_bound+1):
                print "previous result "+str(previous_result)

                viterbi_var = self.viterbi_variable(table-1,
                                                    previous_result,
                                                    observations[:-1])

                print "viterbi var returned "+str(viterbi_var)

                if (viterbi_var < EPS):
                    #this previous result is impossible, try the others
                    continue

                previous_results = self.reconstruct_path(table-1,
                                                         previous_result)

                print "selected path "+str(previous_results)

                #probability of table k giving result
                result_probability = self.transition_probability(
                    table,
                    result,
                    previous_results)
                print "result_probability "+str(result_probability)

                #probability of observing the sum given the result
                emission_probability = self.emission_probability(table,
                                                                 result,
                                                                 observed)
                print "emission_probability "+str(emission_probability)

                prob = viterbi_var * result_probability * emission_probability

                print "prob of previous result {} at table {} is {}".format(
                    previous_result, table, prob)
                print

                if prob > max_prob:
                    max_prob = prob
                    max_previous_result = previous_result

            self.memoization[(table,result)] = (max_prob, max_previous_result)

        return self.memoization[(table,result)][0]

    def reconstruct_path(self, table, result):
        """Returns the most probable path across the states found by the viterbi
        algorithm from table=table giving result=result
        """

        if table==1:
            return [result,]

        previous_result = self.memoization[(table, result)][1]
        previous_results = self.reconstruct_path(table-1, previous_result)

        previous_results.append(result)

        return previous_results

    def emission_probability(self, table, result, observed):
        """Returns the probability of table=table k, with dice result=result c,
        emitting an observed sum=observed v

        P(Sk=v | Xk=c)
        """

        assert table>0 and table<=self.K
        assert result>=1 and result<=6
        assert observed>=2 and observed<=12

        return self.player_dice[observed-result]

    def transition_probability(self, table, result, previous_results):
        """Computes the probability of the dice at table=table k being equal
        to result=result c given the results of the table's dices from 1 to
        k-1.

        P(Xk=c | x1:k-1)
        """

        assert table>0 and table<=self.K
        assert result>=1 and result<=6
        assert len(previous_results) == table-1

        #probability of table k being primed
        primed = self.probability_state(table, 1, previous_results)
        #probability of emitting result if the table is primed
        emission_primed = self.table_dices[table-1][1][result]

        #probability of table k being not primed
        not_primed = self.probability_state(table, 0, previous_results)
        #probability of emitting result if the table is not primed
        emission_not_primed = self.table_dices[table-1][0][result]

        if primed + not_primed < EPS:
            #Table k dice cannot be equal result
            return 0.0

        assert abs((primed + not_primed) - 1.0) < 10 ** -10
        return not_primed * emission_not_primed + primed * emission_primed

    def probability_state(self, table, state, dice_results):
        """Computes the probability of being in state=state h at table=table k,
        given the dice results for tables from 1 to k-1

        P(Zk=h | x1:k-1)"""

        assert table>0 and table<=self.K
        assert state==0 or state==1
        assert len(dice_results) == table-1

        print "probability table {} of being in state {} given {}".format(
            table,state,dice_results)
        #probability of previous table being equal state h
        previous_state = self.forward_alg.run(table-1,
                                              state,
                                              dice_results)

        #probability of previous table being not equal state h
        previous_not_state = self.forward_alg.run(table-1,
                                                  (state+1)%2,
                                                  dice_results)

        if previous_state + previous_not_state < EPS:
            #the dice_results sequence is not possible
            return 0.0

        assert abs((previous_state+previous_not_state) - 1.0) < 10 ** -10

        return 1/4.0 * previous_state + 3/4.0 * previous_not_state


def main():
    random.seed(1)
    fair_dice = Dice([1/6.0,1/6.0,1/6.0,1/6.0,1/6.0,1/6.0])
    dice1 = Dice([1.0,0,0,0,0,0])
    dice3 = Dice([0,0,1.0,0,0,0])
    dice6 = Dice([0,0,0,0.1,0,0.9])
    unfair_dice = Dice([1/10.0,1/10.0,1/10.0,1/10.0,1/10.0,1/2.0])
    increasing = [1,2,4,8,16,32]
    increasing = [float(e)/sum(increasing) for e in increasing]
    decreasing = increasing[:]
    decreasing.reverse()
    inc_dice = Dice(increasing)
    dec_dice = Dice(decreasing)

    K = 5
    table_dices = [(dice3, dice6) for i in range(K)]
    player_dice = Dice([1/2.0,1/2.0,0,0,0,0])
    viterbi_alg = Viterbi(K, table_dices, player_dice)

    print viterbi_alg.run([7,5,4,4,5])

    K = 10
    table_dices = [(fair_dice, fair_dice) for i in range(K)]
    player_dice = fair_dice

    viterbi_alg = Viterbi(K, table_dices, player_dice)
    print viterbi_alg.run([11, 6, 6, 9, 4, 8, 2, 9, 4, 6])
    #print viterbi_alg.run([11, 6, 6, 9, 4, 8, 2])###, 9, 4, 8, 2, 9, 4, 6])

    K = 10
    table_dices = [(inc_dice,dec_dice) for i in range(K)]
    player_dice = fair_dice
    viterbi_alg = Viterbi(K, table_dices, player_dice)
    print viterbi_alg.run([7, 6, 7, 12, 8, 7, 11, 6, 10, 4])
    #print viterbi_alg.run([12, 8])

    K = 20
    table_dices = [(inc_dice,dec_dice) for i in range(K)]
    player_dice = inc_dice
    viterbi_alg = Viterbi(K, table_dices, player_dice)
    print viterbi_alg.run([8, 7, 8, 7, 10, 12, 7, 11, 5, 12, 7, 9, 9, 12, 8, 12, 7, 10, 5, 11])

if __name__ == '__main__':
    main()
