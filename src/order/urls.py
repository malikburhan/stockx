from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.order_sale_list, name='order_sale_list'),
    path('api_order_sale_list', views.api_order_sale_list, name='api_order_sale_list'),

    path('api_order_sale_save', views.api_order_sale_save, name='api_order_sale_save'), #create

    path('<str:id>/api_order_sale_obj', views.api_order_sale_obj, name='api_order_sale_obj'),  # update
    path('<str:id>/api_order_sale_edit', views.api_order_sale_edit, name='api_order_sale_edit'), # update
    path('<str:id>/api_order_sale_delete', views.api_order_sale_delete, name='api_order_sale_delete'), # update

    path('order_bot', views.order_bot, name='order_bot'),

]