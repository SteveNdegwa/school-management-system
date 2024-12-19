from django.urls import re_path

from books.views import BooksAdministration

urlpatterns = [
    re_path(r'create-book/$', BooksAdministration().create_book),
    re_path(r'edit-book/$', BooksAdministration().edit_book),
    re_path(r'delete-book/$', BooksAdministration().delete_book),
    re_path(r'issue-book/$', BooksAdministration().issue_book),
    re_path(r'return-book/$', BooksAdministration().return_book),
    re_path(r'get-book/$', BooksAdministration().get_book),
    re_path(r'filter-books/$', BooksAdministration().filter_books),
    re_path(r'user-borrowing-history/$', BooksAdministration().get_user_borrowing_history),
    re_path(r'get-authors/$', BooksAdministration().get_authors),
    re_path(r'get-publishers/$', BooksAdministration().get_publishers),
    re_path(r'get-book-categories/$', BooksAdministration().get_book_categories),
]