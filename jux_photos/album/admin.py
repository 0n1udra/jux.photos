import os, uuid, zipfile
from PIL import Image

from datetime import datetime
from django.contrib import admin
from django.core.files.base import ContentFile
from django.utils.html import format_html

import jux_photos.settings

from album.models import Album, AlbumImage
from album.forms import AlbumForm


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'thumb')
    list_filter = ('created',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()

            if form.cleaned_data['zip'] != None:
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):
                    file_name = os.path.basename(filename)
                    if not file_name: continue

                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename

                    filename = f'{album.slug}{str(uuid.uuid4())[-13:]}.jpg'
                    img.image.save(filename, contentfile)

                    filepath = f'{jux_photos.settings.MEDIA_ROOT}/albums/{album.title}/{filename}'
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save(f'thumb-{filename}', contentfile)
                    img.save()
                zip.close()
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)


# In case image should be removed from album.
@admin.register(AlbumImage)
class AlbumImageModelAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(f"<img src='{obj.thumb.url}' />")

    list_display = ('image_tag', 'alt', 'album')
    list_filter = ('album', 'created')