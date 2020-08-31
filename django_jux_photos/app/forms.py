#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from app.models import Album


class ImageFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs=
        {'multiple': True, 'webkitdirectory': True, 'directory': True}))
