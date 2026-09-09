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
    elif temp == 0:
        x = (-b + temp**0.5)/(2*a)
        print(f"one solution: {x}")
    elif temp > 0:
        x1 = (-b + temp**0.5)/(2*a)
        x2 = (-b - temp**0.5)/(2*a)
        print(f"two solutions: {x1}, {x2}")
