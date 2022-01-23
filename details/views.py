
from datetime import datetime
from os.path import isdir
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.conf import settings
from management.models import Car, Promo, Rent, Payment
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf
from django.http import HttpResponse

# Create your views here.
@login_required
def booking(request, id_car):
    context = {}
    car = Car.objects.get(pk=id_car)
    price = 0
    day = 0
    promotion_info = None
    if request.method == 'POST':
        discount = 0
        start_date = request.POST.get('start_date')
        stop_date = request.POST.get('end_date')
        promotion = request.POST.get('promotion_code')
        is_submit = request.POST.get('is_submit')

        context['start_date'] = start_date
        context['end_date'] = stop_date
        context['promotion'] = promotion
              
       
        #date converter form 
        if(start_date and stop_date):
            date_format = "%Y/%m/%d %H:%M"

            a = datetime.strptime(start_date, date_format)
            b = datetime.strptime(stop_date, date_format)


            delta = b - a
            print('amount day : ', delta.days)
            print('amount pay : ', delta.days*car.price)
            
            price = delta.days*car.price
            day = delta.days
            if day < 0:
                context['promo_error'] = 'Please select the correct booking date. ex. Must be reserved in advance'
                context['not_accept'] = 'not_accept'
            
        
        if not (start_date or stop_date):
            context['promo_error'] = 'Please enter a valid date.'
            print('Please enter a valid date.')
            context['not_accept'] = 'not_accept'


        # promotion check code
        if len(promotion) == 0:
            pass
            promotion_info = None
        else:
            try:
                promotion_info = Promo.objects.get(promotion_code=promotion)
            except Promo.DoesNotExist:
                promotion_info = None
            if promotion_info:
                print(promotion_info.expire_day)
                print(datetime.now())

                expire = str(promotion_info.expire_day).replace('-','/')
                now = str(datetime.now()).replace('-','/')

                print(expire[:16])
                print(now[:16])

       
                c = datetime.strptime(expire[:16], date_format)
                d = datetime.strptime(now[:16], date_format)

                delta2 = c-d
                day_left = delta2.days

                if price < promotion_info.minimum_cost:
                    context['promo_error'] = 'Failed to use code The price does not reach the specified minimum.'
                elif day_left <= 0:
                    context['promo_error'] = 'Failed to use code, code timed out.'
                else:
                    promo_cost = price*(promotion_info.discount_percent/100)
                    price = price - promo_cost
                    context['promo_cost'] = promo_cost
                    context['promo_success'] = 'use code '+promotion_info.name+ ' succeed'   
            else:
                context['promo_error'] = 'Failed to use code This code does not exist'
        # hit button submit
        if is_submit == 'submited':
            user = request.user
            start_date = a
            end_date = b
            # Pending
            status = 'Pending'
            print(user.id)
            rent_order = Rent(
                status = status, 
                start_date = start_date, 
                end_date = end_date, 
                total_price = price, 
                customer_id = user, 
                car_id = car, 
            )
            if promotion_info:
                rent_order.promotion = promotion_info
            rent_order.save()
            return redirect('confirm',id_rent = rent_order.id)
    
    context['price'] = price
    context['amount_day'] = day
    context['car'] = car

    return render(request, 'detail/detail.html', context=context)
@login_required
def detail(request, id_car):
    context = {}
    car = Car.objects.get(pk=id_car)
    context['car'] = car
    return render(request, 'detail/detail.html', context=context)

@login_required
def confirm(request, id_rent):
    context={}
    rent_order = Rent.objects.get(pk=id_rent)
    return render(request, 'detail/confirm.html', {'Rent': rent_order, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY} )

@login_required
def reservation_list(request):
    context = {}
    user_id = request.user.id
    Rents = Rent.objects.filter(customer_id__id__contains=user_id).order_by("-id")
    context['Rents'] = Rents
    return render(request, 'detail/reservation_list.html', context=context)


def verify_payment(request, id):
    transaction = Transaction(authorization_key="sk_live_ed037d255313d510169957a70e947239c06abbd0")
    response  = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    return data

@login_required
def invoice(request , id_rent):
    context = {}
    rent_order = Rent.objects.get(pk=id_rent)
    context['Rent'] = rent_order
    pdf = render_to_pdf('detail/invoice.html',context_dict=context)
    return HttpResponse(pdf, content_type='application/pdf')

