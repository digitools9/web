from django.contrib import admin
from django.urls import path
from . import views  # Import views from the current app
from imgtools import views as img_views  # Import views from the imgtools app
from pdftools import views as pdf_views  # Import views from the pdftools app
from utiltools import views as util_views  # Import views from the utiltools app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('img-resize/', img_views.img_resize, name='img-resize'),
    path('img-to-img/', img_views.img_to_img, name='img-to-img'),
    path('img-to-pdf/', img_views.img_to_pdf, name='img-to-pdf'),
    path('pdf-merger/', pdf_views.pdf_merge, name='pdf-merger'),
    path('pdf-splitter/', pdf_views.pdf_splitter, name='pdf-splitter'),
    path('encrypt-pdf/', pdf_views.encrypt_pdf, name='encrypt-pdf'),
    path('decrypt-pdf/', pdf_views.decrypt_pdf, name='decrypt-pdf'),
    path('qr-generator/', util_views.qr_generator, name='qr-generator'),
    path('url-shortener/', util_views.url_shortener, name='url-shortener'),
]
