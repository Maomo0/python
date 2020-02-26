# Coding: UTF-8
# Author: Miao

from django.urls import path
from .views import LoginView, HomeView, CustomerView, ProductView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r"", LoginView.as_view(), name='home'),
    path(r'login/', LoginView.as_view(), name='login_in'),
    path(r'prod_home/', HomeView.get, name='prod_home'),
    path(r'prod_home/<int:msg_id>/', HomeView.check_msg, name='prod_msg'),
    path(r'customer_msg/', CustomerView.get, name='customer_msg'),
    path(r'customer_msg/search_customer', CustomerView.post, name='search_customer'),
    path(r'add_prod/', ProductView.add_prod, name='add_prod'),
    path(r'delete_prod/', ProductView.delete_prod, name='delete_prod'),
    path(r'prod_home/prod_search', ProductView.post, name='search_prod'),
    path(r'prod_modify/', ProductView.modify_msg, name='prod_modify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)