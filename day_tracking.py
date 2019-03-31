import food
import datetime
_set_date = datetime.datetime.now()
"""
    Food file Format:
    type:food_name,amount,mode
    [Separated by a comma]
    mode is an element of {Breakfast, Lunch, Dinner, Snacks}
    type is either food or weight
"""

def create_date(date_input):
    return datetime.strptime(date_input, "%b/%d/%Y")

def snap_date_to_now():
    global _set_date
    _set_date = datetime.datetime.now()


def change_set_date(year, month, day):
    global _set_date
    _set_date = datetime.datetime(year, month, day)


def get_set_date_text():
    global _set_date
    return _set_date.strftime("%Y-%b-%d")


def get_time_text():
    global _set_date
    return _set_date.strftime("%H:%M:%S")


def access_date_file(user_info, file_mode):
    username = user_info['User']
    date_str = get_set_date_text()
    date_file = "Users\\{0}\\{1}.data".format(username, date_str)
    return open(date_file, file_mode)


def add_food_to_set_date(food_name, amount, mode, user_info):
    """
        food_name: refers to the name of the food as specified by food_dict
        mode: Breakfast, Lunch, Dinner, Snacks
        amount: amount of food (according to the unit in the database
    """
    date_file = access_date_file(user_info, 'a')
    date_file.write(f"food:{food_name},{amount},{mode}")
    date_file.close()


def add_new_weight(weight, user_info):
    """
    Adds new weight record on current set date
    :param weight:
    :param user_info:
    :return:
    """
    date_file = access_date_file(user_info, 'a')
    snap_date_to_now()
    date_file.write(f"weight:{weight}")


def _get_date_data(user_info):
    date_file = access_date_file(user_info, 'r')
    data_col = date_file.readlines()
    food_list = []
    weight = int()
    for line in data_col:
        data_type, data = line.split(':')
        if data_type == "weight":
            weight = float(data)
        elif data_type == "food":
            food_list.append(data)
    return weight, food_list


def get_allowed_calories_today(user_info):
    """
        Gets the maximum allowable number of calories for current set date
    """
    global _set_date
    weight, _ = _get_date_data(user_info)
    goal_date = create_date(user_info["Goal Date"])
    BMR = float(user_info["BMR"])
    date_diff = goal_date - _set_date
    days_diff = date_diff.days


