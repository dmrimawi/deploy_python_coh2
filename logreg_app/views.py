from django.shortcuts import redirect, render
from . import models
import re
import bcrypt
# Create your views here.

def index(request):
    if "id" in request.session:
        return redirect("/welcome")
    return render(request, 'index.html')

def welcome(request):
    if "id" in request.session:
        context = {
            'all_books': models.get_all_books(),
            'fav_books': models.get_fav_books(request.session['id']),
        }
        return render(request, 'welcome.html', context)
    return redirect("/")

def check_password(passwd, conpasswd):
    num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # for n in num:
    #     if str(n) in passwd:
    #         return True
    # return False
    if passwd == conpasswd and len(passwd) >= 8 and any(str(n) in passwd for n in num):
        return True
    return False

def check_email(email):
    if re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', email) is not None:
        return True
    return False

def register(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        passwd = request.POST['passwd']
        conpasswd = request.POST['conpasswd']
        if check_password(passwd, conpasswd) and check_email(email):
            hashed_passwd =  bcrypt.hashpw(passwd.encode(), bcrypt.gensalt()).decode()
            user = models.create_user(first_name, last_name, email, hashed_passwd)
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect("/welcome")
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        passwd = request.POST['passwd']
        user = models.get_user(email)
        if user and bcrypt.checkpw(passwd.encode(), user.passwd.encode()):
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect("/welcome")
    return redirect("/")

def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        desc = request.POST['description']
        models.create_book(title, desc, request.session['id'])
        return redirect("/welcome")
    return redirect("/")


def add_fav(request, book_id):
    if "id" in request.session:
        models.add_fav_book(request.session['id'], book_id)
        return redirect("/welcome")
    return redirect("/")