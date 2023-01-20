from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('openbeta/', views.openbeta, name='openbeta'),
    # path('admin2/',views.manage, name='manage'),
    path('admin2/',views.login, name='login'),
    path('download/image/', views.download_image, name='download_image', kwargs={'path':''}),
]
