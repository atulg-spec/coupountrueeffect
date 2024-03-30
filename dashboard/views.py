from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
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
