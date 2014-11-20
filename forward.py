from utils import Dice
import random

class Forward (object):
    def __init__(self, K, table_dices, player_dice):
        """Initialize the forward algorithm. K is the number of tables,
        table_dices is a list of length K composed by couple (d,d'):
        d is the dice of the table not primed, d' is the dice of the primed
        table, player_dice is the dice used by the player"""

        self.K = K
        self.table_dices = table_dices
        self.player_dice = player_dice

    def run(self, table, state, dice_results):
        """Run the forward algorithm to compute the probability that
        table k is in state=state h, given the dice_results of tables 1 to k.

        p(Zk = h | x1:xk)
        """

        assert table>=0 and table<=self.K  #tables 0 returns 1/2 primed, 1/2 not
        #state is 0 if table is not primed, 1 if table is primed
        assert state==0 or state==1
        assert len(dice_results)==table

        #initial states distribution
        primed = 1/2.0
        not_primed = 1/2.0

        for i in range(table):
            #apply transition matrix
            old_primed = primed
            old_not_primed = not_primed
            primed = 1/4.0*old_primed + 3/4.0*old_not_primed
            not_primed = 1/4.0*old_not_primed + 3/4.0*old_primed

            assert abs((primed + not_primed) - 1.0) < 10 ** -10

            #primed = p(xi | zi = primed)
            primed = self.table_dices[i][1][dice_results[i]]
            #not_primed = p(xi | zi = not_primed)
            not_primed = self.table_dices[i][0][dice_results[i]]

            if primed + not_primed < 10 ** -10:
                #The dice results given in input couldn't be obtained
                #by the dices given for the tables
                return 0.0

            #normalize
            primed = primed / (primed + not_primed)
            not_primed = not_primed / (primed + not_primed)

        if state==0:
            return not_primed
        else:
            return primed



def main():
    random.seed(1)
    fair_dice = Dice([1/6.0,1/6.0,1/6.0,1/6.0,1/6.0,1/6.0])
    dice1 = Dice([1.0,0,0,0,0,0])
    dice3 = Dice([0,0,1.0,0,0,0])
    dice6 = Dice([0,0,0,0.1,0,0.9])
    unfair_dice = Dice([1/10.0,1/10.0,1/10.0,1/10.0,1/10.0,1/2.0])

    K = 10
    table_dices = [(dice3, dice6) for i in range(K)]
    player_dice = dice1
    forward_alg = Forward(K, table_dices, player_dice)

    print forward_alg.run(5, 1, [6,6,3,4,6])
    print forward_alg.run(0, 1, [])

if __name__ == '__main__':
    main()
