from books.models import Author, Publisher, BookCategory, Book, UserBook
from utils.ServiceBase import ServiceBase


class AuthorService(ServiceBase):
    manager = Author.objects

class PublisherService(ServiceBase):
    manager = Publisher.objects

class BookCategoryService(ServiceBase):
    manager = BookCategory.objects

class BookService(ServiceBase):
    manager = Book.objects

class UserBookService(ServiceBase):
    manager = UserBook.objects