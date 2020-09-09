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

            file_upload_field = form.files['file_upload']
            files = file_upload_field.multi_file_upload



            def check_has(item):
                for file in AlbumImage.objects.all().values():
                    print(file)
                    if file['filename'] == item:
                        return True

            for file in files:
                file_content, filename = file[0], file[1]
                alt_name = f'{album.slug}{str(uuid.uuid4())[-13:]}.jpg'
                file_path = jux_photos.settings.MEDIA_ROOT + 'albums/' + filename


                img = AlbumImage(album=album, alt=alt_name)
                img.filename = filename
                try:
                    img.image.save(alt_name, file_content)
                except:
                    # Sometimes there's an error saving the image, something to do with seek of closed file....
                    # This will try to delete the object then the image. Even though from my testing it'll still successfully upload the images...?
                    try: img.delete()
                    except: pass

                    try: os.remove(file_path)
                    except: pass

            file_upload_field.multi_file_upload = []
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


    list_display = ('image_tag', 'album_title')
    list_filter = ('album', 'created', AlbumAdminFilter)


