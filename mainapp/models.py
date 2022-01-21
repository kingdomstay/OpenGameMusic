from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Track(models.Model):
    name = models.CharField(max_length=60, help_text='Название трека')
    track_url = models.CharField(max_length=256, help_text='Ссылка на файл (Firestore Storage)')
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Кем опубликовано')
    publish = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes')

    class Meta:
        ordering = ('-publish',)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('track-detail', args=[str(self.id)])