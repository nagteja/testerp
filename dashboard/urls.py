from django.conf.urls import url, include
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    
   
]

