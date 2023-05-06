from django.urls import path
from app_sys import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
 
    path('filter/',filter,name='filter'),
    path('search/',search.as_view(),name='search'),
    path('reject/',reject,name='reject'),
    path('publish/', publish, name='publish'),
    path('item_list/', views.item_list, name='item_list'),
    path('home/item/<slug:slug>/', views.item_details, name='item_detail'),
    path('createUser/',createUser.as_view(),name='createUser'),
    path('editUser/<int:id>/',editUser.as_view(),name='editUser'),
    path('deleteUser/',deleteUser.as_view(),name='deleteUser'),
    path('delete/',delete.as_view(),name='delete'),
    path('edit_profile/<int:id>/',edit.as_view(),name='edit_profile'),
    path('edit/<int:id>/',edit.as_view(),name='edit'),
    path('crud/',crud.as_view(),name='crud'),
    path('create/',create.as_view(),name='create'),
    path('profile/',profile,name='profile'),
    path('profile_edit/',profile_edit,name='profile_edit'),
    path('home/item/<slug:slug>',views.item_details,name='item_detail'),
    path('signin/',signin.as_view(),name='signin'),
    path('signout/',signout,name='signout'),
    path('signup/',signup.as_view(),name='signup'),
    path('add_item/', views.add_item, name='add_item'),
    path('admin_panel/',admin_panel,name='admin_panel'),
    path('home/',views.all_items,name='all_items'),
    path('imgupload/',views.imgupload,name='imgupload'),
    path('index/',views.index,name='index'),
    path('addItem/',views.addItem,name='additem'),
    path('editItem/<slug:slug>',views.addItem,name='editItem'), 
    path('home/',home,name='home')   
]