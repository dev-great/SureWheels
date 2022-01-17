from django.urls import include, path
from homepage import views
from .views import AboutPage, ServicePage, ContactPage


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', AboutPage.as_view(), name='aboutPage'),
    path('service/', ServicePage.as_view(), name='servicePage'),
    path('contact/', ContactPage.as_view(), name='contactPage'),
    path('admin/management/car/add/', views.add_edit_car, name='add_edit_car'),
    path('admin/management/car/<int:id_car>/change/', views.change_car, name='change_car'),
    path('car_detail/<int:id_car>', views.car_detail, name='car_detail')

]
