from django.contrib import admin

from books.models import Author, Publisher, BookCategory, Book, UserBook


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'phone_number', 'email', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'address', 'phone_number', 'email', 'state__name')

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = (
        'title', 'author', 'publisher', 'category', 'subject', 'publication_year', 'school', 'state', 'date_modified',
        'date_created'
    )
	search_fields = (
        'title', 'author__name', 'publisher__name', 'category__name', 'subject__name', 'publication_year',
		'school__name', 'school__code', 'state__name'
    )

@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
	list_display = ('user', 'book', 'state', 'date_modified', 'date_created')
	search_fields = (
        'user__id', 'user__id_no', 'user__reg_no', 'user__first_name', 'user__last_name', 'book__title',
		'book__author__name', 'book__publisher__name', 'book__category__name', 'book__publication_year',
		'book__school__name', 'book__school__code', 'state__name'
    )
