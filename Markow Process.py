# p_array = [[0.1,0.35,0.55],[0.2,0.25,0.55],[0.3,0.45,0.25]] zsumujemy żeby losować
import numpy as np

p_array = [[0.1,0.45,1],[0.2,0.45,1],[0.3,0.75,1]]

def func(a):
    n_i = []
    # startujemy z wiersza 2 (ostatniego)
    start = 2
    for a in range(a):
        n = 0
        while start != 1:
            u = np.random.uniform()
            if u <= p_array[start][0]:
                n += 1
                start = 0
            elif u > p_array[start][0] and u <= p_array[start][1]:
                n += 1
                break
            else:
                start = 2
                n += 1
        n_i.append(n)

    return np.mean(n_i)


print(func(10000))
# powinno wyjść 2.35

