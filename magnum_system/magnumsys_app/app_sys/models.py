from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse





class CategoryList(models.Model):
    name=models.CharField(max_length=255,db_index=True)
    slug=models.SlugField(max_length=255,unique=True)


    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name    




class Item(models.Model):
    categorylist=models.ForeignKey(CategoryList,related_name='item',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='item_creater')
    title=models.CharField(max_length=255)
    author = models.CharField(max_length=255,default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug= models.SlugField(max_length=255)
    price=models.DecimalField(max_digits=30, decimal_places=0,default=True)
    in_stock=models.BooleanField(default=True)
    in_active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    recipe=models.FileField(upload_to='recipe/',default=True)

    class Meta:
        verbose_name_plural = 'Item'
        ordering=('-created',)  


    def __str__(self):
        return self.title   
    