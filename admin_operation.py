import json


def remove_user(user_to_be_deleted: str, bank_path: str = "bank.json", auth_path: str = "auth.json" , clients_path: str = "clients.json"):
    # here I changed
    paths = [bank_path, auth_path, clients_path]
    data = {}
    try:
        for path in paths:
            with open(path, "r") as f:
                data[path] = json.load(f)
        for path in paths:
            data[path].pop(user_to_be_deleted, None)
        for path in paths:
            with open(path, "w") as f:
                json.dump(data[path], f, indent=4)

    except Exception as e:
        print(f"Error: {e}")


# Admin case 2
def add_new_client(clients_path = "clients.json", bank_path = "bank.json"):
    username = input("Enter the new client username: ")

    with open(clients_path, "r") as f:
        clients = json.loads(f.read())

    if username in clients:
        print("The user already exists!")
        return

    passwd = input("Enter the new client password: ")
    phone_number = input("Enter the new client phone number: ")

    clients[username] = {
        "password": passwd,
        "telefon": phone_number
    }

    with open(clients_path, "w") as f:
        f.write(json.dumps(clients, indent=4))

    initial_balance = 0
    currency = input("Enter the new user currency: ")

    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    accounts[username] = {
        "value": initial_balance,
        "currency": currency
    }

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    print(f"The client{username} has been successfully added")
