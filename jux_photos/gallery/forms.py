#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from .models import Gallery

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Gallery
        exclude = []

    zip = forms.FileField(required=False)