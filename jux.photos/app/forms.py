#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from app.models import Album, AlbumImage

from multiupload.fields import MultiImageField


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    file_upload = MultiImageField(min_num=0, max_num=30, max_file_size=1024*1024*5)


