from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'digitools/home.html')

def about(request):
    return render(request, 'digitools/about.html')