from django.urls import path,include
from . import views
from django.contrib import admin
from .views import admin_dashboard, sales_report_view
from .views import top_selling_products_view
from .views import sales_report
from .views import export_product_details_to_excel

from .views import chat_view
from django.views.generic import TemplateView
from .views import sales_by_date
from .views import inventory_report






urlpatterns = [
    path('', views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path('products/', views.admin_product_page, name='admin_product_page'),
    path('add/', views.product_add, name='product_add'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('search/', views.product_search, name='product_search'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/sales-report/', sales_report_view, name='sales_report'),
    path('top-selling-products/', top_selling_products_view, name='top_selling_products'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('export-product-details/', export_product_details_to_excel, name='export_product_details'),
   
    #path('daily-sales/', daily_sales_view, name='daily_sales'),
    path('chat/', chat_view, name='chat'),
    path('chatbot/', TemplateView.as_view(template_name='chatbot.html'), name='chatbot'),
    path('sales_by_date/', sales_by_date, name='sales_by_date'),

    path('inventory_report/', inventory_report, name='inventory_report'),
    
]
 


    

