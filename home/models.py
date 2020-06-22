
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
# Create your models here.

class Profile(models.Model):

    # for testing purpose i have set blank = True

    user        =   models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    age         =   models.IntegerField(blank = True, null = True)
    location    =   models.CharField(max_length = 50, blank = True)
    occupation  =   models.CharField(max_length = 50, blank = True)
    bio         =   models.TextField(blank = True)
    profile_pic =   models.ImageField(default = '/static/images/profile_pic/default.jpg', upload_to="profile_pic", null = True, blank = True)
    pref_genere  =   models.CharField(max_length = 100, blank = True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        print("Profile created!")

# post_save.connect(create_profile, sender = User)


@receiver(post_save, sender = User)
def update_profile(sender, instance, created, **kwargs):

    if created == False:
        instance.profile.save()
        print("Profile updated")

# post_save.connect(update_profile, sender = User)



class Book(models.Model):

    user        = models.ManyToManyField(User, blank = True)
    title       = models.CharField(max_length = 100, null = True)
    author      = models.CharField(max_length = 100, null = True)
    author_bio  = models.TextField(null = True,blank = True)
    isbn        = models.CharField(max_length = 10, validators = [MinLengthValidator(10)], null =True)
    book_image  = models.ImageField(upload_to = 'book_covers/', default = 'default.jpg')
    genere      = models.TextField(null = True, blank = True)
    synopsis    = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.title




class Status(models.Model):
    class Meta:
            unique_together = ('user', 'books',)

    CHOICES = (('1', 'Intrested'),
                ('2', 'Read'),
                 ('3', 'Reading'),)


    # user        = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    # books       = models.OneToOneField(Book,  on_delete = models.CASCADE, null = True)
    # user        = models.ManyToManyField(User)
    # books       = models.ManyToManyField(Book)
    user                = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    books               = models.ForeignKey(Book,  on_delete = models.CASCADE, null = True)
    status_of_book      = models.CharField(choices = CHOICES,max_length=1)

    def __str__(self):
        return str(self.books)

class Ratings(models.Model):

    class Meta:
        unique_together = ('user', 'book')

    user        = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    book        = models.ForeignKey(Book, on_delete = models.CASCADE, null = True)
    rating      = models.CharField(max_length=1, null = True)

    def __str__(self):
        return (f"{self.user} | {self.book} | {self.rating} ")


class PredictedBooks(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, null = True, unique = True)
    prediction      = models.TextField(null=True)
    
    def __str__(self):
        return str(self.user)