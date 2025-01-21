import json
import os
import time

import admin_operation
from admin_operation import add_new_client

OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Here I changed colors
USER_MENU = f"""
{ENDC}{BOLD}1.{ENDC} Sa ceara bank statement -> valoare contului
{WARNING}{BOLD}2.{ENDC} Sa transfere unui alt utilizator
{OKCYAN}{BOLD}3.{ENDC} Sa scoata bani din cont
{OKGREEN}{BOLD}4.{ENDC} Sa adauge bani in cont
{OKBLUE}{BOLD}5.{ENDC} Sa converteasca banii
{UNDERLINE}{BOLD}6.{ENDC} Sign out
{FAIL}{BOLD}7.{ENDC} Exit

{OKCYAN}Type in choice:{ENDC} """

ADMIN_MENU = f"""
{FAIL}{BOLD}1.{ENDC} Sa se stearga clientul (admin-only)
{OKBLUE}{BOLD}2.{ENDC} Sa adauge un client nou (admin-only)
{OKCYAN}{BOLD}3.{ENDC} Sign out
{OKGREEN}{BOLD}4.{ENDC} Show users
{WARNING}{BOLD}5.{ENDC} Exit
"""


# ENVIRONMENT VARIABLE

# print(os.environ['admin_bank'])

def login(user: str, auth_path: str = "auth.json") -> str:
    if user == "admin":
        for _ in range(3):
            passwd = input("Type in password: ")
            if passwd == os.environ['admin_bank']:
                return user
        return ""
    else:
        with open(auth_path, "r") as e:
            credentials = json.loads(e.read())

        while user not in credentials:
            print("User not found in database.")
            user = input("Type in user:")

        # passwd = pwinput.pwinput(prompt='PW: ', mask='*')
        passwd = input("Citeste parola: ")

        while passwd != credentials[user]:
            passwd = input("Wrong password: ")

        return user


def account_balance(user: str, bank_path: str = "bank.json") -> str:
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())
    # un comentariu aici
    value = accounts[user]["value"]
    currency = accounts[user]["currency"]

    return f"Your account is worth : {value} {currency}"


def convert_account(user: str, to_currency: str, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    account = accounts[user]
    account["value"] = convert_currency(account['value'], account["currency"], to_currency)
    account["currency"] = to_currency

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    # return "Account converted from x to y"


def convert_currency(amount: int, from_currency: str, to_currency: str, currencies_json="currencies.json") -> int:
    with open(currencies_json, "r") as f:
        conversion_rates = json.loads(f.read())

    amount = amount * conversion_rates[from_currency][to_currency]

    return amount


def transfer_money(sender: str, receiver: str, amount: int, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    if amount <= accounts[sender]["value"]:
        if accounts[sender]["currency"] == accounts[receiver]["currency"]:
            accounts[receiver]["value"] += amount
            accounts[sender]["value"] -= amount
        else:
            amount_receiver_currency = convert_currency(amount, accounts[sender]["currency"],
                                                        accounts[receiver]["currency"])
            accounts[receiver]["value"] += amount_receiver_currency
            accounts[sender]["value"] -= amount

        with open(bank_path, "w") as f:
            f.write(json.dumps(accounts, indent=4))

        print(f"Ati transferat cu succes. Cont curent: {accounts[sender]['value']} {accounts[sender]['currency']} ")



    else:
        print("Not enough money to send")


def get_username_by_phone(phone_number: str, clients_path: str = "clients.json"):
    with open(clients_path, "r") as f:
        clients = json.loads(f.read())

    for user_id, details in clients.items():
        if details['telefon'] == phone_number:
            return user_id

    print("Phone number not recognised!")
    return None


# Here I did case 3
def withdraw_money(user: str,amount: int, bank_path: str = "bank.json" ):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    if amount <= accounts[user]["value"]:
        accounts[user]["value"] -= amount
        with open(bank_path, "w") as f:
            f.write(json.dumps(accounts, indent=4))
        print(
            f"Ati retras {amount} {accounts[user]['currency']}. Cont curent: {accounts[user]['value']} {accounts[user]['currency']}.")
    else:
        print("Fonduri insuficiente pentru retragere.")

# Here I did case 4
def deposit_money(user: str, amount: int, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    accounts[user]["value"] += amount
    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    print(f"Ati adaugat {amount} {accounts[user]['currency']} in contul dumneavoastra. "
          f"Cont curent: {accounts[user]['value']} {accounts[user]['currency']}.")






if __name__ == '__main__':
    username = input("Please enter your username: ")
    username = login(username)
    menu = USER_MENU if username != "admin" else ADMIN_MENU

    user_pick = input(menu)

    while True:
        if username != "admin":
            match user_pick:
                case "1":
                    print(account_balance(username))
                case "2":
                    amount = int(input("Citeste de la tastatura suma de bani in valuta personala: "))
                    phone_number = input("Cui vrei sa ii trimiti bani? Introdu numarul de telefon ")
                    receiver_id = get_username_by_phone(phone_number)
                    if receiver_id:
                        transfer_money(username, receiver_id, amount)

                # Updated case 3
                case "3":
                    amount = int(input("Citeste suma de bani pe care doresti sa o retragi: "))
                    withdraw_money(username, amount)
                # Updated case 4
                case "4":
                    amount = int(input("Citeste suma de bani pe care doresti sa o depui: "))
                    deposit_money(username, amount)
                case "5":
                    currency = input("Ce vrei sa transformi? ")
                    # verificati sa fie currency corect
                    convert_account(username, currency)
                case "6":
                    username = input("Citeste un nou user: ")
                    username = login(username)
                case "7":
                    exit(0)
                case "8":
                    pass
                case _:
                    pass
            time.sleep(3)
            menu = USER_MENU if username != "admin" else ADMIN_MENU
            user_pick = input(menu)
        else:
            match user_pick:
                case "1":
                    user_to_delete = input("Ce user doresti sa stergi? ")
                    admin_operation.remove_user(user_to_delete)
                # Updated case 2
                case "2":
                    add_new_client()
                case "3":
                    username = input("Citeste un nou user: ")
                    username = login(username)
                case "4":
                    with open("bank.json", "r") as f:
                        print(f.read())
                case "5":
                    # option 1
                    # break
                    exit(0)

            time.sleep(3)
            menu = USER_MENU if username != "admin" else ADMIN_MENU
            user_pick = input(menu)