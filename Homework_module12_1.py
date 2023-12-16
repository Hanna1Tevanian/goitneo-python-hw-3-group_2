from datetime import datetime, timedelta
from collections import UserDict, defaultdict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate_format(self):
        if not (isinstance(self.value, str) and self.value.isdigit() and len(self.value) == 10):
            raise ValueError("Invalid phone number format")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone.validate_format()
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                phone.validate_format()

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner

@input_error
def add_contact(contacts, username, phone):
    contacts[username] = phone
    return "Contact added."

@input_error
def change_contact(contacts, username, new_phone):
    if username in contacts:
        contacts[username] = new_phone
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(contacts, username):
    if username in contacts:
        return f"Phone number for {username}: {contacts[username]}"
    else:
        return "Contact not found."

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    else:
        result = "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
        return result

class BirthdayAssistant:
    def __init__(self):
        self.users = []

    def add_user(self, name, birthday):
        self.users.append({"name": name, "birthday": birthday})

    def find_user(self, name):
        for user in self.users:
            if user["name"] == name:
                return user
        return None

    def get_birthdays_per_week(self):
        birthday_d = defaultdict(list)

        today = datetime.today().date()

        for user in self.users:
            name = user["name"]
            birthday = user["birthday"].date()
            birthday_year = birthday.replace(year=today.year)

            if birthday_year < today:
                birthday_year = birthday_year.replace(year=today.year + 1)

            delta_days = (birthday_year - today).days

            if delta_days < 7:
                day_week = (today + timedelta(days=delta_days)).strftime("%A")
            else:
                continue

            birthday_d[day_week].append(name)

        for day, names in birthday_d.items():
            print(f"{day}: {', '.join(names)}")

@input_error
def add_birthday(assistant, name, birthday_str):
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
    assistant.add_user(name, birthday)
    return "Birthday added."

@input_error
def show_birthday(assistant, name):
    user = assistant.find_user(name)
    if user:
        return f"{name}'s birthday: {user['birthday'].strftime('%Y-%m-%d')}"
    else:
        return "User not found."

@input_error
def show_birthdays_next_week(assistant):
    assistant.get_birthdays_per_week()
    return "Birthdays for the next week displayed."

def main():
    contacts = {}
    birthday_assistant = BirthdayAssistant()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add" and len(args) == 2:
            username, phone = args
            print(add_contact(contacts, username, phone))
        elif command == "change" and len(args) == 2:
            username, new_phone = args
            print(change_contact(contacts, username, new_phone))
        elif command == "phone" and len(args) == 1:
            username = args[0]
            print(show_phone(contacts, username))
        elif command == "all" and not args:
            print(show_all(contacts))
        elif command == "add-birthday" and len(args) == 2:
            name, birthday_str = args
            print(add_birthday(birthday_assistant, name, birthday_str))
        elif command == "show-birthday" and len(args) == 1:
            name = args[0]
            print(show_birthday(birthday_assistant, name))
        elif command == "birthdays" and not args:
            print(show_birthdays_next_week(birthday_assistant))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

