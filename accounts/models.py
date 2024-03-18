from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    goals = models.IntegerField(default=0)
    date_of_birth = models.DateField(null=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month:
            age -= 1
        elif today.month == self.date_of_birth.month and today.day < self.date_of_birth.day:
            age -= 1
        return age

    def __str__(self):
        return self.user.username
