from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):

        if not len(str(value)) == 10 or not str(value).isdigit():
            raise ValueError

        super().__init__(value)


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = [phone] if phone else []

    def add_phone(self, phone):

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):

        for p in self.phones:
            if str(p.value) == phone:
                index = self.phones.index(p)
                self.phones.pop(index)
                return f'Contact number {self.name} {phone} has been deleted'
            else:
                return f'Contact {self.name} does not have a number {phone}'

    def edit_phone(self, old_phone, new_phone):

        for p in self.phones:
            if str(p.value) == old_phone:
                index = self.phones.index(p)
                self.phones[index] = Phone(new_phone)
                return f'Сontact number {self.name.value} {old_phone} has been changed to: {new_phone}'
            else:
                raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join([str(p.value) for p in self.phones])}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        try:
            self.data.pop(name)
        except KeyError:
            return 'You have no contacts with this name'


book = AddressBook()


def input_error(func):
    def inner(*args):

        try:
            return func(*args)
        except IndexError:
            return 'Not enough params'
        except KeyError:
            return 'You have no contacts with this name'
        except ValueError:
            return 'You entered incorrect data'

    return inner


def hello(*args):
    return 'How can I help you?'


@input_error
def add_contact(*args):

    name = Name(args[0])

    if name.value in book:

        try:
            phone = Phone(args[1])
            book[name.value].add_phone(phone)
            return f'A contact with the name {name.value} and number: {phone.value} has been added'
        except IndexError:
            return f'A contact with the name {name.value} already exists'

    else:
        book[name.value] = Record(name)
        try:
            phone = Phone(args[1])
            book[name.value].add_phone(phone)
            return f'A contact with the name {name.value} and number: {phone.value} has been added'
        except IndexError:
            return f'A contact with the name {name.value} has been added'


@input_error
def change(*args):

    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    record = book.get(name)
    if record:
        message = record.edit_phone(old_phone, new_phone)
        return message
    else:
        raise KeyError


@input_error
def phone(*args):
    name = args[0]
    record = book.get(name)
    if record:
        return record
    else:
        return f'You have no contacts with this name'


@input_error
def show_all(*args):
    all_contacts = ''
    for name, record in book.data.items():
        all_contacts += f'{record}\n'
    return all_contacts.strip()


@input_error
def delete_contact(*args):
    name = args[0]
    book.delete(name)
    return f'Сontact with the name {name} has been deleted'


@input_error
def remove_phone(*args):
    name = args[0]
    phone = args[1]
    record = book.get(name)

    if record:
        message = record.remove_phone(phone)
        return message
    else:
        return f'You have no contacts with this name'


def close(*args):
    return 'Good bye!'


def no_command(*args):
    return 'Unknown command'


COMMANDS = {
    hello: ['hello'],
    add_contact: ['add'],
    change: ['change'],
    phone: ['phone'],
    show_all: ['show_all', 'show'],
    close: ['good bye', 'close', 'exit', '.', 'good'],
    delete_contact: ['delete_contact', 'delete'],
    remove_phone: ['remove_phone', 'remove']

}


@input_error
def get_handler(command):

    for func, k_words in COMMANDS.items():
        for word in k_words:
            if command.startswith(word):
                return func

    return no_command


def main():

    while True:

        user_input = input('>>> ')

        if not user_input:
            continue

        input_list = user_input.split()

        command = input_list[0].lower()
        data = input_list[1:]

        function = get_handler(command)
        print(function(*data))

        if function.__name__ == 'close':
            break


if __name__ == '__main__':
    main()
