from django.contrib import admin
from .models import CategoryList,Item

@admin.register(CategoryList)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields = {'slug':('name',)}
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display=['title','author','slug','price','in_stock','created','updated']
    list_filter=['in_stock','in_active']

    list_editable=['price','in_stock']

    prepopulated_fields= {'slug':('title',)}

