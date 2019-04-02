import os


def get_user_data():
    """
    :return:  Returns a dictionary of all users referenced in the user file
    """
    users = open('user.txt', 'r').readlines()
    userbase = dict()
    for user in users:
        user = user.strip('\n')
        data = user.split(',')
        userbase[data[0]] = data[1]
    return userbase


def signup():
    print("Sign Up: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    while not _create_account(username, password):
        signup()
        return


def _create_account(username, password):
    users = open('user.txt', 'a')
    userbase = get_user_data()
    if username not in userbase.keys():
        users.write("\n{0},{1}".format(username, password))
        os.system(f"mkdir Users\\{username}")
        open(f"Users\\{username}\\user.data", 'w')
        return True

    else:
        print("Username already taken")
        return False

def login(user_info: dict):
    """
        Asks the user for a username and password (in the console) and stores
        his login at an externally-defined dictionary
    """
    print("Login: ")
    username = input("\tEnter Username: ")
    password = input("\tEnter Password: ")
    userbase = get_user_data()

    if (username, password) in userbase.items():
        user_info.clear()  # Clears previous login
        user_info['User'] = username
        fetch_user_info(user_info)

    else:
        print("Invalid login...", end="\n\n")
        login(user_info)


def write_user_data(user_info: dict):
    """
    Updates the user's data file according to the data currently cached in the program.
    """
    user_file = open(f"Users\\{user_info['User']}\\user.data", 'w')
    for label, data in user_info.items():
        user_file.write(f"{label}:{data}\n")


def fetch_user_info(user_info) -> dict:
    """
        Retrieves a user's data from the filesystem
    """
    lines = open(f"Users\\{user_info['User']}\\user.data", 'r').readlines()
    for line in lines:
        [label, data] = line.split(":")
        user_info[label] = data.strip("\n").strip()
