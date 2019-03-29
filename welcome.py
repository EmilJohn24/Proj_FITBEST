from fitness_calc import *
import os

def new_user_data(user_info):
    height = lexical_metric_conversion(input("What is your height: "))
    weight = lexical_metric_conversion(input("What is your weight: "))
    sex = input("What is your sex(M/F): ")
    age = input("What is your age: ")
    os.system('start "C:\Program Files (x86)\Google\
                Chrome\Application\chrome.exe" https://www.vertex42.com/ExcelTemplates/Images/body-mass-index-chart.gif')
    print("Use the image as a guide...")
    desired_weight = int(input("What is your desired weight: "))
    user_info['Weight'] = weight
    user_info['Height'] = height
    user_info['Sex'] = sex
    user_info['Age'] = age
    user_info['BMI'] = calculate_bmi(weight, height)
    user_info['BMR'] = calculate_bmr(weight, height, age, sex)
    user_info['DesiredWeight'] = desired_weight