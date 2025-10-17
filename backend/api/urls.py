
from django.urls import path
from . import views

app_name = 'api'  

urlpatterns = [
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', views.TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path("create-stripe-customer/", views.CreateStripeCustomerView.as_view(), name="create-stripe-customer"),

    
]