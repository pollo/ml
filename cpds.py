#X -> understands explaining away
#Y -> looks for new example
#Z -> having an original solution

X1 = 0.15
X0 = 1 - X1
Y1 = 0.10
Y0 = 1 - Y1

Z00 = 0.10
Z01 = 0.25
Z10 = 0.25
Z11 = 0.90

def Z1():
    return \
        X0*Y0*Z00+\
        X0*Y1*Z01+\
        X1*Y0*Z10+\
        X1*Y1*Z11

def Z1_X1():
    return Y1 * Z11 + Y0 * Z10

def Z1_Y1():
    return X1 * Z11 + X0 * Z01

def X1_Z1():
    return X1 * Z1_X1() / Z1()

def X1_Z1Y1():
    return X1 * Z11 / Z1_Y1()

def Y1_Z1():
    return Y1 * Z1_Y1() / Z1()

def Y1_Z1X1():
    return Y1 * Z11 / Z1_X1()

print "P(Z=1) = "+str(Z1())
print "P(Z=1 | X=1) = "+str(Z1_X1())
print "P(Z=1 | Y=1) = "+str(Z1_Y1())
print "P(X=1 | Z=1) = "+str(X1_Z1())
print "P(X=1 | Z=1,Y=1) = "+str(X1_Z1Y1())
print "P(Y=1 | Z=1) = "+str(Y1_Z1())
print "P(Y=1 | Z=1,X=1) = "+str(Y1_Z1X1())
