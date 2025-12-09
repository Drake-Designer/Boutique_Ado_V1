from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def success(request):
    return HttpResponse("Login successful")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('success/', success, name='success'),
    path('', include('home.urls')),
]
