import sys
import sqlite3

connection = sqlite3.connect('accounts.db')
c = connection.cursor()
autocommit = True


def get_all_names():
    names = [name[0] for name in c.execute("SELECT username FROM accounts")]

    return names


def table_exists(table_name):
    c.execute(
        "SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{}' ".format(table_name))
    if c.fetchone()[0] == 1:
        return True
    return False


if not table_exists('accounts'):
    c.execute('''
        CREATE TABLE accounts(
            username STRING,
            pin STRING,
            balance FLOAT
        )
    ''')


def new_account(username, pin, balance):
    params = (username, pin, balance)
    c.execute("INSERT INTO accounts VALUES (?, ?, ?)", (params))
    connection.commit()


def get_account(username):
    c.execute("SELECT * FROM accounts WHERE username = '{}'".format(username))
    accounts = []
    for row in c.fetchall():
        accounts.append(row)
    return accounts


def get_all_accounts():
    c.execute("SELECT * FROM accounts")
    data = []
    for row in c.fetchall():
        data.append(row)
    return data


def update_account(username, change):
    valid_keys = ['pin', 'balance']
    for key in change.keys():
        if key not in valid_keys:
            raise Exception('Unable to change this field!')
    for key in change.keys():
        if type(change[key]) == float:
            change_statement = "UPDATE accounts SET {} = '{}' WHERE username = '{}' ".format(
                key, change[key], username)
        c.execute(change_statement)
    connection.commit()


def show_balance(user):
    your_account = get_account(user)
    print('Current Balance: ${0:.2f}'.format(your_account[0][2]))


def deposit(user, balance):
    your_account = get_account(user)
    balance = your_account[0][2]

    amount = input('Enter amount to deposit: ')
    update_account(user, {'balance': (balance + float(amount))})

    print('Current Balance: ${0:.2f}'.format(balance + float(amount)))

    return balance


def withdraw(user, balance):
    your_account = get_account(user)
    balance = your_account[0][2]

    amount = input('Enter amount to withdraw: ')
    if(float(amount) > balance):
        print('Sir, this is a Wendys, we do not print money')
        withdraw(user, balance)
    else:
        update_account(user, {'balance': (
            your_account[0][2] - float(amount))})
        print('Current Balance: ${0:.2f}'.format(
            your_account[0][2] - float(amount)))

    return balance


def logout(name):
    print('Goodbye {}!\n'.format(name))


def register():
    starting_balance = 0
    registered_names = [name[0]
                        for name in c.execute("SELECT username FROM accounts")]

    while True:
        user = input('Enter name to register: ')
        if user in registered_names:
            print('Username already exists, please try again.')
            continue
        if len(user) >= 1 and len(user) <= 10:
            break
        else:
            print('Please input a name between 1 and 10 characters.\n')
            continue

    while True:
        pin = input('Enter PIN: ')
        if len(pin) == 4:
            break
        else:
            print('Please enter a 4 digit PIN.\n')
            continue

    new_account(user, pin, starting_balance)

    print("{} has been registered with a starting balance of {}\n".format(
        user, starting_balance))

    return user


def login():
    all_names = get_all_names()

    while True:
        print('\nLOGIN')
        name = input('Enter name: ')
        pin = input('Enter PIN: ')
        print('\n')

        if name == '' or pin == '':
            choice = input('Would you like to register instead? Y/N \n')
            if(choice == 'Y'):
                pass
            else:
                sys.exit('Leaving...')
        elif name in all_names:
            your_account = get_account(name)
            if pin == str(your_account[0][1]):
                print('Login successful!')
                print('Welcome {}!\n'.format(name))
            break
        else:
            print('Wrong username or password.\n')
            continue

    return name
