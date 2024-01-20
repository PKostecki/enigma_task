from django.urls import path
from . import views

app_name = 'enigma_ecommerce'

urlpatterns = [
    path("", views.index, name="index"),
    path('product/list/',
         views.ProductListView.as_view(),
         name='product-list'),
    path('product/<int:pk>',
         views.ProductDetailView.as_view(),
         name='product-detail'
         ),
    path('product/create',
         views.ProductCreateView.as_view(),
         name='product-create',
         ),
    path('product/<int:pk>/update',
         views.ProductUpdateView.as_view(),
         name='product-update'
         ),
    path('product/<int:pk>/delete',
         views.ProductDeleteView.as_view(),
         name='product-delete'
         ),
    path('order/create',
         views.OrderCreateView.as_view(),
         name='create_order'),
    path('order/list',
         views.OrderItemListView.as_view(),
         name='order-list')
]
