from django.urls import path
from app_sys import views
from .views import home,signin,signup,profile,admin_panel,crud,create,delete,edit
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('delete/',delete.as_view(),name='delete'),
    
    path('edit/<int:id>/',edit.as_view(),name='edit'),
    path('crud/',crud.as_view(),name='crud'),
    path('create/',create.as_view(),name='create'),
    path('profile/',profile,name='profile'),
    path('home/item/<slug:slug>',views.item_details,name='item_detail'),
    path('signin/',signin,name='signin'),
    path('signup/',signup.as_view(),name='signup'),
    path('add_item/', views.add_item, name='add_item'),
    path('admin_panel/',admin_panel,name='admin_panel'),
    path('home/',views.all_items,name='all_items'),
    path('imgupload/',views.imgupload,name='imgupload'),
    path('index/',views.index,name='index'),
    path('addItem/',views.addItem,name='additem'),
    path('editItem/<slug:slug>',views.addItem,name='editItem'),    
]