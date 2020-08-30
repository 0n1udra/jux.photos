from django.shortcuts import render

def blog_view(request):
    return render(request, 'blog.html')

def about_view(request):
    return render(request, 'about.html')
