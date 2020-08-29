from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

from .models import Gallery, GalleryImage

def gallery(request):
    list = Gallery.objects.filter(is_visible=True).order_by('-created')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        gallery = paginator.page(page)
    except PageNotAnInteger:
        gallery = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        gallery = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'gallery.html', { 'gallery': list })

class AlbumDetail(DetailView):
    model = Gallery

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = GalleryImage.objects.filter(album=self.object.id)
        return context

