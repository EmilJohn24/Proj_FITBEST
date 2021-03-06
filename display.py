import user
import os
import time
import day_tracking
import food
import fitness_calc
from random import randint
from functools import wraps


def display_tip():
    tips = open("tips.txt", 'r').readlines()
    index = randint(0, len(tips) - 1)
    print("Remember:", tips[index])


def clear_screen(menu_func):
    @wraps(menu_func)
    def clear_wrapper(*args, **kwargs):
        os.system("cls")
        display_tip()
        print("Loading...")
        time.sleep(2)
        os.system("cls")
        return menu_func(*args, **kwargs)
    return clear_wrapper


@clear_screen
def main_menu(user_info):
    print("Welcome to FITBEST!")
    print("What would you like to do?")
    print("\t1. Sign Up")
    print("\t2. Login")
    print("\t3. Exit")
    choice = input("\t> ")
    if choice == '1':
        signup()
        print("We're preparing your account...")
        time.sleep(5)
        print("Sign up complete...")
        time.sleep(5)
        main_menu(user_info)
    elif choice == '2':
        login(user_info)
        user.fetch_user_info(user_info)
        if len(user_info) == 1:
            new_user_data(user_info)
    else:
        print("Invalid Output...")
        main_menu(user_info)
    return


@clear_screen
def add_food_to_database(user_info):
    print("What would you like to add,", user_info["User"], '?')
    name = input("Name of the food: ")
    unit = input("Unit of calories: ")
    calorie = float(input("Number of calories per unit: "))
    food.add_food_to_database(name, calorie, unit)
    return name


def display_food(name, counter):
    food_data = food.get_food_data(name)
    calories, unit = food_data["Unit Calorie"], food_data["Unit"]
    print("{0}-{1} ({2} calories per {3}".format(counter, name, calories, unit))


@clear_screen
def search_food_menu(user_info):
    print("Search for food: ", end=" ")
    query = input()
    results = food.search_food(query)
    for index, food_name in enumerate(results):
        display_food(food_name, index + 1)
    if len(results) > 0:
        choice = int(input("Choose a result: "))
        return results[choice - 1]
    else:
        print("No results found.")
        print("Would you like to add this do our database? (Y/N)")
        choice = input("\t>")
        if choice == 'Y':
            return add_food_to_database(user_info)
        elif choice == 'N':
            user_menu(user_info)
        else:
            print("Invalid choice")
            return search_food_menu(user_info)


@clear_screen
def add_food_menu(user_info):
    food_name = search_food_menu(user_info)
    food_data = food.get_food_data(food_name)
    print("Adding {0}".format(food_name))
    amount = float(input("Amount (in {0}): ".format(food_data["Unit"])))
    day_tracking.add_food_to_set_date(food_name, amount, "Breakfast", user_info)  # have user choose mode later


@clear_screen
def add_weight_menu(user_info):
    weight = float(fitness_calc.lexical_metric_conversion(input("Record your weight today: ")))
    day_tracking.add_new_weight(weight, user_info)
    user_menu(user_info)


@clear_screen
def weight_menu(user_info):
    print("Weight Menu:")
    print("What would you like to do?")
    print("Set Date: {0}".format(day_tracking.get_set_date_text()))
    latest_weight, _ = day_tracking.get_date_data(user_info)
    print("\tRecorded Weight on Set Date: {0}".format(latest_weight))
    print("\t1. Add new weight recording to this date.")
    print("\tX. Go back")
    choice = input("\t>")
    if choice == '1':
        add_weight_menu(user_info)
    elif choice == 'X':
        user_menu(user_info)


@clear_screen
def display_info(user_info):
    side_by_side = False
    for label, info in user_info.items():
        if side_by_side:
            label_end = '\t|\t'
        else:
            label_end = '\n'

        print(f"{label}: {info[0:10]:<30}", end=label_end)
        side_by_side = not side_by_side


@clear_screen
def recommender(user_info):
    food_base = food.load_food()
    print("The FITBEST algorithm recommends the following food: ")
    recommendations = food.get_recommendations(user_info, 10)
    for recommendation in recommendations:
        food_data = food_base[recommendation]
        print(">> {0}: {1} calories per {2} [{3}]".format(
            recommendation, food_data["Unit Calorie"], food_data["Unit"], food_data["Mode"]))
    _ = input("Press enter to leave...")
    return


@clear_screen
def remove_food_menu(user_info):
    food_data_loaded = False
    try:
        _, food_data = day_tracking._get_date_data(user_info)
        food_data_loaded = True
    except FileNotFoundError:
        print("No food to display...")
    if food_data_loaded:
        names = []
        counter = 1
        for named, params in food_data.items():
            calorie_amount = food.get_calorie(named, float(params["Amount"]))
            print("{0}. {1} | {2} | {3}".format(counter, named, params["Amount"], calorie_amount))
            names.append(named)
            counter += 1
        choice = input("Pick the number of the item you would like removed: ")
        try:
            day_tracking.remove_food_from_set_date(names[int(choice) - 1], user_info)
        except KeyError:
            print("Invalid choice...")
            time.sleep(2)
            remove_food_menu(user_info)


