from django.contrib import admin
from .models import User, Advertisement, Category, News

admin.site.register(User)
admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(News)
