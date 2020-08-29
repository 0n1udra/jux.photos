from django.db import models
from datetime import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateField(default=datetime.now(), editable=True)

