from django.urls import path, re_path
from . import views

app_name = "shop"

urlpatterns = [
    path("products/", views.ProductsListView.as_view(), name="products"),
    re_path(r'product/(?P<slug>[-\w]*)/detail/', views.ProductDetailView.as_view(), name="product-detail"),
    path("recent-products/", views.RecentProductsView.as_view(), name="recent-products"),
    path("discounted-products/", views.DiscountedProductsView.as_view(), name="discounted-products"),
]