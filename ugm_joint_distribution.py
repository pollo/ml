phi1 = {(0,0): 30, (0,1): 5, (1,0): 1, (1,1): 10}
phi2 = {(0,0): 100, (0,1): 1, (1,0): 1, (1,1): 100}
phi3 = {(0,0): 1, (0,1): 100, (1,0): 100, (1,1): 1}
phi4 = {(0,0): 100, (0,1): 1, (1,0): 1, (1,1): 100}

def factors(a,b,c,d):
    return phi1[a,b] * phi2[b,c] * phi3[c,d] * phi4[d,a]

def partition_function():
    combinations = [list('{:04b}'.format(i)) for i in range(16)]
    fact = [factors(*map(int,comb)) for comb in combinations]
    return sum(fact)

def p(a,b,c,d):
    return float(factors(a,b,c,d)) / partition_function()

if __name__ == '__main__':
    print "Z = "+str(partition_function())
    print "P(A=0,B=0,C=0,D=0) = "+str(p(0,0,0,0))
