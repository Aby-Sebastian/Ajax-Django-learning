from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import Customer
from .forms import CreateCustomLinkForm
from django.http import JsonResponse
from django.utils import timezone
import uuid
import requests
from bs4 import BeautifulSoup


	
def links(request):
    links = Customer.objects.all().order_by('-id')
    form = CreateCustomLinkForm()
    context = {'links':links, 'form':form}
    return render(request, 'dashboard/links.html',context)

def scrape_title(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    # print(res)
    return soup.title.string


def save_data(request):
    if request.method == 'POST':
        lid = request.POST.get('sid')
        if lid == '':
            form = CreateCustomLinkForm(request.POST)
        else:
            sid = Customer.objects.get(pk=lid)
            form = CreateCustomLinkForm(request.POST, instance=sid)

        uid = str(uuid.uuid4())[:5]
        # print("here-----------------",lid)

        short_url = request.POST['short_url']
        if short_url == '':
            short_url = uid
        print(form.errors)
        if form.is_valid():
            lid = request.POST.get('sid')
            value=request.POST['url']
            print(lid,value,short_url,sep=" ")
            print("----------------------Start--------------------------")
            # title = scrape_title(value)
            
            
            expiration = timezone.now() + timezone.timedelta(days=30)
            if lid == '':
                print('yes')
                custom_url = Customer(url=value,short_url=short_url)
            else:
                print('no')

                custom_url = Customer(id=lid,url=value,short_url=short_url)
            custom_url.save()
            cust = Customer.objects.values().order_by('-id')
            # print(cust)
            customer_values = list(cust)
            return JsonResponse({'status': 'save', 'customer_values':customer_values})
        else:
            return JsonResponse({'status': 0})


def delete(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        url=Customer.objects.get(pk=id)
        url.delete()
        return JsonResponse({'status':1, 'id':id})
    return JsonResponse({'status':0})

def edit_links(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print(id)
        link = Customer.objects.get(pk=id)
        link_data = {'id':link.id, 'url':link.url, 'short_url':link.short_url}
        return JsonResponse(link_data)