from django.db import models

# Create your models here.
import uuid
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from multiupload.fields import MultiImageField

class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024)
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(300)], format='JPEG', options={'quality': 90})
    tags = models.CharField(max_length=250)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    #def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

    def __unicode__(self):
        return self.title


class AlbumImage(models.Model):
    image = models.ImageField(upload_to='albums')
    filename = models.CharField(max_length=255, blank=True, default='')
    thumb = ImageSpecField(source='image', processors=[ResizeToFit(300)], format='JPEG', options={'quality': 70})
    album = models.ForeignKey(Album, related_name='album', on_delete=models.PROTECT)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)



@receiver(pre_delete, sender=AlbumImage)
def album_image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)

@receiver(pre_delete, sender=Album)
def album_image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.thumb.delete(False)
