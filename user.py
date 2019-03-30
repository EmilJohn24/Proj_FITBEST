import os


def get_user_data():
    users = open('user.txt', 'r').readlines()
    userbase = dict()
    for user in users:
        user = user.strip('\n')
        data = user.split(',')
        userbase[data[0]] = data[1]
    return userbase


def signup():
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
        return True

    else:
        print("Username already taken")
        return False


def login(user_info):
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    userbase = get_user_data()

    if (username, password) in userbase.items():
        user_info['User'] = username
    else:
        print("Invalid login")
        login(user_info)


def write_user_data(user_info):
    user_file = open(f"Users\\{user_info['User']}\\user.data", 'w')
    for label,data in user_info.items():
        user_file.write(f"{label}:{data}\n")


def fetch_user_info(username):
    lines = open(f"Users\\{username}\\user.data", 'r').readlines()
    user_info = {}
    for line in lines:
        [label, data] = line.split(":")
        user_info[label] = data
    return user_info
