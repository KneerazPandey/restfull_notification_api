from django.urls import path
from . views import DevelopmentView


urlpatterns = [
    path('dev/', DevelopmentView.as_view(), name='Development View')
]