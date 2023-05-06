
import os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import  CreateForm, SigninForm, SignupForm,ProfileForm,CreateUserForm,ItemForm
from .models import CategoryList, Item,Profile
import re
from django.views.generic import ListView
from django.db.models import Q



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






class signin(View):
    template_name = 'auth/signin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            uname = user.username
            return redirect('/home/', {'uname': uname})
        else:
            messages.success(request, "Username or password is incorrect.")
            return redirect('signin')



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
        

class editUser(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        fm = CreateUserForm(instance=user)
        return render(request, 'auth/edituser.html', {'form': fm})

    def post(self, request, id):
        user = User.objects.get(id=id)
        fm = CreateUserForm(request.POST, instance=user)

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
    

class deleteUser(View):
    def post(self, request):
        data = request.POST
        id = data.get('id')

        userdata = User.objects.get(id=id)
        userdata.delete()
        return redirect('/crud/')    


class createUser(View):
    def get(self, request):
        fm = CreateUserForm()
        return render(request, 'auth/createUser.html', {'form': fm})

    def post(self, request,):
        fm = CreateUserForm(request.POST, request.FILES)
        if fm.is_valid():
            fm.save()
            return redirect('crud')
        else:
            return render(request, 'auth/createUser.html', {'form': fm})

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
        user_data=User.objects.all()
        context={
            'item_data': item_data,
            'user_data': user_data
        }
        return render(request, 'auth/crud.html', context)













def filter(request):
    queryset = Item.objects.all()

    # Filter by category
    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(categorylist__slug=category)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'items': queryset,
    }
    return render(request, 'auth/home.html', context)

class search(ListView):
    
    template_name='auth/home.html'
    context_object_name= 'items'
    pagination_by=5

    def get_queryset(self):
        return Item.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args, **kwargs)
        context['q']=self.request.GET.get('q')
        return context



def item_list(request):
    items = Item.objects.filter(in_active=True)
    context = {
        'items': items
    }
    return render(request, 'auth/home.html', context)

# def publish(request):
#     if request.method == 'POST':
#         form = CreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.created_by = request.user
#             item.in_active = False
#             item.save()
#             return redirect('/home/')
#     else:
#         form = CreateForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'auth/publish.html', context)




def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, 'auth/profile_edit.html', context)

def profile(request):
    profile= Profile.objects.all()
    username = User.objects.all()
    if (request.user.is_authenticated and user is not None):
        username = request.user.username
        profile= request.user.profile
        context={
             'username': username,
             'profile':profile
        }
    return render(request, 'auth/profile.html',context)

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


# Create your views here.

# def addItem(request):
#     if request.method == 'POST':
#         prod = Item()
#         prod.title = request.POST.get('title')
#         prod.price = request.POST.get('price')
#         prod.description = request.POST.get('description')

#         if len(request.FILES) != 0:
#             prod.image = request.FILES['image']

#         prod.save()
#         messages.success(request, 'Product  Added Successfully')
#         return redirect('/')

#     return render(request, 'auth/add.html')


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

    items = Item.objects.order_by('-last_viewed')
    username = User.objects.all()
    if (request.user.is_authenticated and user is not None):

        username = request.user.username
    context = {'items': items, 'username': username}

    return render(request, 'auth/home.html', context)

def item_details(request, slug):
    items = get_object_or_404(Item, slug=slug, in_stock=True)
    items.last_viewed=datetime.now()
    items.save()
    return render(request, 'auth/detail.html', {'item': items})



# def addItem(request):
#     if request.method == 'POST':
#         prod = Item()
#         prod.title = request.POST.get('title')
#         prod.price = request.POST.get('price')
#         prod.description = request.POST.get('description')

#         if len(request.FILES) != 0:
#             prod.image = request.FILES['image']

#         prod.save()
#         messages.success(request, 'Product  Added Successfully')
#         return redirect('/')

#     return render(request, 'auth/add.html')



def home(request):
    username = User.objects.all()
    if (request.user.is_authenticated and user is not None):
        username = request.user.username
    return render(request, 'auth/home.html', {'username': username})

def signout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('/home/')

        


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




def pending(request):
    items = ItemForm.objects.filter(in_active=False)  # Filter items that are not yet approved
    return render(request, 'auth/pending.html', {'items': items})

def approve(request, slug):
    item = ItemForm.objects.get(slug=slug)
    item.in_active = True  # Set in_active flag to True to mark the item as approved
    item.save()
    return redirect('/')

def reject(request, slug):
    item = ItemForm.objects.get(slug=slug)
    item.in_active=False
    item.save()
    return redirect('/pending/')

def publish(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST,request.FILES )
        if form.is_valid():
            item = form.save(commit=False)
            item.in_active=False
            item.save()
            return redirect('/home/')  # Redirect to the list of items after successful submission
    
    return render(request, 'auth/publish.html', {'form': form})

