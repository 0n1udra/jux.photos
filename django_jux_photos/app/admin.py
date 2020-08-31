import os, uuid, zipfile
from PIL import Image

from datetime import datetime
from django.contrib import admin
from django.core.files.base import ContentFile
from django.utils.html import format_html
from django.db import models

import jux_photos.settings

from app.models import Album, AlbumImage
from app.forms import AlbumForm


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    def thumbnail_tag(self, obj):
        return format_html(f"<img src='{obj.thumb.url}' />")

    form = AlbumForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'thumbnail_tag')
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

                    filepath = f'{jux_photos.settings.MEDIA_ROOT}albums/{album.title}/{filename}'
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save(f'thumb-{filename}', contentfile)
                    img.save()
                zip.close()
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)


class AlbumAdminFilter(admin.SimpleListFilter):
    title = 'Album'
    parameter_name = 'album_id'
    default_value = None

    def lookups(self, request, model_admin):
        queryset = AlbumImage.objects.all()
        list_of_albums = {(str(image.album_id), image.album.title) for image in queryset}
        return sorted(list_of_albums, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(album_id=self.value())
        return queryset



# In case image should be removed from album.
@admin.register(AlbumImage)
class AlbumImageModelAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(f"<img src='{obj.thumb.url}' />")

    def album_title(self, obj): return obj.album.title

    def lookups(self, request, model_admin):
        list_of_albums = []
        queryset = AlbumImage.objects.all()
        for album in queryset:
            list_of_albums.append((str(album.id), album.album))
        return sorted(list_of_albums, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(species_id=self.value())
        return queryset

    list_display = ('image_tag', 'album_title')
    list_filter = ('album', 'created', AlbumAdminFilter)


