from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('faq/', views.faq_view, name='faq'),
    path('delivery/', views.delivery_info, name='delivery'),
    path('newsletter/', views.newsletter_signup, name='newsletter'),
    path('admin_orders/', views.admin_view, name='admin-orders'),
    path(
        'update_payment_status/<int:order_id>/',
        views.update_payment_status,
        name='update_payment_status'),
    path('get-random-bikes/', views.get_random_bikes, name='get_random_bikes'),
]
