from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('order_sale_list', views.order_sale_list, name='order_sale_list'),
    path('api_order_sale_list', views.api_order_sale_list, name='api_order_sale_list'),

    path('api_order_sale_save', views.api_order_sale_save, name='api_order_sale_save'),

    path('order_bot', views.order_bot, name='order_bot'),

]