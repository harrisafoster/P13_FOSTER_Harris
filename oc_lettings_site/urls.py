from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls'), name='lettings'),
    path('profiles/', include('profiles.urls'), name='profiles'),
    path('admin/', admin.site.urls),
]
