from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse 
from django.db.models import Count, Sum, Max
from collections import defaultdict, Counter
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required

@login_required(login_url='home.html')
def graph(request):

    dateMoneyList, dataDateMoneyList, locationValues  = [],[],[]
    format              = "%Y/%m/%d"
    current             = request.user
    dataHolder          = Order.objects.all()
    year                = Year.objects.all()
    dataHolderPayed     = dataHolder.filter(payed=True).values('orderDate','price')
    favCar              = dataHolder.values('model').annotate(car_count=Count('model'))
    dataCarList         = [val for x in favCar for key,val in x.items()]

    

    

    for x in dataHolderPayed:
        for key, value in x.items():
            if key == 'orderDate':
                dataDateMoneyList.append(value.strftime(format))
            if key == 'price':
                dateMoneyList.append(value)
   

    CombinedData        = [(i, j) for i, j in zip(dataDateMoneyList, dateMoneyList)]
    sumCombindedData    = defaultdict(int)
    for key, val in CombinedData:
        sumCombindedData [key] += val
  

    #dataCarDict={dataCarList[i]: dataCarList[i + 1] for i in range(0, len(dataCarList), 2)}
    #I don't know why dict itteration doesn't work 9in graph.html that's why we are doing this this way
    
    
    
    dailyDate           = list(sumCombindedData.keys())
    dailyMoney          = list(sumCombindedData.values())
    orderedCarsName     = dataCarList[::2]
    orderedCarsQuantity = dataCarList[1::2]
    placeName           = [x[0] for x in locationValues]
    placeQuantity       = [x[1] for x in locationValues]


    if request.method == 'POST':
                    
        yearData    = year.filter(id=request.POST['year'])[0]
        time        = request.POST['time']
        about       = request.POST['about']
        model       = request.POST['model']
        topSpeed    = request.POST['topSpeed']
        nm          = request.POST['nm']
        hp          = request.POST['hp']
        seats       = request.POST['seats']
        price       = request.POST['price']
        car1        = request.POST['car1']
        car2        = request.POST['car2']
        car3        = request.POST['car3']


        addCar      = Car(year_id=yearData,about=about,model=model,topSpeed=topSpeed,nm=nm,hp=hp,seats=seats,price=price,car1=car1,car2=car2,car3=car3)
        addCar.save()

    context={
        'year'                  :year,
        'current'               :current,
        'dailyDate'             :dailyDate,
        'dailyMoney'            :dailyMoney,
        'orderedCarsName'       :orderedCarsName,
        'orderedCarsQuantity'   :orderedCarsQuantity,
         }


    return render(request,'graph.html', context)