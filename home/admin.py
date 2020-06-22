from django.contrib import admin
from .models import Profile, Book, Status, Ratings, PredictedBooks
# Register your models here.

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Status)
admin.site.register(Ratings)
admin.site.register(PredictedBooks)