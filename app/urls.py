from django.urls import path
from app import views
app_name = 'app'
urlpatterns = [

    path(r'', views.index, name='index'),
    path('about', views.about, name='about'),
    path(r'<slug:cat_no>/', views.detail, name='detail'),
    path('products', views.products, name='products'),
    path('placeorder', views.place_order, name='place_order'),
    path(r'products/<slug:prod_id>/', views.productdetail, name='Productdetail'),

    ]
