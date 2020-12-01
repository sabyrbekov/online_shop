from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from . import views 


urlpatterns = [
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('activate/<uuid:activation_code>/', views.ActivationApiView.as_view(), name='activate_account'),
    path('logout/', views.Logout.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('logout/', views.Logout.as_view()),
]
