from logging import exception
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt

from e_food.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from .forms import NewUSerForm
import razorpay

def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = NewUSerForm()
    return render(request, 'accounts/signup.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('/')

def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 100

        client = razorpay.Client(
            auth=("rzp_live_35X6zFXeQlOyA9", "mSjTvYNYXj3HWolUR6nP2YRk"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'index.html')

@csrf_exempt
def success(request):
    return render(request, "success.html")
