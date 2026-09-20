def line_number(file_name1:str, file_name2:str):
    try:
        file1 = open(file_name1, "r") # open file to read from
        file2 = open(file_name2, "w") # open file to write to
        line_num = 0
        for line in file1: # iterate through each line in the file
            line_num += 1
            print(f"{line_num}. {line}", file=file2) # write the line number and the line to the output file
        file1.close()
        file2.close()
    except FileNotFoundError:
        print(f"Unable to find a file with name: {file_name1} . Check spelling and placement of file.")
        raise
    except:
        print("Unexpected Error")
        raise

def parse_functions(file_name:str): 
    ''' reads and parses the Python file and returns a tuple of tuples where each tuple
    has its element 0 the line number of the function definition, element 1 the function name, element 2 the
    formal argument list as a string, and element 3 the function code as a string (signature and body), with
    all empty lines and comments removed.'''   
    try:
        list_of_tuples = [] # create an empty list to hold the functions' tuples
        file = open(file_name, "r") # open the file to read from
        line_num = 0 # initialize the line number counter
        func_num = -1 # initialize the function counter
        for line in file: # iterate through each line in the file
            input_str = "" # initialize the input string to hold the argument list
            line_num += 1 # increment the line number counter
            if line.startswith("def"): # if the line is the beginning of a function definition
                if func_num >= 0: # if this is not the first function
                    inner_tuple += (code, ) # add the previous function's code to the inner tuple
                    list_of_tuples.append(inner_tuple) # add the inner tuple to the list of tuples
                func_num += 1 # increment the function counter
                inner_tuple = (line_num, ) # create a new inner tuple with the line number of the function definition
                code = "" # initialize the code string to hold the function code
                func_name = line.split("(")[0].strip("def ") # extract the function name from the line
                inner_tuple += (func_name, ) # add the function name to the inner tuple
                func_input = False # bool to show if it is the argument or not
                for char in line:
                    if char == ")":
                        func_input = False
                    if func_input == True:
                        input_str += char
                    if char == "(":
                        func_input = True
                inner_tuple += (input_str,)
            if func_num >= 0:
                    if not line.startswith("#"):
                        if "#" in line:
                            line = line.split(" #")[0] + "\n" # remove comments from the line
                        if line.strip() != "": # if the line is not empty
                            if line.startswith("def") or line.startswith("    "):
                                line = line.replace("    ", "\t")
                                code += line
        inner_tuple += (code, ) # add the last function's code to the inner tuple
        list_of_tuples.append(inner_tuple) # add the last function's inner tuple to the list of tuples
        file.close()
        list_of_tuples.sort(key=lambda x: x[1]) # sort the list of tuples by the name of the function
        return tuple(list_of_tuples)
    except FileNotFoundError:
        print(f"Unable to find a file with name: {file_name} . Check spelling and placement of file.")
        raise
    except:
        print("Unexpected Error")
        raise

def main():
    line_number("p1_Bernstein_Gigi.py", "test_file.txt")
    print(parse_functions("funs.py"))

if __name__ == "__main__":
    main()