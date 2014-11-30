import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from math import pi,sin
from scipy.spatial.distance import cdist

#define noise as N(0,05)
sigma2 = 0.5
noise = scipy.stats.multivariate_normal(0.0,sigma2)
#produce data
X = np.linspace(-pi, pi, 7)
Y = [sin(x) + noise.rvs() for x in X]

output_path = '/home/pollo/university/ml/report/images/'

def prior_W(X, l2):
    #compoute covariance matrix
    distance = cdist(X,X)
    distance = np.square(distance)
    print distance
    exponents = distance / (-2*l2)
    print exponents
    covariance = np.exp(exponents)
    #covariance *= sigma2
    print covariance
    return scipy.stats.multivariate_normal(np.zeros(len(X)),covariance)

def sample_prior_W(X, prior):
    for i in range(10):
        Y = prior.rvs()
        plt.plot(X,Y)
    #plt.ylim(-4,6)
    #plt.savefig(output_path+'lr_sample_posterior_'+str(len(X))+'.png')
    plt.show()
    plt.close()

def main():
    X = np.transpose(np.array([np.linspace(-4, 4, 500)]))
    print X
    l2 = 10
    prior = prior_W(X, l2)
    sample_prior_W(X, prior)

if __name__ == '__main__':
    main()
