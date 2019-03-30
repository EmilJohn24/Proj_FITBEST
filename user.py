import os

conversion_lexicon = {
    'lb': 0.45,
    'ft': 0.3,
    "'" : 0.3,
    '"': 0.00393700787,
    'in': 0.00393700787
}


def lexical_metric_conversion(value: str):
    tokens = []
    running_digit = ""
    running_unit = ""
    # Split value to token
    for c in value:
        if c.isdigit() or c == '.':
            running_digit += c
            if len(running_unit) > 0:
                tokens.append(running_unit)
        else:
            running_unit += c
            if len(running_digit) > 0:
                tokens.append(float(running_digit))

    for index, token in enumerate(tokens):
        if isinstance(token, str):
            tokens[index - 1] *= conversion_lexicon[token]
            del tokens[index]
    return str(sum(tokens))


def get_user_data():
    users = open('user.txt', 'r').readlines()
    userbase = dict()
    for user in users:
        data = user.split(',')
        userbase[data[0]] = data[1]
    return userbase


def signup():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    users = open('user.txt', 'a')
    userbase = get_user_data()
    if username not in userbase.keys():
        users.write("\n{0},{1}".format(username, password))
        os.system(f"mkdir Users\\{username}")
    else:
        print("Username already taken")
        signup()


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
    user_file = open(f"Users\\{user_info['User']}", 'w')
    for label, data in user_info.items():
        user_file.write(f"{label}:{data}")


def fetch_user_info(username):
    lines = open(f"Users\\{username}", 'r').readlines()
    user_info = {}
    for line in lines:
        [label, data] = line.split(":")
        user_info[label] = data
    return user_info
