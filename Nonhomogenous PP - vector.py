import numpy as np
import matplotlib.pyplot as plt

def density_v(t, T):
    return (np.sin(t))**2/(1/2*(T-np.sin(T)*np.cos(T)))

def npp_v(T, m):
    v_i = []

    for i in range(m):
        k = 0
        v = []
        n = np.random.poisson(1/2*(T-np.sin(T)*np.cos(T)))
        while k != n:
            if n != 0:
                u_1 = np.random.uniform(0,T)
                u_2 = np.random.uniform(0, 2/(T-np.sin(T)*np.cos(T)))
                if u_2 <= density_v(u_1, T):
                    v.append(u_1)
                    k+=1
        v_i.append(sorted(v))
    return v_i

T = 10*np.pi
m = 1000

data = npp_v(T, m)
print(data)
for i in range(m):
    plt.hlines(0,0,data[i][0], color='b')
    plt.step(data[i], np.linspace(0,len(data[i]),len(data[i])), color='b')
x = np.linspace(0,T)
plt.plot(x, 1/2*(x - np.sin(x)*np.cos(x)), color='r', label='EN(t)')
plt.hlines(0,0,0.001, color='b', label='Realizacje NPP')
plt.axvline(x = T, label='Horyzont czasowy T', linestyle='dashed', color='k')
plt.xlim(0,T+2)
plt.legend()
plt.title('Generator NPP przy użyciu wektora momentów skoków')
plt.show()