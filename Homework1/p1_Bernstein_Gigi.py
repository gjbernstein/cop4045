import math
import matplotlib.pyplot as plt
import numpy as np

a = ""
b = ""
c = ""

while True:
    a = input("enter value for coefficient a: ")
    if not a: #if enter key is pressed
        break #exit program
    a = float(a)
    b = float(input("enter value for coefficient b: "))
    c = float(input("enter value for coefficient c: "))

    temp = b**2 - 4*a*c
    if temp < 0:
        print("no real solutions")
        center = -b - 2*a
        min_x = center -2
        max_x = center +2
    elif temp == 0:
        x = (-b + temp**0.5)/(2*a)
        print(f"one solution: {x}")
        min_x = x - 2
        max_x = x + 2
    elif temp > 0:
        x1 = (-b + temp**0.5)/(2*a)
        x2 = (-b - temp**0.5)/(2*a)
        print(f"two solutions: {x1}, {x2}")
        min_x = x2 - 2
        max_x = x1 + 2

    xs = []
    ys = []

    n = 150 # n points
    dx = (max_x - min_x) / n # delta between points
    x = min_x

    while x <= max_x:
        xs.append(x)
        # edit this function
        # y = 2 * math.sin(2*math.pi*1*x)
        y = a*x**2 * b*x * c
        ys.append(y)
        x += dx

    # after the loop:
    plt.plot(xs, ys, "ro-") # creates the graph figure, but does not show it yet
    plt.show() 
