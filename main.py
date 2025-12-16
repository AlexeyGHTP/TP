class Book:
    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def is_available(self):
        return self.__available

    def mark_as_taken(self):
        self.__available = False

    def mark_as_returned(self):
        self.__available = True

    def __str__(self):
        status = "доступна" if self.__available else "выдана"
        return f'"{self.__title}" - {self.__author} ({self.__year}) [{status}]'


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"
        # если "новая" - ничего не меняем

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} | {self.pages} стр., состояние: {self.condition}"


class EBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format

    def download(self):
        print(f"Книга '{self.get_title()}' загружается... ({self.file_size} МБ, {self.format})")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} | {self.file_size} МБ, формат: {self.format}"


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(f"{self.name} взял(а) книгу: {book.get_title()}")
        else:
            print(f"Книга '{book.get_title()}' недоступна")

    def return_book(self, book):
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            print(f"{self.name} вернул(а) книгу: {book.get_title()}")
        else:
            print(f"У {self.name} нет книги '{book.get_title()}'")

    def show_books(self):
        if not self.__borrowed_books:
            print(f"У {self.name} нет книг")
        else:
            print(f"Книги {self.name}:")
            for book in self.__borrowed_books:
                print(f"  - {book.get_title()}")

    def get_borrowed_books(self):
        return self.__borrowed_books.copy()


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)
        print(f"Библиотекарь {self.name} добавил(а) книгу: {book.get_title()}")

    def remove_book(self, library, title):
        library.remove_book(title)
        print(f"Библиотекарь {self.name} удалил(а) книгу: {title}")

    def register_user(self, library, user):
        library.add_user(user)
        print(f"Библиотекарь {self.name} зарегистрировал(а) пользователя: {user.name}")


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, title):
        book_to_remove = self.find_book(title)
        if book_to_remove:
            self.__books.remove(book_to_remove)
            return True
        return False

    def add_user(self, user):
        self.__users.append(user)

    def find_book(self, title):
        for book in self.__books:
            if book.get_title().lower() == title.lower():
                return book
        return None

    def show_all_books(self):
        if not self.__books:
            print("В библиотеке нет книг")
        else:
            print("Все книги в библиотеке:")
            for book in self.__books:
                print(f"  - {book}")

    def show_available_books(self):
        available_books = [book for book in self.__books if book.is_available()]
        if not available_books:
            print("Нет доступных книг")
        else:
            print("Доступные книги:")

            for book in available_books:
                print(f"  - {book}")

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = self.__find_user(user_name)

        if not book:
            print(f"Книга '{title}' не найдена в библиотеке")
            return False

        if not user:
            print(f"Пользователь '{user_name}' не зарегистрирован")
            return False

        if not book.is_available():
            print(f"Книга '{title}' уже выдана")
            return False

        user.borrow(book)
        return True

    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = self.__find_user(user_name)

        if not book:
            print(f"Книга '{title}' не найдена в библиотеке")
            return False

        if not user:
            print(f"Пользователь '{user_name}' не зарегистрирован")
            return False

        user.return_book(book)
        return True

    def __find_user(self, name):
        for user in self.__users:
            if user.name.lower() == name.lower():
                return user
        return None


if __name__ == '__main__':
    lib = Library()

    # --- создаём книги ---
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

    # --- создаём пользователей ---
    user1 = User("Анна")
    librarian = Librarian("Мария")

    # --- библиотекарь добавляет книги ---
    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)

    # --- библиотекарь регистрирует пользователя ---
    librarian.register_user(lib, user1)

    print("\n--- Доступные книги ---")
    lib.show_available_books()

    print("\n--- Пользователь берёт книгу ---")
    lib.lend_book("Война и мир", "Анна")

    print("\n--- Пользователь смотрит свои книги ---")
    user1.show_books()

    print("\n--- Доступные книги после выдачи ---")
    lib.show_available_books()

    print("\n--- Пользователь возвращает книгу ---")
    lib.return_book("Война и мир", "Анна")

    print("\n--- Электронная книга ---")
    b2.download()

    print("\n--- Ремонт книги ---")
    print("До ремонта:", b3)
    b3.repair()
    print("После ремонта:", b3)

    print("\n--- Все книги в библиотеке ---")
    lib.show_all_books()