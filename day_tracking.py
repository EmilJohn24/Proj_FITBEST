import food
import datetime
_set_date = datetime.datetime.now()
"""
    Foodfile Format:
    food_name,mode
    [Separated by a comma]
    mode is an element of {Breakfast, Lunch, Dinner, Snacks}

"""
def change_set_date(year, month, day):
    global _set_date
    _set_date = datetime.datetime(year, month, day)

def get_set_date_text():
    return _set_date.strftime("%Y-%b-%d")

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
    date_file.write(f"{food_name},{amount},{mode}")
    date_file.close()


