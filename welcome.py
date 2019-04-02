from fitness_calc import *
from user import write_user_data
import day_tracking
from functools import wraps
import os
import time


def clear_screen(menu_func):
    @wraps(menu_func)
    def clear_wrapper(*args, **kwargs):
        os.system("cls")
        time.sleep(2)
        return menu_func(*args, **kwargs)
    return clear_wrapper


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
    if  sex == 'M' or sex == 'F':
        return sex
    else:
        print("Invalid Sex")
        return input_sex()

def input_desired_weight(message, errormsg, weight):
    desired_weight = lexical_metric_conversion(input(message))
    if float(weight) < float(desired_weight) or float(desired_weight) < 0:
        print(errormsg)
        return input_desired_weight(message, errormsg, weight)
    return desired_weight


@clear_screen
def new_user_data(user_info):
    print("Edit Your Data:")
    print("Please add the proper units to your height and weight")
    try:
        height = lexical_metric_conversion(input("What is your height: "))
        if float(height) < 0:
            print("Error: Invalid Height")
            time.sleep(3)
            new_user_data(user_info)
            return
        print("Height converted to: {0} meters".format(height))
        weight = lexical_metric_conversion(input("What is your weight: "))
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
    desired_weight = input_desired_weight("What is your desired weight (add unit): ", "Weight must be lesser than your actual weight.", weight)
    date = input_date("When do you want to achieve this? (mm/dd/YYYY)", "Invalid Date")
    user_info['Weight'] = weight
    user_info['Height'] = height
    user_info['Sex'] = sex
    user_info['Age'] = age
    user_info['BMI'] = calculate_bmi(weight, height)
    user_info['BMR'] = calculate_bmr(weight, height, sex, age)
    user_info['Desired Weight'] = desired_weight
    user_info['Goal Date'] = date
    write_user_data(user_info)

