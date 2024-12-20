import logging

from django.db import transaction as trx
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.backend.services import SchoolService, SubjectService, StateService
from base.models import State
from books.backend.services import AuthorService, PublisherService, BookCategoryService, BookService, UserBookService
from users.backend.decorators import user_login_required
from users.backend.services import UserService
from utils.get_request_data import get_request_data

lgr = logging.getLogger(__name__)

class BooksAdministration(object):
    @csrf_exempt
    @user_login_required
    def create_book(self, request):
        """
        Creates a book
        @params: WSGI request
        @return: Success message and book_id or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            number = data.get("number", "")
            if not number:
                raise Exception("Book number not provided")
            title = str(data.get("title", "")).title().strip()
            if not title:
                raise Exception("Book title not provided")
            publication_year = data.get("publication_year", "")
            school_id = str(data.get("school", "")).lower()
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            author = str(data.get("author", "")).title().strip()
            if not author:
                raise Exception("Author name not provided")
            author = AuthorService().get_or_create(name=author, state=State.active())
            publisher = str(data.get("publisher", "")).title().strip()
            if not publisher:
                raise Exception("Publisher name not provided")
            publisher = PublisherService().get_or_create(name=publisher, state=State.active())
            category = str(data.get("category", "")).title().strip()
            if not category:
                raise Exception("Category name not provided")
            category = BookCategoryService().get_or_create(name=category, state=State.active())
            subject = str(data.get("subject", "")).title().strip()
            if not subject:
                raise Exception("Subject name not provided")
            subject = SubjectService().get_or_create(name=subject, state=State.active())
            k = {"number": number, "title": title, "publication_year": publication_year, "school": school,
                 "author": author, "publisher": publisher, "category": category, "subject": subject}
            book = BookService().create(**k)
            if not book:
                raise Exception("Book not created")
            return JsonResponse({
                "code": "100.000.000", "message": "Book created successfully", "book_id": str(book.id)})
        except Exception as e:
            lgr.exception("Create book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Create book exception", "error": e})

    @csrf_exempt
    @user_login_required
    def edit_book(self, request):
        """
        Edits a book
        @params: WSGI request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            book_id = data.get("book_id", "")
            book = BookService().get(id=book_id)
            if not book:
                raise Exception("Book not found")
            number = data.get("number", "")
            if not number:
                raise Exception("Book number not provided")
            title = str(data.get("title", "")).title().strip()
            if not title:
                raise Exception("Book title not provided")
            publication_year = data.get("publication_year", "")
            school_id = str(data.get("school", "")).lower()
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(code=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            author = str(data.get("author", "")).title().strip()
            if not author:
                raise Exception("Author name not provided")
            author = AuthorService().get_or_create(name=author, state=State.active())
            publisher = str(data.get("publisher", "")).title().strip()
            if not publisher:
                raise Exception("Publisher name not provided")
            publisher = PublisherService().get_or_create(name=publisher, state=State.active())
            category = str(data.get("category", "")).title().strip()
            if not category:
                raise Exception("Category name not provided")
            category = BookCategoryService().get_or_create(name=category, state=State.active())
            subject = str(data.get("subject", "")).title().strip()
            if not subject:
                raise Exception("Subject name not provided")
            subject = SubjectService().get_or_create(name=subject, state=State.active())
            k = {"number": number, "title": title, "publication_year": publication_year, "school": school,
                 "author": author, "publisher": publisher, "category": category, "subject": subject}
            book = BookService().update(pk=book.id, **k)
            if not book:
                raise Exception("Book not edited")
            return JsonResponse({"code": "100.000.000", "message": "Book edited successfully"})
        except Exception as e:
            lgr.exception("Edit book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Edit book exception", "error": e})

    @csrf_exempt
    @user_login_required
    def delete_book(self, request):
        """
        Deletes a book
        @params: WSGI request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            book_id = data.get("book_id", "")
            book = BookService().get(id=book_id)
            if not book:
                raise Exception("Book not found")
            book.delete()
            return JsonResponse({"code": "100.000.000", "message": "Book deleted successfully"})
        except Exception as e:
            lgr.exception("Delete book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Delete book exception", "error": e})

    @csrf_exempt
    @user_login_required
    @trx.atomic
    def issue_book(self, request):
        """
        Issues a book
        @params: WSGI request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                raise Exception("User not found")
            book_id = data.get("book_id", "")
            book = BookService().get(id=book_id)
            if not book:
                raise Exception("Book not found")
            if book.state == State.issued():
                raise Exception("Book already issued")
            if not UserBookService().create(user=user, book=book):
                raise Exception("Book not issued")
            if not BookService().update(pk=book.id, state=State.issued()):
                raise Exception("Book state not updated")
            return JsonResponse({"code": "100.000.000", "message": "Book issued successfully"})
        except Exception as e:
            lgr.exception("Issue book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Issue book exception", "error": e})

    @csrf_exempt
    @user_login_required
    @trx.atomic
    def return_book(self, request):
        """
        Returns a book
        @params: WSGI request
        @return: Success or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            book_id = data.get("book_id", "")
            book = BookService().get(id=book_id)
            if not book:
                raise Exception("Book not found")
            if not UserBookService().filter(book=book).update(state=State.returned()):
                raise Exception("Book not returned")
            if not BookService().update(pk=book.id, state=State.idle()):
                raise Exception("Book state not updated")
            return JsonResponse({"code": "100.000.000", "message": "Book returned successfully"})
        except Exception as e:
            lgr.exception("Return book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Return book exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_user_borrowing_history(self, request):
        """
        Fetches user's borrowing history
        @params: WSGI request
        @return: Success message and borrowing history or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            user_id = data.get("user_id", "")
            user = UserService().get(id=user_id, state=State.active())
            if not user:
                raise Exception("User not found")
            history = UserBookService().filter(user=user) \
                .annotate(book_id=F("book__id")).annotate(title=F("book__title")) \
                .annotate(number=F("book__number")).annotate(author=F("book__author__name")) \
                .annotate(publisher=F("book__publisher__name")).annotate(category=F("book__category__name")) \
                .annotate(subject=F("book__subject__name")).annotate(publication_year=F("book__publication_year")) \
                .annotate(from_date=F("date_created")).annotate(to_date=F("date_modified")) \
                .annotate(state=F("state__name")).values(
                "book_id", "number", "title", "author", "publisher", "category", "subject", "publication_year",
                "from_date", "to_date", "state")
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully fetched user borrowing history", "data": history})
        except Exception as e:
            lgr.exception("Get user borrowing history exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get user borrowing history exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_book(self, request):
        """
        Fetches a book's details
        @params: WSGI request
        @return: Success message and book details or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            book_id = data.get("book_id", "")
            book = BookService().get(id=book_id)
            if not book:
                raise Exception("Book not found")
            book_data = BookService().filter(id=book_id).annotate(school=F("school__id")) \
                .annotate(author=F("author__name")).annotate(publisher=F("publisher__name")) \
                .annotate(category=F("category__name")).annotate(subject=F("subject__name")) \
                .annotate(state=F("state__name")).values(
                "id", "number", "title", "school", "author", "publisher", "category", "subject", "publication_year",
                "state").first()
            issue_history = UserBookService().filter(book=book, state=State.returned()) \
                .annotate(user_id=F("user__id")).annotate(first_name=F("user__first_name")) \
                .annotate(last_name=F("user__last_name")).annotate(from_date=F("date_created")) \
                .annotate(to_date=F("date_modified")).values(
                "user_id", "first_name", "last_name", "from_date", "to_date")
            book_data["issue_history"] = list(issue_history)
            if book_data.state == State.issued():
                issued_to = UserBookService().filter(book=book, state=State.active()) \
                    .annotate(user_id=F("user__id")).annotate(first_name=F("user__first_name")) \
                    .annotate(last_name=F("user__last_name")).annotate(from_date=F("date_created")).values(
                    "user_id", "first_name", "last_name", "from_date").first()
                book_data["issued_to"] = issued_to
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully fetched book's details", "data": book_data})
        except Exception as e:
            lgr.exception("Get book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get book exception", "error": e})

    @csrf_exempt
    @user_login_required
    def filter_books(self, request):
        """
        Filters books
        @params: WSGI request
        @return: Success message and filter results or error message
        @rtype: JsonResponse
        """
        try:
            data = get_request_data(request)
            data.pop("user_id", "")
            data.pop("token", "")
            if "school" in data:
                school = data.get("school")
                school = SchoolService().get(code=school, state=State.active())
                data["school"] = school
            if "author" in data:
                author = data.get("author")
                author = AuthorService().get(name=author, state=State.active())
                data["author"] = author
            if "publisher" in data:
                publisher = data.get("publisher")
                publisher = PublisherService().get(name=publisher, state=State.active())
                data["publisher"] = publisher
            if "category" in data:
                category = data.get("category")
                category = BookCategoryService().get(name=category, state=State.active())
                data["category"] = category
            if "subject" in data:
                subject = data.get("subject")
                subject = SubjectService().get(name=subject, state=State.active())
                data["subject"] = subject
            if "state" in data:
                state = data.get("state")
                state = StateService().get(name=state)
                data["state"] = state
            filter_results = BookService().filter(**data).annotate(school=F("school__id")) \
                .annotate(author=F("author__name")).annotate(publisher=F("publisher__name")) \
                .annotate(category=F("category__name")).annotate(subject=F("subject__name")) \
                .annotate(state=F("state__name")).values(
                "id", "number", "title", "school", "author", "publisher", "category", "subject", "publication_year",
                "state")
            filter_results = list(filter_results)
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully filtered books", "data": filter_results})
        except Exception as e:
            lgr.exception("Filter books exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Filter books exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_authors(self, request):
        """
        Fetches authors' details
        @params: WSGI request
        @return: Success message and authors' details or error message
        @rtype: JsonResponse
        """
        try:
            data = list(AuthorService().filter(state=State.active()).values("name"))
            return JsonResponse({"code": "100.000.000", "message": "Successfully fetched authors", "data": data})
        except Exception as e:
            lgr.exception("Get authors exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get authors exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_publishers(self, request):
        """
        Fetches publishers' details
        @params: WSGI request
        @return: Success message and publishers' details or error message
        @rtype: JsonResponse
        """
        try:
            data = list(PublisherService().filter(state=State.active()).values(
                "name", "address", "phone_number", "email"))
            return JsonResponse({"code": "100.000.000", "message": "Successfully fetched publishers", "data": data})
        except Exception as e:
            lgr.exception("Get publishers exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get publishers exception", "error": e})

    @csrf_exempt
    @user_login_required
    def get_book_categories(self, request):
        """
        Fetches book categories details
        @params: WSGI request
        @return: Success message and book categories details or error message
        @rtype: JsonResponse
        """
        try:
            data = list(BookCategoryService().filter(state=State.active()).values("name"))
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully fetched book categories", "data": data})
        except Exception as e:
            lgr.exception("Get book categories exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get book categories exception", "error": e})
