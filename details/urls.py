
from django.urls import path  
from details import views 
  
urlpatterns = [ 
    path('<int:id_car>/', views.detail, name = 'detail'),
    path('<int:id_car>/booking/', views.booking, name = 'booking'),
    path('confirm/<int:id_rent>/', views.confirm, name = 'confirm'),
    path('reservation/', views.reservation_list, name='reservation_list'),
    path('verify/<int:id>/', views.verify_payment, name = 'verify'),
    path('invoice/<int:id_rent>/', views.invoice, name = 'invoice') 
] 
