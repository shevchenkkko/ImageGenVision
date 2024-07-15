from django.urls import path
from generate_image.views import *

app_name = 'generate'
urlpatterns = [
    path('', first_page, name='first_page'),
    path('generate-image/', generate_image, name='generate_image')
]
