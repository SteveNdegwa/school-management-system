from django.db import models

from base.models import BaseModel, GenericBaseModel, State, School, Subject
from users.models import User


class Author(GenericBaseModel):
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

class Publisher(GenericBaseModel):
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)

class BookCategory(GenericBaseModel):
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_created',)
        verbose_name = "Book Category"
        verbose_name_plural = "Book Categories"

class Book(BaseModel):
    number = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    publication_year = models.IntegerField(null=True, blank=True)
    state = models.ForeignKey(State, default=State.idle, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.title, self.author)

    class Meta:
        ordering = ('-date_created',)

class UserBook(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    state = models.ForeignKey(State, default=State.active, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.user, self.book)

    class Meta:
        ordering = ('-date_created',)
        verbose_name = "User Book"
        verbose_name_plural = "User Book"
