import json
import xml.etree.ElementTree as ET # noqa
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class Display(ABC):

    @abstractmethod
    def display(self, book: Book) -> None:
        pass


class ConsoleDisplay(Display):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplay(Display):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class Printer(ABC):

    @abstractmethod
    def print_book(self, book: Book) -> None:
        pass


class ConsolePrinter(Printer):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}")
        print(book.content)


class ReverseConsolePrinter(Printer):
    def print_book(self, book: Book) -> None:
        print(f"Printing the reversed book: {book.title}")
        print(book.content[::-1])


class Serializer(ABC):

    @abstractmethod
    def serialize(self, book: Book) -> None:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    strategies = {
        "display": {
            "console": ConsoleDisplay(),
            "reverse": ReverseDisplay(),
        },
        "print": {
            "console": ConsolePrinter(),
            "reverse": ReverseConsolePrinter(),
        },
        "serialize": {
            "json": JsonSerializer(),
            "xml": XmlSerializer(),
        },
    }

    result = None

    for cmd, method_type in commands:
        strategy = strategies.get(cmd, {}).get(method_type)
        if not strategy:
            raise ValueError(f"Unknown {cmd} type: {method_type}")

        if cmd == "display":
            strategy.display(book)
        elif cmd == "print":
            strategy.print_book(book)
        elif cmd == "serialize":
            result = strategy.serialize(book)

    return result


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(
        main(sample_book, [
            ("display", "reverse"),
            ("serialize", "xml")
        ])
    )
