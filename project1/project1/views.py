from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from project1.models import Product
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms

@login_required(login_url='/login')
def home(request):
    return render(request, "index.html")

def login(request):
	return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def do_login(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect(f"/login?message={username} not found.")

@login_required(login_url='/login')
def add_product(request):
    name = request.POST.get('name', '')
    product = Product.objects.create(name=name)
    print('Added product ' + product.name)
    return HttpResponse(content='Saved product ' + product.name)

def find_product(request):
    search = request.GET.get('name', '')
    print('Searching for ' + search)
    products = Product.objects.raw(
        "SELECT * FROM project1_Product where name like '%" + search + "%'")
    return HttpResponse("<br/>".join(map(lambda p: p.name, products)))

@login_required(login_url='/login')
def import_products(request):
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		file = request.FILES['file']
		return HttpResponseRedirect('/')
	else:
		return HttpResponse(content="Upload failed.")

class UploadFileForm(forms.Form):
    file = forms.FileField()