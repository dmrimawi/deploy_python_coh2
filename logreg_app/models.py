from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    passwd = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    users = models.ManyToManyField(User, related_name="books")
    uploaded_by_id = models.ForeignKey(User, related_name="user_books", on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Car(models.Model):
    name = models.CharField(max_length=200)
    model = models.IntegerField()
    clients = models.ManyToManyField(User, related_name="cars")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def create_user(first_name, last_name, email, passwd):
    return User.objects.create(first_name=first_name, last_name=last_name,
                                email=email, passwd=passwd)

def create_book(title, desc, user_id):
    user = User.objects.get(id=user_id)
    book = Book.objects.create(title=title, desc=desc, uploaded_by_id=user)
    user.books.add(book)
    return book

def get_user(email):
    users = User.objects.filter(email=email)
    if len(users) > 0:
        return users[0]
    return None

def get_user_cars(id):
    user = User.objects.get(id=id)
    return user.cars.all()

def get_all_books():
    return Book.objects.all()

def get_fav_books(user_id):
    user = User.objects.get(id=user_id)
    return user.books.all()

def add_fav_book(user_id, book_id):
    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)
    user.books.add(book)
