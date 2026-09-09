def find_dup_str(s:str, n):
    for i in range (len(s) - 2*n + 1): # only searches through the length where there could be a possible duplicate after
        substr = s[i: i + n] # substring of length n beginning with i
        searchstr = s[i + n:] # the rest of the string after the substring
        if substr in searchstr:
            return substr
    return ""

s = input("enter string: ")
n = int(input("enter length of duplicate to find: "))
print(find_dup_str(s, n))

def find_max_dup(s):
    for n in reversed(range(2, len(s)//2 + 1)): # starting at the highest posiible length of duplicate
        found = find_dup_str(s, n)
        if found != "": #if a duplicate is found
            return found
    return found

s = input("enter string: ")
print(find_max_dup(s))

