import numpy as np
import matplotlib.pyplot as plt
import math

def plot_function(fun_str:str, domain:tuple, ns:int):
    step = (domain[1] - domain[0]) / (ns - 1)
    xs = []
    ys = []
    for x in np.arange (domain[0], domain[1] + step, step):
        xs.append(x)
        y = eval(fun_str)
        ys.append(y)
    print ('{:>10s}{:>10s}'.format("x", "y"))
    print("-"*20)
    for i in range (ns):
        print('{:>+10.4f}{:>+10.4f}'.format(xs[i], ys[i]))

    # create plot
    plt.plot(xs, ys, "ro-") # creates the graph figure, but does not show it yet
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.show()

fun_str = input("Enter function with variable x: ")
ns = int(input("Enter number of samples: "))
xmin = float(input("Enter xmin: "))
xmax = float(input("Enter xmax: "))
domain = (xmin, xmax)
plot_function(fun_str, domain, ns)

