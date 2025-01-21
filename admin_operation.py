import json


def remove_user(user_to_be_deleted: str, bank_path: str = "bank.json", auth_path: str = "auth.json" , clients_path: str = "clients.json"):
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



