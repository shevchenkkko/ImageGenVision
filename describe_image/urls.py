from django.urls import path
from describe_image.views import *

app_name = 'describe'


urlpatterns = [
    path('', describe_image, name='describe_image'),
]
