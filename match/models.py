from django.db import models

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile


class Match(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    place = models.CharField(max_length=250)
    date = models.DateTimeField()
    price = models.CharField(max_length=250)
    publish = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    players = models.ManyToManyField(Profile, related_name='players', blank=True, null=True)

    class Meta:
        ordering = ['publish']
        indexes = [
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    match = models.ForeignKey(Match,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.match}'
