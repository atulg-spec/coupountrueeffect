from django.urls import path
from dashboard.views import *
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm,CustomSetPasswordForm

# urls.py
urlpatterns = [
    path("",index,name='home'),
    # --SINGUP AND LOGIN--
    path("login",handlelogin,name='login'),
    path("signup",handlesignup,name='signup'),
    path("verify_user/<str:code>/",verify_user,name='verify_user'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,  
        template_name='forgot_password.html', 
        email_template_name='password_reset_email.html',  
        subject_template_name='password_reset_subject.txt',  
    ), name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='forgot_password.html',  
        form_class=CustomSetPasswordForm, 
    ), name='password_reset_confirm'),
    path('reset_password_done/', reset_password_done, name='reset_password_done'),
    path('reset_password_complete/', password_reset_complete, name='password_reset_complete'),
    # -=-=-=-= SIGNUP AND LOGIN DONE-==-=-=-=-=-
    path("dashboard",dashboard,name='dashboard'),
    # path("campaign_effect",campaign_effect,name='campaign_effect'),
    path("order_data",order_data,name='order_data'),
]
