from django.urls import path
from . import views
from .views import landing, register, user_login, user_logout, profile
from .views import user_logout, create_order, order_list, edit_order, delete_order
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("landing/", landing, name="landing"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    #path('', views.index, name='index'),
    path('calculate_cost/', views.calculate_cost, name='calculate_cost'),
    path('index/', views.index, name='index'),
    path('aud1/', views.aud1, name='aud1'),
    path('calculate_parallelepiped/', views.calculate_parallelepiped, name='calculate_parallelepiped'),
    path('orders/new/', create_order, name='create_order'),
    path('orders/', order_list, name='order_list'),
    path('orders/edit/<int:order_id>/', edit_order, name='edit_order'),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

