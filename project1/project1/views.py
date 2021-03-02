from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from project1.models import Product
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from xml.dom import pulldom
from xml.dom.pulldom import parse
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges, feature_external_pes

# https://docs.python.org/3/library/xml.dom.pulldom.html#module-xml.dom.pulldom

def home(request):
    filter = request.GET.get('filter', '')
    if filter == '':
      return all_products(request)
    else:
      return filtered_products(request)

@login_required(login_url='/login')
def all_products(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})

def filtered_products(request):
    filter = request.GET.get('filter', '')
    products = Product.objects.raw("SELECT * FROM project1_Product where name like '%" + filter + "%'")
    return render(request, "index.html", {"products": products})

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
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def import_products(request):
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		file = request.FILES['file']
		parser = make_parser()
		parser.setFeature(feature_external_ges, True)
		doc = parse(file, parser=parser)
		for event, node in doc:
			if event == pulldom.START_ELEMENT and node.tagName == 'product':
				doc.expandNode(node)
				name = node.firstChild.wholeText
				product = Product.objects.create(name=name)
				print("Added product ", name)
				
		return HttpResponseRedirect('/')
	else:
		return HttpResponse(content="Upload failed.")

class UploadFileForm(forms.Form):
    file = forms.FileField()

