'''
Nucamp
Darren Zhang
Added a database to store bank information using sqlite3
Added method to register and log out and log in
'''

from banking_pkg import account
import sys
import sqlite3

connection = sqlite3.connect('accounts.db')
c = connection.cursor()


def table_exists(table_name):
    c.execute(
        "SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{}' ".format(table_name))
    if c.fetchone()[0] == 1:
        return True
    return False


def welcome():
    print('Welcome to Nu Bank')
    print("--------------------------------------------------------------------")
    print("| 1.    Login      | 2.      Register      |3        Quit         | ")
    print("--------------------------------------------------------------------")

    menu1 = input('Would you like to login or create a new account? ')
    if menu1 == '1':
        name = account.login()
        return name
    elif menu1 == '2':
        name = account.register()
        return name
    elif menu1 == '3':
        sys.exit("Bank's closing...apparently.\n")
    else:
        print('Select a valid option\n')
        welcome()


def atm_menu():
    print("")
    print("      === Automated Teller Machine ===          ")
    print("--------------------------------------------")
    print("| 1.    Balance      | 2.     Deposit      |")
    print("--------------------------------------------")
    print("--------------------------------------------")
    print("| 3.    Withdraw     | 4.     Logout       |")
    print("--------------------------------------------")


def menu(user, balance):
    while True:
        atm_menu()
        option = input('Choose an option: ')
        print('\n')

        if option == '1':
            account.show_balance(user)
        elif option == '2':
            account.deposit(user, balance)
        elif option == '3':
            account.withdraw(user, balance)
        elif option == '4':
            account.logout(user)
            break
        else:
            print('Invalid option.\n')
            continue


if not table_exists('accounts'):
    c.execute('''
        CREATE TABLE accounts(
            username STRING,
            pin STRING,
            balance FLOAT
        )
    ''')

all_accounts = account.get_all_accounts()

while True:
    name = welcome()
    your_account = account.get_account(name)
    balance = 0
    menu(name, balance)
