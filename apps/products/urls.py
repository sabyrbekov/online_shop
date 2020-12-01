from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register('viewsets-products', views.ProductViewSet, basename='viewsets-products')

urlpatterns = [
    path('<int:pk>/', views.ProductDetailApiView.as_view()),
    path('', views.ProductListApiView.as_view()),
    path('wishlist/', views.WishListApiView.as_view()),
    path('<int:pk>/wish/add/', views.WishAdd.as_view()),
    path('wish/<int:pk>/favorite_delete/', views.WishDelete.as_view()),
]