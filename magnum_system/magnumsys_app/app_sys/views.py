import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

from .forms import CreateForm, SigninForm, SignupForm
from .models import CategoryList, Item
import re





class edit(View):
    def get(self, request, id):
        item = Item.objects.get(id=id)
        fm = CreateForm(instance=item)
        return render(request, 'auth/edit.html', {'form': fm})

    def post(self, request, id):
        item = Item.objects.get(id=id)
        fm = CreateForm(request.POST, instance=item)

        if fm.is_valid():
            fm.save()
            return redirect('/crud/')


class delete(View):
    def post(self, request):
        data = request.POST
        id = data.get('id')

        itemdata = Item.objects.get(id=id)
        itemdata.delete()
        return redirect('/crud/')


class create(View):
    def get(self, request):
        fm = CreateForm()
        return render(request, 'auth/create.html', {'form': fm})

    def post(self, request,):
        fm = CreateForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect('crud')
        else:
            return render(request, 'auth/create.html', {'form': fm})


class crud(View):
    def get(self, request):
        item_data = Item.objects.all()
        return render(request, 'auth/crud.html', {'item_data': item_data})


def imgupload(request):
    if request.method == "POST":

        return render(request, "auth/profile.html")

    return render(request, "auth/profile.html")


def editItem(request, slug):
    item = Item.objects.all()
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(item.image) > 0:
                os.remove(item.image.path)
            item.image = request.FILES['image']
        item.title = request.POST.get('title')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        item.save()
        messages.success(request, "updated")
        return redirect('/')
    context = {'item': item}
    return render(request, 'auth/edit.html', context)


def index(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'auth/index.html', context)


def addItem(request):
    if request.method == 'POST':
        prod = Item()
        prod.title = request.POST.get('title')
        prod.price = request.POST.get('price')
        prod.description = request.POST.get('description')

        if len(request.FILES) != 0:
            prod.image = request.FILES['image']

        prod.save()
        messages.success(request, 'Product  Added Successfully')
        return redirect('/')

    return render(request, 'auth/add.html')


def admin_panel(request):

    all_items = Item.objects.all()
    return render(request, 'auth/admin_panel.html', {'all_items': all_items})


def add_item(request):
    return render(request, 'auth/add.html')


def profile(request):

    username = User.objects.all()

    if (request.user.is_authenticated and user is not None):

        username = request.user.username

    return render(request, 'auth/profile.html', {'username': username})

# Create your views here.


def categories(request):
    return {
        'categories': CategoryList.objects.all()
    }


def item(request):
    return {
        'item': Item.objects.all()
    }


def user(request):
    return {
        'userset': User.objects.all()
    }


def all_items(request):

    items = Item.objects.all()
    username = User.objects.all()
    if (request.user.is_authenticated and user is not None):

        username = request.user.username
    context = {'items': items, 'username': username}

    return render(request, 'auth/home.html', context)


def item_details(request, slug):
    items = get_object_or_404(Item, slug=slug, in_stock=True)
    return render(request, 'auth/detail.html', {'item': items})


def home(request):
    username = User.objects.all()

    if (request.user.is_authenticated and user is not None):

        username = request.user.username
    return render(request, 'auth/home.html', {'username': username})


def signout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('home')


def signin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            uname = user.username
            return redirect('/home/', {'uname': uname})
        else:
            messages.success(request, "Username or password is incorrect.")
            return redirect('signin')
    else:
        return render(request, 'auth/signin.html')


class signup(View):
    form_class = SignupForm
    template_name = 'auth/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            uname = form.cleaned_data.get('username')
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            pass1 = form.cleaned_data.get('password1')
            pass2 = form.cleaned_data.get('password2')

            if User.objects.filter(username=uname).exists():
                messages.info(request, "Username is Taken")
                return redirect('/signup')

            myuser = User.objects.create_user(username=uname, email=email, password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            messages.success(request, "Your account has been created")
            return redirect('/signin/')

        return render(request, self.template_name, {'form': form})

# def signup(request):

#     if request.method == 'POST':
#         form = SignupForm(request.POST or None)
#         if form.is_valid():
#             uname = request.POST.get('uname')
#             fname = request.POST.get('fname')
#             lname = request.POST.get('lname')
#             email = request.POST.get('email')
#             pass1 = request.POST.get('pass1')
#             pass2 = request.POST.get('pass2')

           
#             myuser = User.objects.create_user(uname, email, pass1)
#             myuser.first_name = fname

#             myuser.last_name = lname

#             myuser.save()

#             messages.success(request, "Your account created")
            
#             return redirect('/signin/')
        
#     else:
#         form = SignupForm()

#     try:
#         if User.objects.get(uname=uname):
#             messages.info(request, "Username is Taken")
#             return redirect('/signup')
#     except:
#         pass

#     return render(request, 'auth/signup.html', {'form': form})
