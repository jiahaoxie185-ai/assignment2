class LibraryItem:
    """Base class for any item that can be borrowed from the library."""

    def __init__(self, item_id, title):
        """Create an item that starts out available.

        Args:
            item_id: Unique ID of the item.
            title: Title of the item.
        """
        self.item_id = item_id
        self.title = title

        self.__is_checked_out = False
        self.__checked_out_by = None

    def checkout(self, member):
        """Mark the item as checked out by a member.

        Args:
            member: The Member borrowing the item.

        Returns:
            True if the checkout worked, False if the item was already checked out.
        """
        if not self.__is_checked_out:
            self.__is_checked_out = True
            self.__checked_out_by = member
            return True

        else:
            print("This item is checked out.")
            return False

    def return_item(self):
        """Mark the item as available again."""
        if self.__is_checked_out:
            self.__is_checked_out = False
            self.__checked_out_by = None

        else:
            print("This item is not checked out.")

    def get_status(self):
        """Return "Available" or "Checked out by <name>"."""
        if self.__is_checked_out:
            return f"Checked out by {self.__checked_out_by.name}"
        else:
            return "Available"

    def get_loan_period(self):
        """Return the default loan period in days (14)."""
        return 14

    def display_info(self):
        """Print the item's ID, title and status."""
        print(f"ID:{self.item_id}\n")
        print(f"Title:{self.title}\n")
        print(f"Status:{self.get_status()}\n")
class Book(LibraryItem):
    """A library item with an author and a page count."""

    def __init__(self, item_id, title, author, number_of_pages):
        """Create a book.

        Args:
            item_id: Unique ID of the book.
            title: Title of the book.
            author: Author of the book.
            number_of_pages: Number of pages.
        """
        super().__init__(item_id, title)

        self.author = author
        self.number_of_pages = number_of_pages

    def get_loan_period(self):
        """Return the book loan period in days (21). Overrides the base class."""
        return 21

    def display_info(self):
        """Print the book's info, including author and page count."""
        print(f"ID:{self.item_id}\n")
        print(f"Title:{self.title}\n")
        print(f"Author:{self.author}\n")
        print(f"Numbuer of pages:{self.number_of_pages}\n")
        print(f"Status:{self.get_status()}\n")


class DVD(LibraryItem):
    """A library item with a director and a runtime."""

    def __init__(self, item_id, title, director, runtime):
        """Create a DVD.

        Args:
            item_id: Unique ID of the DVD.
            title: Title of the DVD.
            director: Director of the movie.
            runtime: Runtime in minutes.
        """
        super().__init__(item_id, title)

        self.director = director
        self.runtime = runtime

    def get_loan_period(self):
            """Return the DVD loan period in days (7). Overrides the base class."""
            return 7

    def display_info(self):
        """Print the DVD's info, including director and runtime."""
        print(f"ID:{self.item_id}\n")
        print(f"Title:{self.title}\n")
        print(f"Director:{self.director}\n")
        print(f"Runtime:{self.runtime}\n")
        print(f"Status:{self.get_status()}\n")

class Member:
    """A library member who can hold up to three items at a time."""

    def __init__(self, member_id, name):
        """Create a member with no borrowed items.

        Args:
            member_id: Unique ID of the member.
            name: Name of the member.
        """
        self.member_id = member_id
        self.name = name

        self.checked_out_items = []

    def borrow_item(self, item: LibraryItem):
        """Add an item to this member's list if they have fewer than three.

        Args:
            item: The LibraryItem being borrowed.

        Returns:
            True if the item was added, False if the limit was reached.
        """
        if len(self.checked_out_items) >= 3:
            print("You can't borrow items more than 3.")
            return False
        else:
            self.checked_out_items.append(item)
            print(f"You borrowed {item.title}")
            return True


    def return_item(self, item: LibraryItem):
        """Remove an item from this member's list.

        Args:
            item: The LibraryItem being returned.

        Returns:
            True if the item was removed, False if the member didn't have it.
        """
        if item in self.checked_out_items:
            self.checked_out_items.remove(item)
            return True
        else:
            print("You didn't borrow this item.")
            return False

    def display_checked_out_items(self):
        """Print the titles of all items this member has borrowed."""
        if not self.checked_out_items:
            print("There is no checked out items.")

        for item in self.checked_out_items:
            print(f"{item.title}")
