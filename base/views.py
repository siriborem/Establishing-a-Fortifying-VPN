from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Configuration
from .vpn_controller import VPNController
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
import asyncio
# from pyppeteer import launch

# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return HttpResponse("<strong>Password Mismatched</strong>")
        user_ins = User.objects.create_user(username=username, password=password)
        login(request, user_ins)
        return redirect('/')
    return render(request, 'user_register.html', context)

def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse("<strong>User Not Found</strong>")
    return render(request, 'user_login.html', context)

def user_logout(request):
    logout(request)
    return HttpResponse("<strong>Logged out successfully</strong>")


def create_new_connection(request):
    if not request.user.is_authenticated:
        return HttpResponse("<strong>Authentication Required</strong>")
    curr_user = request.user
    ip_addr = request.META.get('REMOTE_ADDR')
    controller = VPNController(request_ip=str(ip_addr))
    controller.mask_even()
    new_ip = controller.masked_ip
    new_config_ins = Configuration.objects.create(user=curr_user, ip_address=ip_addr, configuration= controller.configuration['method'], is_connected=True)

    return HttpResponse(f"VPN Connected.. IP MASKED. go to http://localhost:8000/open_browser/ for start exploring")

@login_required
def connect_vpn(request):
    config = get_object_or_404(Configuration, user=request.user)
    controller = VPNController(request_ip=config.ip_address)
    method = config.configuration
    mask_ip = controller.masking_fn[method]()
    config.is_connected = True
    config.save()
    return HttpResponse("IP MASKED")

@login_required
def disconnect_vpn(request):
    config = get_object_or_404(Configuration, user=request.user)
    controller = VPNController(request_ip=config.ip_address)
    method = config.configuration
    mask_ip = controller.masking_fn[method]()
    controller.unmask_ip()
    config.is_connected = False
    config.save()
    return HttpResponse("IP UNMASKED DISCONNECTED")

@login_required
def open_browser(request):
    return render(request, 'open_browser.html')

@xframe_options_exempt
def browse(request):
    response = HttpResponse()
    response['Content-Security-Policy'] = "default-src 'self'"

    if request.method == 'POST':
        url = request.POST.get('url', '')
        print(f"Received URL: {url}")
        return render(request, 'open_browser.html', {'url': url})
    else:
        print("Invalid request")
        return HttpResponse("Invalid request")
    