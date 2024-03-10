from datetime import datetime
from collections import UserDict, defaultdict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        # Реалізація валідації номера телефону.
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number should consist of 10 digits.")
        super().__init__(value)

class Birthday(Field):
    # Реалізація валідації формату дати народження.
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Date format should be DD.MM.YYYY")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday is not None else None

    # Додавання нового номера телефону до запису.
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Видалення вказаного номера телефону із запису.
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # Редагування наявного номера телефону в записі.
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone not found.")
    
    # Пошук вказаного номера телефону в записі.
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    # Додавання дня народження до запису.
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    # Додавання запису до self.data.
    def add_record(self, record):
        self.data[record.name.value] = record

    # Зміна телефонного номера для вказаного контакту.
    def change_phone(self, name, old_phone, new_phone):
        if name not in self.data:
            raise KeyError
        self.data[name].edit_phone(old_phone, new_phone)

    # Пошук запису за ім'ям.
    def find(self, name):
        contact = self.data[name]
        if contact:
            return contact
        else:
            raise KeyError
        
    # Всі контакти в адресній книзі.
    def all(self):
        return self.data
    
    # Видалення запису за ім'ям.
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found.")
        

    # Функція з ДЗ-1 (модифікована під ДЗ-3).
    def get_birthdays_per_week(self):
        birthdays = defaultdict(list)
        today = datetime.today().date()

        for name, record in self.data.items():
            if record.birthday and record.birthday.value:
                try:
                    # Аналіз дати народження:
                    birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                    birthday_this_year = birthday_date.replace(year=today.year)

                    # Оцінка дати на цей рік.
                    if birthday_this_year < today:
                        birthday_this_year = birthday_date.replace(year=today.year + 1)

                    delta_days = (birthday_this_year - today).days

                    # Визначення дня тижня.
                    if delta_days < 7:
                        day_of_week = birthday_this_year.strftime('%A')
                        if day_of_week in ["Saturday", "Sunday"]:
                            day_of_week = "Monday"

                        # Зберігаємо ім'я користувача у відповідний день тижня.
                        birthdays[day_of_week].append(record.name.value)

                except ValueError:
                    print(f"Incorrect birthday format for {name}")
        
        result = []
        # Виводимо зібрані імена по днях тижня (з понеділка по п'ятницю) у відповідному форматі.
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            if birthdays[day]:
                result.append(f"{day}: {', '.join(birthdays[day])}")
        return result
        
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")