class Library:
    """Holds all items and members and coordinates checkouts and returns."""

    def __init__(self):
        """Create an empty library."""
        self.items = []
        self.members = []

    def add_item(self, item):
        """Add an item unless another item already uses its ID.

        Args:
            item: The LibraryItem to add.
        """
        if self.find_item(item.item_id) is None:
            self.items.append(item)
        else:
            print("Item ID already exist")

    def add_member(self, member):
        """Add a member unless another member already uses their ID.

        Args:
            member: The Member to add.
        """
        if self.find_member(member.member_id) is None:
            self.members.append(member)
        else:
            print("Member ID already exist")

    def find_item(self,item_id):
        """Return the item with this ID, or None if there isn't one."""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def find_member(self,member_id):
        """Return the member with this ID, or None if there isn't one."""
        for member in self.members:
            if member.member_id == member_id:
                return member

        return None

    def checkout_item(self, item_id, member_id):
        """Check out an item to a member, updating both objects.

        Args:
            item_id: ID of the item to check out.
            member_id: ID of the member borrowing it.
        """
        item = self.find_item(item_id)
        member = self.find_member(member_id)

        if item is None:
            print("Item not found.")
            return
        if member is None:
            print("Member not found")
            return
        if len(member.checked_out_items) >= 3:
            print("This member already has three items.")
            return
        if item.checkout(member):
            member.borrow_item(item)

    def return_item(self, item_id):
        """Return an item, updating both the item and the member who had it.

        Args:
            item_id: ID of the item to return.
        """
        item = self.find_item(item_id)

        if item is None:
            print("Item is not exist.")
            return


        for member in self.members:
            if item in member.checked_out_items:
                member.return_item(item)
                item.return_item()
                return


        print("This item is available")

    def display_available_items(self):
        """Print the titles of all items that are not checked out."""
        available_items = []

        for item in self.items:
            if item.get_status() == "Available":
                available_items.append(item)

        if len(available_items) == 0:
            print("No available items")

        for item in available_items:
            print(f"Available items:{item.title}")

    def display_checked_out_items(self):
        """Print the full info of every checked-out item."""
        checked_out_items = []
        for item in self.items:
            if item.get_status() != "Available":
                checked_out_items.append(item)

        if not checked_out_items:
            print("No checked out items.")
            return

        for item in checked_out_items:
            item.display_info()

def main():
    """Create the library objects and run the required test scenario."""
    library = Library()

    book1 = Book("B1", "1984", "George Orwell", 328)
    book2 = Book("B2", "The Hobbit", "J.R.R. Tolkien", 310)
    book3 = Book("B3", "Dune", "Frank Herbert", 412)
    dvd1 = DVD("D1", "Inception", "Christopher Nolan", 148)
    dvd2 = DVD("D2", "Spirited Away", "Hayao Miyazaki", 125)

    alex = Member("M1", "Alex")
    sam = Member("M2", "Sam")

    for item in [book1, book2, book3, dvd1, dvd2]:
        library.add_item(item)
    library.add_member(alex)
    library.add_member(sam)

    print("=== Adding duplicate IDs (should fail) ===")
    library.add_item(Book("B1", "Duplicate Book", "Someone", 100))
    library.add_member(Member("M1", "Duplicate Member"))

    print("\n=== 1. All available items ===")
    library.display_available_items()

    print("\n=== 2. Alex checks out a Book (B1) and a DVD (D1) ===")
    library.checkout_item("B1", "M1")
    library.checkout_item("D1", "M1")

    print("\n=== 3. Sam checks out another Book (B2) ===")
    library.checkout_item("B2", "M2")

    print("\n=== 4. Sam tries to check out B1, already checked out by Alex ===")
    library.checkout_item("B1", "M2")
    print(f"B1 status: {book1.get_status()}")

    print("\n=== 5. Return B2, then try to return it again ===")
    library.return_item("B2")
    print(f"B2 status after first return: {book2.get_status()}")
    library.return_item("B2")

    print("\n=== 6. Nonexistent item ID and nonexistent member ID ===")
    library.checkout_item("X99", "M1")
    library.checkout_item("B3", "M99")

    print("\n=== 7. Three-item limit: Alex borrows B3, then tries D2 ===")
    library.checkout_item("B3", "M1")
    library.checkout_item("D2", "M1")
    print(f"D2 status: {dvd2.get_status()}")

    print("\n=== 8. Each member's checked-out items ===")
    print("Alex:")
    alex.display_checked_out_items()
    print("Sam:")
    sam.display_checked_out_items()

    print("\n=== 9. All available and all checked-out items ===")
    print("--- Available ---")
    library.display_available_items()
    print("--- Checked out ---")
    library.display_checked_out_items()

    print("\n=== 10. Polymorphism: get_loan_period() on Books and DVDs ===")
    for item in [book1, book2, book3, dvd1, dvd2]:
        print(f"{item.title} ({type(item).__name__}): {item.get_loan_period()} days")
if __name__ == "__main__":

    main()


# AI usage statement:
# I used AI (Claude) to brainstorm the design of this assignment
# and to help write the docstrings/comments in this file.
