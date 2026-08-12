from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
]