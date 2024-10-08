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
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone format is not correct")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i, p in enumerate(self.phones):
            if p.value == phone:
                del self.phones[i]
                return
        raise ValueError("Phone was not found")
    
    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
            return
        raise ValueError("Phone was not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def __str__(self):
        result = ""
        for name, record in self.items():
            result += str(record) + "\n"
        return result
    
book = AddressBook()

join_record = Record("Join")
join_record.add_phone("0500000380")
join_record.add_phone("0500000321")

joio_record = Record("Joio")
joio_record.add_phone("0500000480")
joio_record.add_phone("0500000380")

book.add_record(join_record)
book.add_record(joio_record)
book.delete("Joio")

print(book)

join = book.find("Join")
join.edit_phone("0500000380", "0500000945")
print(join)

found_phone = join.find_phone("0500000420")
print(f"{join.name}: {found_phone}")
