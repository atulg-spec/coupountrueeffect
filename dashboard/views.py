from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from coupontrueeffect.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import random
import string

User = get_user_model()

def generate_verification_code(length=60):
    characters = string.ascii_letters + string.digits
    attempts = 0
    while True:
        verification_code = ''.join(random.choice(characters) for _ in range(length))
        if not CustomUser.objects.filter(verification_code=verification_code).exists():
            return verification_code
        attempts += 1

def index(request):       # Index Page for further Landing Pages
    return redirect('/login')

# LOGIN AND SIGNUP
def handlelogin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def handlesignup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.save()
            subject = "Important: Confirm your email"
            html_content = render_to_string('verification-email.html', {'verification_code': verification_code})
            content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject,
                content ,
                EMAIL_HOST_USER ,
                [user.email]
            )
            email.attach_alternative(html_content,'text/html')
            email.send()
            content = "An verification link has been sent to your email. Please verify to continue."
            return render(request,'message.html',{'content':content})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


def verify_user(request,code):
    try:
       client = User.objects.filter(verification_code = code).first()
       client.is_active = True
       client.save()
       messages.success(request,'Congratulations ! Your email has been successfully verified Please login to continue.')       
       return redirect('/login')
    except:
        return redirect('/')


def reset_password_done(request):
    content = "An Reset Password link has been sent to your email. Please reset to continue."
    return render(request,'message.html',{'content':content})

def password_reset_complete(request):
    messages.success(request,'Congratulations ! Your password updated successfully.')
    return redirect('/login')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = CampaignsForm(request.POST,request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            messages.success(request,'Campaign Registered Successfully.')
        else:
            errors = form.errors.items()
            for x in errors:
                messages.error(request,f'{x}')
    campaigns = Campaigns.objects.filter(user=request.user)
    context = {
        'campaignform':CampaignsForm(),
        'campaigns':campaigns,
    }
    return render(request,'dashboard.html',context)


@login_required
def order_data(request):
    if request.method == 'POST':
        form = OrderdataForm(request.POST,request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request,'Registered Successfully.')
        else:
            errors = form.errors.items()
            for x in errors:
                messages.error(request,f'{x}')
    orders = Orders.objects.filter(user=request.user)
    context = {
        'orderform':OrderdataForm(),
        'orders':orders,
    }
    return render(request,'order_data.html',context)


def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)
