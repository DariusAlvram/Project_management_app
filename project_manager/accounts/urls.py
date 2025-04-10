from django.urls import path
from .views import dashboardView


app_name = 'accounts'

urlpatterns = [
    path('', dashboardView.as_view(), name='dashboard'),
]