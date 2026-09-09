
def find_Pythagorean(n):
    triples = []

    c = 0.0 # declare c
    float(c) # make c a float

    for a in range(1, n+1):
        for b in range(1, n+1):
            print(a, b, c)
            c = (a**2 + b**2)**0.5
            if c.is_integer(): # if c is a whole number
                triple_tuple = (a, b, c)
                triples.append(triple_tuple)

    return triples

n = int(input("input n: "))
print(find_Pythagorean(n))