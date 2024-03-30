from django.urls import path
from dashboard.views import *
from django.contrib.auth import views as auth_views

# urls.py
urlpatterns = [
    path("",index,name='home'),
    # --SINGUP AND LOGIN--
    path("login",handlelogin,name='login'),
    path("dashboard",dashboard,name='dashboard'),
    # path("campaign_effect",campaign_effect,name='campaign_effect'),
    path("order_data",order_data,name='order_data'),
    # path("signup/",handlesignup,name='signup'),
    # path("logout/",handlelogout,name='logout'),
    # path("verify_user/<str:code>/",verify_user,name='verify_user'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),   
]