@clear_screen
def food_menu(user_info):
    food_data_loaded = False
    try:
        _, food_data = day_tracking._get_date_data(user_info)
        food_data_loaded = True
    except FileNotFoundError:
        print("No food to display...")
    counter = 1
    print("Max Calories: {0:.2f}".format(day_tracking.get_allowed_calories_today(user_info)))
    if food_data_loaded:
        remaining_calories = day_tracking.get_remaining_calories_today(user_info)
        print("Remaining Calories: {0:.2f}".format(remaining_calories))
        if remaining_calories < 0:
            print("\tStop Eating!!! You're out of calories today, but I'm not gonna stop you.")
        for name, params in food_data.items():
            calorie_amount = food.get_calorie(name, float(params["Amount"]))
            print("{0}. {1} | {2} | {3}".format(counter, name, params["Amount"], calorie_amount))
            counter += 1
        print("Food Menu:")
        print("What would you like to do?")
        print("\t 1. Add New Food")
        print("\t 2. Get some recommendations")
        print("\t 3. Remove New Food")
        print("\t X. Go Back")
        choice = input("\t> ")
        if choice == '1':
            add_food_menu(user_info)
        elif choice == '2':
            recommender(user_info)
        elif choice == '3':
            remove_food_menu(user_info)
        elif choice == 'X':
            user_menu(user_info)
        else:
            print("Invalid choice")
            food_menu(user_info)
    else:
        print("No food to display.")
    user_menu(user_info)


def change_date_menu(user_info):
    date = input("Type in the new date (type 'now' to return to current date): ")
    if date == 'now':
        day_tracking.snap_date_to_now()
    else:
        try:
            new_date = day_tracking.create_date(date)
            day_tracking.change_set_date_with_datetime(new_date)
        except ValueError:
            print("Invalid date.")
            change_date_menu(user_info)
    user_menu(user_info)


def signup():
    print("Sign Up: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    if not user.create_account(username, password):
        print("Username already taken")
        signup()
    return


def login(user_info: dict):
    """
        Asks the user for a username and password (in the console) and stores
        his login at an externally-defined dictionary
    """
    print("Login: ")
    username = input("\tEnter Username: ")
    password = input("\tEnter Password: ")
    userbase = user.get_user_data()

    if (username, password) in userbase.items():
        user_info.clear()  # Clears previous login
        user_info['User'] = username
        user.fetch_user_info(user_info)

    else:
        print("Invalid login...", end="\n\n")
        login(user_info)


@clear_screen
def user_menu(user_info):
    user.fetch_user_info(user_info)
    print("Hello, {0}".format(user_info["User"]))
    display_info(user_info)
    print("What would you like to do?")
    print(">> Current Viewing Date: {0}".format(day_tracking.get_set_date_text()))
    print("\t1. Check Food Balance")
    print("\t2. Add New Food")
    print("\t3. Record New Weight")
    print("\t4. Change All Personal Info")
    print("\t5. Check another date.")
    print("\tX. Exit")
    choice = input("\t> ")
    if choice == '1':
        food_menu(user_info)
    elif choice == '2':
        add_food_menu(user_info)
    elif choice == '3':
        weight_menu(user_info)
    elif choice == '4':
        new_user_data(user_info)
    elif choice == '5':
        change_date_menu(user_info)
    elif choice == 'X':
        exit()
    else:
        print("Invalid choice.")
        user_menu(user_info)
    user_menu(user_info)


"""
Functions from welcome.py
"""


def input_date(prompt, error_msg):
    date = input(prompt)
    try:
        day_tracking.create_date(date)
    except ValueError:
        print(error_msg)
        return input_date(prompt, error_msg)
    return date


def input_age(prompt, error_msg):
    try:
        age = int(input(prompt))
        if age > 100 or age < 0:
            raise ValueError()
        return age
    except ValueError:
        print(error_msg)
        return input_age(prompt, error_msg)


def input_sex():
    sex = input("What is your sex (M/F)?")
    if sex == 'M' or sex == 'F':
        return sex
    else:
        print("Invalid Sex")
        return input_sex()


def input_desired_weight(message, errormsg, weight):
    desired_weight = fitness_calc.lexical_metric_conversion(input(message))
    if float(weight) < float(desired_weight) or float(desired_weight) < 0:
        print(errormsg)
        return input_desired_weight(message, errormsg, weight)
    return desired_weight


@clear_screen
def new_user_data(user_info):
    print("Edit Your Data:")
    print("Please add the proper units to your height and weight")
    try:
        height = fitness_calc.lexical_metric_conversion(input("What is your height: "))
        if float(height) < 0:
            print("Error: Invalid Height")
            time.sleep(3)
            new_user_data(user_info)
            return
        print("Height converted to: {0} meters".format(height))
        weight = fitness_calc.lexical_metric_conversion(input("What is your weight: "))
        if float(weight) < 0:
            print("Error: Invalid Weight")
            time.sleep(3)
            new_user_data(user_info)
            return
    except KeyError:
        print("Invalid value inputted...")
        time.sleep(3)
        new_user_data(user_info)
        return
    print("Weight converted to: {0} kg".format(weight))
    sex = input_sex()
    age = input_age("What is your age?", "Invalid age")

    os.system('start "C:\Program Files (x86)\Google\
                Chrome\Application\chrome.exe" https://www.vertex42.com/ExcelTemplates/Images/body-mass-index-chart.gif')
    print("Use the image as a guide...")
    desired_weight = input_desired_weight("What is your desired weight (add unit): ",
                                          "Weight must be lesser than your actual weight.", weight)
    date = input_date("When do you want to achieve this? (mm/dd/YYYY)", "Invalid Date")
    user_info['Weight'] = weight
    user_info['Height'] = height
    user_info['Sex'] = sex
    user_info['Age'] = age
    user_info['BMI'] = fitness_calc.calculate_bmi(weight, height)
    user_info['BMR'] = fitness_calc.calculate_bmr(weight, height, sex, age)
    user_info['Desired Weight'] = desired_weight
    user_info['Goal Date'] = date
    user.write_user_data(user_info)
