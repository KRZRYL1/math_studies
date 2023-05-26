import random
import matplotlib.pyplot as plt
import math
from scipy.stats import genpareto, pareto
import numpy as np
random.seed(1)

def density(x, mu, alpha):
  return mu/((1-x)**(1/alpha))

def density_odwrócona(x, mu, alpha):
  return (alpha*mu**alpha/x)**(1/(alpha+1))

def density_Pareto(x, mu, alpha):
  return alpha*mu**alpha/(x**(alpha+1))

epsilon = float(input('Podaj błąd przybliżenia'))
mu = float(input('Podaj mu'))
alpha = float(input('Podaj alpha'))

def approx_r(mu, alpha):
    r = np.linspace(1,10,10000)
    X = []
    abs_ = []
    for i in r:
        f_r = density_Pareto(i, mu, alpha)
        v = i * f_r + (mu / i) ** alpha
        x_i = np.zeros(256)
        x_i[-1] = i
        for b in range(254, 0, -1):
            den = v / x_i[b + 1] + density_Pareto(x_i[b + 1], mu, alpha)
            x_i[b] = density_odwrócona(den, mu, alpha)
        x_i[0] = density_odwrócona(v / x_i[1] + density_Pareto(x_i[1], mu, alpha),mu,alpha)
        X.append(x_i[0])
        abs_.append(abs(x_i[0] - 1))

    for i in range(len(abs_)):
        if X[i]>=1:
            if epsilon/2 < abs_[i] < epsilon:
                print(abs_[i], i)
                r = r[i]
                print(r)
                f_r = density_Pareto(r, mu, alpha)
                v = r * f_r + (mu / r) ** alpha
                x_i = np.zeros(256)
                x_i[-1] = r
                for b in range(254, 0, -1):
                    den = v / x_i[b + 1] + density_Pareto(x_i[b + 1], mu, alpha)
                    x_i[b] = density_odwrócona(den, mu, alpha)
                x_i[0] = density_odwrócona(v / x_i[1] + density_Pareto(x_i[1], mu, alpha), mu, alpha)
                print(X[i])
                return x_i, r



data = approx_r(mu,alpha)
x_i = data[0]
r = data[1]
v = r * density_Pareto(r, mu, alpha) + (mu / r) ** alpha


def get_vec(r, mu, alpha):
  k0 = np.floor(2**32*r*(density_Pareto(r, mu, alpha)/v))
  w0 = ((1/2)**32)*(v/density_Pareto(r, mu, alpha))
  k = np.zeros(256)
  w = np.zeros(256)
  k[0] = k0
  w[0] = w0

  for i in range(1, 255):
      k[i] = np.floor(2**32 * (x_i[i-1]/x_i[i]))
      w[i] = ((1/2)**32)*x_i[i]
  return k, w

def binary_to_decimal(binary):
    decimal = 0
    power = len(binary) - 1
    for digit in binary:
        decimal += int(digit) * 2 ** power
        power -= 1
    return decimal


def pareto_zig(mu, alpha, n):
    r = data[1] + mu
    k, w = get_vec(r, mu, alpha)
    f_x = [density_Pareto(y, mu, alpha) for y in x_i]
    results = []
    for i in range(n):
        binary = [str(np.random.randint(0, 2)) for i in range(32)]
        j = binary_to_decimal(binary)
        binary_i = binary[-8:]
        i = binary_to_decimal(binary_i)
        x = j*w[i]
        u = random.random()
        if j < k[i] and x >= mu:
           results.append(x)
        elif i == 0:
           results.append(density(random.random(), mu, alpha))
        elif (f_x[i-1]-f_x[i])*random.random() < (density_Pareto(x, mu, alpha) - f_x[i]):
           if x >= mu:
              results.append(x)
    return results

x = np.linspace(0, 5, 1000)
plt.hist(pareto_zig(mu, alpha, 30000), bins = 70, density = True)
plt.plot(x, pareto.pdf(x, alpha, scale=mu))
plt.show()