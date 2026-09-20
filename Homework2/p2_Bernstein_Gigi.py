# problem a
''' Write a list comprehension that returns all tuples (a,b,c,d ), with a,b,c,d distinct integers, such that
1<=a,b,c,d<=10, and a2+b2=c2 + d2'''
a = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4
        and a ** 2 + b ** 2 == c ** 2 + d ** 2
    ]
print(f"a = {a}")

# problem b
'''Write a list comprehension that produces a list with tuples where the first element of the tuple is lowercase version of a string in
the initial list, the second element of the tuple is the length of the element of the initial list, and the
resulting list contains only tuples for strings with the length shorter than five characters.
For our example the list comprehension should return [‘one’, 3), (‘two’, 3), 'ten', 3)].'''
words = ["One", "SEVEN", "three", "two", "Ten"]
b = [(word.lower(), len(word)) for word in words if len(word) < 5]
print(f"\n\nb = {b}")

# problem c
'''Write a list comprehension that produces a list with the full names in this format: “Firstname M.
Lastname”. The resulting list should look like ['Christopher A. Kutcher', 'Elizabeth S. Fey']. The list
comprehension should work for any list names with the proper format.'''
names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
c = [f"{name.split()[0]} {name.split()[1][0]}. {name.split()[2]}" for name in names]
print(f"\n\nc = {c}")

# problem d
'''Consider these two lists of strings:
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
Write a list comprehension that returns a list of tuples (w1, w2) where w1 is from lst1 and w2 is from
lst2 and w1 and w2 are anagrams (case insensitive).
For the lists above, the anagram pairs are in this list:
[('Trams', 'Smart'), ('Elbows', 'Bowels'), ('Tops', 'Stop'), ('Astral', 'Altars')]'''
lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
d = [(w1, w2) for w1 in lst1 for w2 in lst2 if sorted(w1.lower()) == sorted(w2.lower())]
print(f"\n\nd = {d}")

# problem e
'''Consider a list of distinct strings like this one:
s = ['one', 'two', 'three']
Write a dictionary comprehension that returns a dictionary that maps each string from s to its length.
Example: {'one': 3, 'two': 3, 'three': 5}'''
s = ['one', 'two', 'three']
e = {string: len(string) for string in s}
print(f"\n\ne = {e}")

# problem f
'''Write a dictionary comprehension that uses a string in a variable called text and that returns a
dictionary with entries i:c where i is the index of character c in text only for characters c that are vowels
(a e i o u). Checking for vowels is case insensitive.'''
text = "Hello world"
f = {num: c for num, c in enumerate(text) if c.lower() in 'aeiou'}
print(f"\n\nf = {f}")

