import random
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

#define the prior of W=N(0,I)
prior_W = scipy.stats.multivariate_normal(np.zeros(2),np.identity(2))
X = np.linspace(-1,1,200)
W = np.array([-1.3,0.5])
#define noise as N(0,03)
sigma2 = 0.3
noise = scipy.stats.multivariate_normal(0.0,sigma2)
Y = [x*W[0]+W[1] + noise.rvs() for x in X]

def likelihood(Y, X, W):
    tot_l = 1
    for y,x in zip(Y,X):
        mu = W[0]*x + W[1]
        l = scipy.stats.multivariate_normal(mu, 0.3)
        tot_l *= l.pdf(y)
    return tot_l

def posterior_W(Y, X):
    X = np.array([[x, 1] for x in X])
    #posterior covariance
    inv_covariance = np.dot(np.transpose(X), X) / sigma2 + np.identity(2)
    covariance = np.linalg.inv(inv_covariance)
    #posterior mean
    Xy = np.dot(np.transpose(X),Y)/sigma2
    mean = np.dot(covariance,Xy)
    return scipy.stats.multivariate_normal(mean,covariance)

def visualize_prior_W():
    xaxis = np.linspace(-2, 2, 100)
    yaxis = np.linspace(-2, 2, 100)
    z = [[prior_W.pdf([x,y]) for x in xaxis] for y in yaxis]
    z.reverse()
    im = plt.imshow(z,extent=[-2,2,-2,2])
    plt.colorbar(im, orientation='vertical')
    plt.ylabel('Intercept')
    plt.xlabel('Slope')
    plt.show()

def visualize_posterior_W(Y, X):
    print "Data: "
    print X
    print Y
    xaxis = np.linspace(-2, 2, 100)
    yaxis = np.linspace(-2, 2, 100)
    #z = [[prior_W.pdf([x,y])*likelihood(Y, X, [x,y])
    #      for x in xaxis] for y in yaxis]
    posterior = posterior_W(Y,X)
    z = [[posterior.pdf([x,y])
          for x in xaxis] for y in yaxis]
    z.reverse()
    fig, ax = plt.subplots()
    im = ax.imshow(z,extent=[-2,2,-2,2])
    plt.colorbar(im, orientation='vertical')
    plt.ylabel('Intercept')
    plt.xlabel('Slope')
    plt.show()

def sample_posterior_W(Y, X):
    xmax = 1.5
    xmin = -1.5
    posterior = posterior_W(Y,X)
    for i in range(100):
        w = posterior.rvs()
        plt.plot([xmin,xmax],[xmin*w[0]+w[1],xmax*w[0]+w[1]])
    plt.plot(X, Y, 'ko')
    plt.show()

def main():
    visualize_prior_W()
    visualize_posterior_W([Y[175]],[X[175]])
    sample_posterior_W([Y[175]],[X[175]])
    visualize_posterior_W([Y[75],Y[175]],[X[75],X[175]])
    sample_posterior_W([Y[75],Y[175]],[X[75],X[175]])
    visualize_posterior_W(Y,X)
    sample_posterior_W(Y,X)


if __name__ == '__main__':
    main()
