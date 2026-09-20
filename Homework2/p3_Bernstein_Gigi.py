def add_user(sn, username, fullname):
    '''adds to the social network stored in
    dictionary sn a new user with the given username and full name. The new user has initially no friend
    links. The function returns True if the user was added successfully and False, otherwise, i.e. if the user
    existed before.'''
    try:
        if username in sn:
            return False
        else:
            sn[username] = (fullname, [])
            return True
    except:
        print("Unexpected Error")
        raise

def add_friend(sn, user1, user2):
    '''takes a dictionary sn with a social network and
    adds a mutual friend link between users user1 and user2. The function returns True if success, and
    False otherwise, e.g. when at least one the user names given are not found in sn.'''
    try:
        if user1 in sn and user2 in sn:
            sn[user1][1].append(user2)
            sn[user2][1].append(user1)
            return True
        else:
            return False
    except:
        print("Unexpected Error")
        raise

def get_friends(sn, user1, distance):
    '''takes a dictionary sn with a social network, a
    username in argument user1, and a positive integer in argument distance and that returns a list with all
    friends of user1 at link distance 1, 2, …, distance.
    Friends at distance=1 of a user are the users in its immediate list of friends, Friends at distance=2 of 
    a user are the users at distance 1 and the users in the immediate friend lists of users at distance 1. 
    The function returns the empty list if the are no friends to return or if the given user name is wrong.'''
    try:
        if user1 not in sn:
            return []
        else:
            friends = set()
            current_level = {user1}
            for _ in range(distance):
                next_level = set()
                for user in current_level:
                    next_level.update(sn[user][1])
                friends.update(next_level)
                current_level = next_level
            friends.discard(user1)  # Remove the original user from the list of friends
            return list(friends)
    except:
        print("Unexpected Error")
        raise

def save_network(filename, sn):
    '''saves a social network dictionary to a .CSV file.
    The function takes as parameter the file name and the dictionary.'''
    try:
        with open(filename, 'w') as file:
            for username, (fullname, friends) in sn.items():
                friends_str = ','.join(friends)
                file.write(f"{username},{fullname},{friends_str}\n")
    except FileNotFoundError:
        print(f"Unable to find a file with name: {filename} . Check spelling and placement of file.")
        raise
    except:
        print("Unexpected Error")
        raise

def load_network(filename):
    '''reads a social network from a .CSV file saved with
    save_network(…) and that returns the dictionary object.'''
    try:
        sn = {}
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                username = parts[0]
                fullname = parts[1]
                friends = parts[2:] if len(parts) > 2 else []
                sn[username] = (fullname, friends)
        return sn
    except FileNotFoundError:
        print(f"Unable to find a file with name: {filename} . Check spelling and placement of file.")
        raise
    except:
        print("Unexpected Error")
        raise

def main():
    sn = {}
    add_user(sn, "alice", "Alice Smith")
    add_user(sn, "bob", "Bob Johnson")
    add_friend(sn, "alice", "bob")
    print(get_friends(sn, "alice", 1))  # Should print ['bob']
    save_network("network.csv", sn)
    print(sn)  # Should print the social network dictionary
    loaded_sn = load_network("network.csv")
    print(loaded_sn)  # Should print the same as sn

if __name__ == "__main__":
    main()