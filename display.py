import welcome
import user
import os
import time
import day_tracking
import food
import fitness_calc


def main_menu(user_info):
    print("Welcome to FITBEST!")
    print("What would you like to do?")
    print("\t1. Sign Up")
    print("\t2. Login")
    print("\t3. Exit")
    choice = input("\t> ")
    if choice == '1':
        user.signup()
        print("Sign up complete...")
        time.sleep(5)
        # os.system("cls")
        main_menu(user_info)
    elif choice == '2':
        user.login(user_info)
        user.fetch_user_info(user_info)
        if len(user_info) == 1:
            welcome.new_user_data(user_info)
    else:
        print("Invalid Output...")
        main_menu(user_info)
    return


def display_food(name, counter):
    food_data = food.get_food_data(name)
    calories, unit = food_data["Unit Calorie"], food_data["Unit"]
    print("{0}-{1} ({2} calories per {3}".format(counter, name, calories, unit))


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
        return None


def add_food_menu(user_info):
    food_name = search_food_menu(user_info)
    food_data = food.get_food_data(food_name)
    amount = float(input("Amount (in {0}): ".format(food_data["Unit"])))
    day_tracking.add_food_to_set_date(food_name, amount, "Breakfast", user_info)  # have user choose mode later


def add_weight_menu(user_info):
    weight = float(fitness_calc.lexical_metric_conversion(input("Record your weight today: ")))
    day_tracking.add_new_weight(weight, user_info)


def weight_menu(user_info):
    print("Weight Menu:")
    print("What would you like to do?")
    print("Set Date: {0}".format(day_tracking.get_set_date_text()))
    print("\t1. Add new weight recording to this date.")
    print("\tX. Go back")
    choice = input("\t>")
    if choice == '1':
        add_weight_menu(user_info)
    elif choice == 'X':
        user_menu(user_info)


def food_menu(user_info):
    _,food_data = day_tracking._get_date_data(user_info)
    counter = 1
    print("Max Calories: {0:.2f}".format(day_tracking.get_allowed_calories_today(user_info)))
    for name, params in food_data.items():
        calorie_amount = food.get_calorie(name, float(params["Amount"]))
        print("{0}. {1} | {2} | {3}".format(counter, name, params["Amount"], calorie_amount))
        counter += 1
    print("Food Menu:")
    print("What would you like to do?")
    print("\t 1. Add New Food")
    print("\t X. Go Back")
    choice = input("\t> ")
    if choice == '1':
        add_food_menu(user_info)
    elif choice == 'X':
        user_menu(user_info)
    else:
        print("Invalid choice")
        food_menu(user_info)


def change_date_menu(user_info):
    date = input("Type in the new date: ")
    try:
        new_date = day_tracking.create_date(date)
        day_tracking.change_set_date_with_datetime(new_date)
        user_menu(user_info)
    except ValueError:
        print("Invalid date.")
        change_date_menu(user_info)


def user_menu(user_info):
    print("Hello, {0}".format(user_info["User"]))
    print("What would you like to do?")
    print(">> Current Viewing Date: {0}".format(day_tracking.get_set_date_text()))
    print("\t1. Check Food Balance")
    print("\t2. Add New Food")
    print("\t3. Record New Weight")
    print("\t4.Change Personal Info")
    print("\t5. Check another date.")
    choice = input("\t> ")
    if choice == '1':
        food_menu(user_info)
    elif choice == '2':
        add_food_menu(user_info)
    elif choice == '3':
        weight_menu(user_info)
    elif choice == '4':
        welcome.new_user_data(user_info)
    elif choice == '5':
        change_date_menu(user_info)
    else:
        print("Invalid choice.")
        user_menu(user_info)

