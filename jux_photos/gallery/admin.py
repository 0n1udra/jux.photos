from django.contrib import admin

# Register your models here.
from .models import Gallery, GalleryImage

admin.site.register(Gallery)
admin.site.register(GalleryImage)
