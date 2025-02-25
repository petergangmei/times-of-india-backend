from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('api/', include('app.api.urls')),  # Updated to include the full path to api.urls
]
