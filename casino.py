from utils import Dice

import random

class Casino(object):
    def __init__(self, K, table_dices):
        """Initialize the simulation. K is the number of tables, table_dices
        is a list of length K composed by couple (d,d'): d is the dice of the
        table not primed, d' is the dice of the primed table"""

        self.K = K
        self.table_dices = table_dices

    def simulate_player(self, player_dice):
        """Simulate the sequence of a player with Dice dice"""

        #Player starts with primed table with probability 1/2
        primed = True if random.random() > 0.5 else False

        observations = []
        table_results = []
        player_results = []
        for table in range(self.K):
            #roll dices and observe sum
            player_result = player_dice.roll()
            if (primed):
                table_result = self.table_dices[table][1].roll()
            else:
                table_result = self.table_dices[table][0].roll()
            table_results.append(table_result)
            player_results.append(player_result)
            observations.append(player_result+table_result)

            #update primed state, changes with probability 3/4
            primed = primed if random.random()<1/4.0 else not primed

        return observations, player_results, table_results

def simulate(K, N, table_dices, player_dices):
    print "Simulation K="+str(K)+", N="+str(N)
    for i,dices in enumerate(table_dices):
        print "T"+str(i)+"  -> "+str(dices[0])
        print "T"+str(i)+"' -> "+str(dices[1])
    print

    c = Casino(K, table_dices)
    for i,dice in enumerate(player_dices):
        print "Player "+str(i+1)+" -> "+str(dice)

        observations,player_results,table_results = c.simulate_player(dice)
        print observations
        print player_results
        print table_results
    print

def main():
    random.seed(1)
    fair_dice = Dice([1/6.0,1/6.0,1/6.0,1/6.0,1/6.0,1/6.0])
    dice1 = Dice([1.0,0,0,0,0,0])
    dice3 = Dice([0,0,1.0,0,0,0])
    dice6 = Dice([0,0,0,0,0,1.0])
    unfair_dice = Dice([1/10.0,1/10.0,1/10.0,1/10.0,1/10.0,1/2.0])
    increasing = [1,2,4,8,16,32]
    increasing = [float(e)/sum(increasing) for e in increasing]
    decreasing = increasing[:]
    decreasing.reverse()
    inc_dice = Dice(increasing)
    dec_dice = Dice(decreasing)

    N = 3
    K = 10
    table_dices = [(fair_dice, fair_dice) for i in range(K)]
    player_dices = [fair_dice for i in range(N)]
    simulate(K, N, table_dices, player_dices)

    N = 3
    K = 10
    table_dices = [(fair_dice, unfair_dice) for i in range(K)]
    player_dices = [fair_dice for i in range(N)]
    simulate(K, N, table_dices, player_dices)

    N = 3
    K = 10
    table_dices = [(dice3, dice6) for i in range(K)]
    player_dices = [dice1 for i in range(N)]
    simulate(K, N, table_dices, player_dices)

    N = 3
    K = 10
    table_dices = [(inc_dice,dec_dice) for i in range(K)]
    player_dices = [fair_dice for i in range(N)]
    simulate(K, N, table_dices, player_dices)

    N = 3
    K = 20
    table_dices = [(inc_dice,dec_dice) for i in range(K)]
    player_dices = [inc_dice for i in range(N)]
    simulate(K, N, table_dices, player_dices)

if __name__ == '__main__':
    main()
