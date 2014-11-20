import random
import numpy as np

class Dice(object):
    def __init__(self, probabilities):
        """Initialize dice. Probabilities is expected to be of length 6
        and add up to 1"""

        if len(probabilities)!=6 or abs(sum(probabilities)-1) > 10 ** -10:
            raise ValueError('Impossible to instantiate Dice with given '
                             'probabilities. Sum='+str(sum(probabilities)))

        cutoffs = np.cumsum(probabilities)
        self.cutoffs = cutoffs
        self.probabilities = probabilities

    def roll(self):
        """Roll the Dice and returns the result"""

        p = random.random()
        res = self.cutoffs.searchsorted(p)
        return res+1

    def __getitem__(self, val):
        assert val>=1 and val<=6

        return self.probabilities[val-1]

    def __str__(self):
        s = ["{",]
        for i in range(6):
            s.append("{}:{: .2f}, ".format(i+1,self.probabilities[i]))
        s.append("}")
        return "".join(s)
