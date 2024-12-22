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
            school_id = str(data.get("school_id", "")).lower()
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            author_name = str(data.get("author_name", "")).title().strip()
            if not author_name:
                raise Exception("Author name not provided")
            author = AuthorService().get_or_create(name=author_name, state=State.active())
            publisher_name = str(data.get("publisher_name", "")).title().strip()
            if not publisher_name:
                raise Exception("Publisher name not provided")
            publisher = PublisherService().get_or_create(name=publisher_name, state=State.active())
            category_name = str(data.get("category_name", "")).title().strip()
            if not category_name:
                raise Exception("Category name not provided")
            category = BookCategoryService().get_or_create(name=category_name, state=State.active())
            subject_name = str(data.get("subject_name", "")).title().strip()
            if not subject_name:
                raise Exception("Subject name not provided")
            subject = SubjectService().get_or_create(name=subject_name, state=State.active())
            k = {"number": number, "title": title, "publication_year": publication_year, "school": school,
                 "author": author, "publisher": publisher, "category": category, "subject": subject}
            book = BookService().create(**k)
            if not book:
                raise Exception("Book not created")
            return JsonResponse({
                "code": "100.000.000", "message": "Book created successfully", "book_id": str(book.id)})
        except Exception as e:
            lgr.exception("Create book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Create book failed with an exception", "error": e})

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
            school_id = str(data.get("school_id", "")).lower()
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            author_name = str(data.get("author_name", "")).title().strip()
            if not author_name:
                raise Exception("Author name not provided")
            author = AuthorService().get_or_create(name=author_name, state=State.active())
            publisher_name = str(data.get("publisher_name", "")).title().strip()
            if not publisher_name:
                raise Exception("Publisher name not provided")
            publisher = PublisherService().get_or_create(name=publisher_name, state=State.active())
            category_name = str(data.get("category_name", "")).title().strip()
            if not category_name:
                raise Exception("Category name not provided")
            category = BookCategoryService().get_or_create(name=category_name, state=State.active())
            subject_name = str(data.get("subject_name", "")).title().strip()
            if not subject_name:
                raise Exception("Subject name not provided")
            subject = SubjectService().get_or_create(name=subject_name, state=State.active())
            k = {"number": number, "title": title, "publication_year": publication_year, "school": school,
                 "author": author, "publisher": publisher, "category": category, "subject": subject}
            book = BookService().update(pk=book.id, **k)
            if not book:
                raise Exception("Book not edited")
            return JsonResponse({"code": "100.000.000", "message": "Book edited successfully"})
        except Exception as e:
            lgr.exception("Edit book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Edit book failed with an exception", "error": e})

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
            return JsonResponse({"code": "999.999.999", "message": "Delete book failed with an exception", "error": e})

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
            return JsonResponse({"code": "999.999.999", "message": "Issue book failed with an exception", "error": e})

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
            return JsonResponse({"code": "999.999.999", "message": "Return book failed with an exception", "error": e})

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
                .annotate(title=F("book__title")).annotate(number=F("book__number")) \
                .annotate(author_name=F("book__author__name")).annotate(publisher_name=F("book__publisher__name")) \
                .annotate(category_name=F("book__category__name")).annotate(subject_name=F("book__subject__name")) \
                .annotate(publication_year=F("book__publication_year")).annotate(from_date=F("date_created")) \
                .annotate(to_date=F("date_modified")).annotate(state_name=F("state__name")).values(
                "book_id", "number", "title", "author_name", "publisher_name", "category_name", "subject_name",
                "publication_year", "from_date", "to_date", "state_name")
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully fetched user borrowing history", "data": history})
        except Exception as e:
            lgr.exception("Get user borrowing history exception: %s" % e)
            return JsonResponse({
                "code": "999.999.999", "message": "Get user borrowing history failed with an exception", "error": e})

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
            book_data = BookService().filter(id=book_id).annotate(author_name=F("author__name")) \
                .annotate(publisher_name=F("publisher__name")).annotate(category_name=F("category__name")) \
                .annotate(subject_name=F("subject__name")).annotate(state_name=F("state__name")).values(
                "id", "number", "title", "school_id", "author_name", "publisher_name", "category_name", "subject_name",
                "publication_year", "state_name").first()
            issue_history = UserBookService().filter(book=book, state=State.returned()) \
                .annotate(first_name=F("user__first_name")).annotate(last_name=F("user__last_name")) \
                .annotate(other_name=F("user__other_name")).annotate(classroom_name=F("user__classroom__name")) \
                .annotate(state_name=F("state__name")).annotate(from_date=F("date_created")) \
                .annotate(to_date=F("date_modified")).values(
                "user_id", "first_name", "last_name", "other_name", "classroom_name", "state_name",  "from_date",
                "to_date")
            book_data["issue_history"] = list(issue_history)
            if book_data.state == State.issued():
                issued_to = UserBookService().filter(book=book, state=State.active()) \
                    .annotate(first_name=F("user__first_name")).annotate(last_name=F("user__last_name")) \
                    .annotate(other_name=F("user__other_name")).annotate(classroom_name=F("user__classroom__name")) \
                    .annotate(state_name=F("state__name")).annotate(from_date=F("date_created")).values(
                    "user_id", "first_name", "last_name", "other_name", "classroom_name", "state_name" "from_date") \
                    .first()
                book_data["issued_to"] = issued_to
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully fetched book's details", "data": book_data})
        except Exception as e:
            lgr.exception("Get book exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Get book failed with an exception", "error": e})

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
            school_id = data.pop("school_id", "")
            if not school_id:
                raise Exception("School id not provided")
            school = SchoolService().get(id=school_id, state=State.active())
            if not school:
                raise Exception("School not found")
            data["school"] = school
            if "author_name" in data:
                author_name = data.pop("author_name")
                author = AuthorService().get(name=author_name, state=State.active())
                data["author"] = author
            if "publisher_name" in data:
                publisher_name = data.pop("publisher_name")
                publisher = PublisherService().get(name=publisher_name, state=State.active())
                data["publisher"] = publisher
            if "category_name" in data:
                category_name = data.pop("category_name")
                category = BookCategoryService().get(name=category_name, state=State.active())
                data["category"] = category
            if "subject_name" in data:
                subject_name = data.pop("subject_name")
                subject = SubjectService().get(name=subject_name, state=State.active())
                data["subject"] = subject
            if "state_name" in data:
                state_name = data.pop("state_name")
                state = StateService().get(name=state_name)
                data["state"] = state
            filter_results = BookService().filter(**data).annotate(author_name=F("author__name")) \
                .annotate(publisher_name=F("publisher__name")).annotate(category_name=F("category__name")) \
                .annotate(subject_name=F("subject__name")).annotate(state_name=F("state__name")).values(
                "id", "number", "title", "school_id", "author_name", "publisher_name", "category_name", "subject_name",
                "publication_year", "state_name")
            filter_results = list(filter_results)
            return JsonResponse({
                "code": "100.000.000", "message": "Successfully filtered books", "data": filter_results})
        except Exception as e:
            lgr.exception("Filter books exception: %s" % e)
            return JsonResponse({"code": "999.999.999", "message": "Filter books failed with an exception", "error": e})

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
            return JsonResponse({"code": "999.999.999", "message": "Get authors failed with an exception", "error": e})

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
            return JsonResponse({
                "code": "999.999.999", "message": "Get publishers failed with an exception", "error": e})

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
            return JsonResponse({
                "code": "999.999.999", "message": "Get book categories failed with an exception", "error": e})
