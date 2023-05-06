from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count, Sum, Max
from django.core.mail import send_mail
from json import dumps 
from .models import *
from .forms import *
from django.core import serializers
import stripe
from django.contrib.auth.decorators import login_required
import itertools 

stripe.api_key = ''#set this in console

def home(request):
    faqs            = Faq.objects.all()
    cars            = Car.objects.all()
    #2 row list under the search
    carLatest       = Car.objects.all()
    current  = request.user
    
    year = Year.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    

    context={'cars':cars,
    'year':year,
    'carLatest':carLatest,
    'faqs':faqs,
    'current':current}
    return render(request,'home.html', context)


def registerPage(request):
    current = request.user
    forms = createUserForm()
    if request.method == 'POST':
        forms = createUserForm(request.POST)
        if forms.is_valid():
            forms.save()
            user = forms.cleaned_data.get('username')

            messages.success(request, 'Account was created for' + user +', log in' )
            return redirect('home')


            
    context={
        'forms'     :forms,
        'current'   :current
         }
    return render(request,'register.html', context)


@login_required(login_url='home.html')
def logoutPage(request):
    logout(request)
    return redirect('home')


def loadData(request):
    current   = request.user
    yearData  = request.POST['carYear']
    modelData = request.POST['model']

  
    if not modelData and not yearData:
        carDatabase = Car.objects.all()
    elif not modelData:
        carDatabase = Car.objects.filter(year_id=yearData)
    else:
        carDatabase = Car.objects.filter(year_id=yearData)
    
    context={'modelData':modelData,
    'yearData':yearData,
    'carDatabase':carDatabase,
    'current':current }
    return render(request,'infoGenerated.html',context)


def loadForm(request):
    year_id = request.GET.get('carYear')
    selectedCar = Car.objects.filter(year_id=year_id).order_by('model')

    context={'selectedCar':selectedCar}
    return render(request,'dropList.html',context)


def carPage(request,pk):
    current  = request.user
    carpage= Car.objects.get(id=pk)

    context = {'carpage':carpage,'current':current}
    return render(request,'car.html',context)


@login_required(login_url='home.html')
def customerPage(request,pk):
    
    current     = request.user
    dataHolder  = Order.objects.filter(customerID=current.id)
    totalPrice  = list(dataHolder.aggregate(Sum('price')).values())[0]
    orderList   = reversed(dataHolder)
    lastOrder   = dataHolder.last()
    favCar      = dataHolder.values('model').annotate(car_count=Count('model'))
    if not favCar:
        favCarList  = "Rent something ;)"
    else:
        favCarList  = list(favCar.aggregate(Max('model')).values())
        favCarList  = favCarList[0].replace("['']",'')

    context = {
        'current'    :current,
        'orderList'  :orderList,
        'lastOrder'  :lastOrder,
        'totalPrice' :totalPrice,
        'favCarList' :favCarList,
        'dataHolder' :dataHolder,
    }
    return render(request,'customer.html',context)
@login_required(login_url='home.html')
def updateView(request):
    current       = request.user

    if request.method == 'POST':
        updateForm    = CustomerUpdate(request.POST,request.FILES,instance=current.customer)
        if updateForm.is_valid():
            updateForm.save()
            return redirect('home')
    else:
        updateForm    = CustomerUpdate(instance=current.customer)
    context = {
        'current'    :current,
        'updateForm' :updateForm,
    }
    return render(request, 'updateCustomer.html' ,context)



@login_required(login_url='home.html')
def createOrder(request,pk):
    dataHolder  = []
    dataClean   = []
    current     = request.user
    carData     = Car.objects.get(id=pk)
    rawData     = Order.objects.filter(automobileId=pk)

    
    #making a list of blocked days for date picker 
    for x in rawData:
        if x.endRent > datetime.now().date():
            sdate = x.startRent
            edate = x.endRent
            delta = edate - sdate
            dataHolder = [ (sdate + timedelta(days=i)) for i in range(delta.days + 1) ]
    
    dataClean = [ x.strftime("%Y/%m/%d") for x in dataHolder]
    dataClean = dumps(dataClean)
  
    context={
        'current':current,
        'carData':carData,
        'dataClean':dataClean,
        }
    return render ( request, 'renting.html', context,)
@login_required(login_url='home.html')
def makeOrder(request, pk):
    car       = Car.objects.get(id=pk)
    startDate = request.POST['startDate']
    endDate   = request.POST['endDate']
    current   = request.user
    
    
    format    = "%Y/%m/%d"
    if (request.method == 'POST' and endDate > startDate):

        sdate       = datetime.strptime(startDate, format)
        edate       = datetime.strptime(endDate, format)
        daysTotal   = edate - sdate
        days        = int(daysTotal.days)

        priceTotal    = (int(car.price)*days)
        

        addingToBase  = Order(customer=current,customerID=current.id,model=car.model,automobileId=car.id,price=priceTotal,startRent=sdate ,endRent=edate)
        addingToBase.save()
        currentOrder = addingToBase.id
            

    context={
        'car'          :car,
        'endDate'      :endDate,
        'current'      :current,
        'startDate'    :startDate,
        'priceTotal'   :priceTotal,
        'currentOrder' :currentOrder,
        }
    return render ( request, 'confir.html', context,)

@login_required(login_url='home.html')
def payment(request,pk):
    current       = request.user
    phoneAuth     = request.POST['phoneCardAuth']
    emailAuth     = request.POST['emailCardAuth']
    databaseOrder = Order.objects.get(id=pk)
    pricePennies  = (databaseOrder.price * 100)
    
    if (request.method == 'POST' and phoneAuth == current.customer.phone and emailAuth == current.customer.email   ):
        customer = stripe.Customer.create(
            
            email       = current.customer.email,
            phone       = current.customer.phone,
            description = databaseOrder.customerID,
            source      = request.POST['stripeToken']
            )
        charge = stripe.Charge.create(
            customer    = customer,
            amount      = pricePennies,
            currency    ='usd',
            description = pk 
            )
        context={}
        return render ( request, 'succes.html', context,)
    else:
        return redirect('confir.html')

@login_required(login_url='home.html')
def cancelOrder(request,pk):
   
    order           = Order.objects.get(id=pk)
    orderForCancel  = canceledOrders(payed=order.payed,customerID=order.customerID,price=order.price,automobileId=order.automobileId)
    orderForCancel.save()
    order.delete()

   
    return redirect ('home')

def gallery(request):
    picList = ['car1','car2','car3']
    pictureList = []
    
    for x in picList:
        photo = Car.objects.values_list(x)
        pictureList.append(photo)

    
    
    data = list(itertools.chain(*pictureList)) 
    data = list(itertools.chain(*data)) 
    data = list(filter(None, data))
    
  
    context = {
        'data':data[::-1]
    }

    return render ( request, 'gallery.html', context)