import welcome
import user
import os
import time
import day_tracking


def main_menu(user_info):
    print("Welcome to FITBEST!")
    print("What would you like to do?")
    print("\t1. Sign Up")
    print("\t2. Login")
    print("\t3. Exit")
    choice = input("\t> ")
    if choice == '1':
        user.signup()
        welcome.new_user_data(user_info)
        print("Sign up complete...")
        time.sleep(5)
        # os.system("cls")
        main_menu(user_info)
    elif choice == '2':
        user.login(user_info)
    else:
        print("Invalid Output...")
        main_menu(user_info)
    return


def user_menu(user_info):
    print("Hello, {0}".format(user_info["User"]))
    print("What would you like to do?")
    print(">> Current Date: {0}".format(day_tracking.get_set_date_text()))
    print("\t1. Check Food Balance")
    print("\t2. Add New Food")
    print("\t3.Change Personal Info")
    choice = input("\t> ")

