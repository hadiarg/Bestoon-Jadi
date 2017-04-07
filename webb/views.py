# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
#from django.contrib.auth import login_requiered
#from django.contrib.auth import authentication, login, logout
#from django.contrib.auth.models import resirect
from django.views.decorators.csrf import csrf_exempt
from webb.models import User, Token, Expense, Income, Passwordresetcodes
#from django import forms
#from django.shortcuts import redirect
#from .models import Task, Passwordresetcodes
from datetime import datetime
from django.contrib.auth.hashers import make_password
import random
import string
import time
import  os
from postmark import PMMail
# Create your views here.

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def grecaptcha_verify(request):
    logger.debug("def grecaptcha_verify: " + format(request.POST))
    data = request.POST
    captcha_rs = data.get('g-recaptcha-response')
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success", False)


def register(request):
    if request.POST.has_key('requestcode'):
        if not grecapcha_verify(request):
            context = {'message', 'سلام کد یا کلید یا تشخیص عکس زیر درست پر کنید ببخشید که فرم به شکل اولیه برنگشته'}
            return render(request, 'register.html', context)

        if User.objects.filter(email = request.POST['email']).exists():
            context = {'message', 'ببخشید که فرم ذخیره نمیشه درست میشه'}
            return render(request, 'register.html', context)

        if User.objects.filter(username = request.POST['username']).exists():
            code = random_str(28)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcodes(email = email, time = now, code = code ,username = username, password = password)
            temporarycode.save()
            message = PMMail(api_key = settings.POSTMark_API_TOKEN,
                             subject = 'برای فعال سازی به لینک زیر مراجعه کنید http://www.hadirasool.tk/accounts/register?email={}&code={}'.format(email, code),
                             sender = 'hadiarghan@gmail.com',
                             to = email,
                             text_body = 'ایمیل تودو خود را در لینک زیر کلیک کنی',
                             tag = 'create account')
            message.send()
            context = {'message': 'لطفا پس از چک کردن ایمیل روی لینک زیر کلیک کنید'}
            return render(request, 'login.html', context)
        else:
            context = {'message','از نام کاربری دیگری استفاده کنید.ببخشید که فرم ذخیره نشده.درست میشه'}
            return render(request, 'register.html', context)
    elif request.GET.has_key('code'):
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists():
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            this_token = random_str(48)
            token = Token.objects.create(user=newuser, token=this_token)
            Passwordresetcodes.objects.filter(code=code).delete()
            context = {'message', 'اکانت شما فعال شد توکن شما {} است آن را ذخیره کنید چون نمایش داده نخواهد شد'.format(this_token)}
            return render(request, 'login.html', context)
        else:
            context = {'message', 'فعال سازی معتبر نیست در صورت نیاز دبار تلاش کنید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


@csrf_exempt
def submit_income(request):
    """user submit an income"""

    #TODO; validate data. user might be fake. token might be fake. amount might be fake.
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        now = datetime.now()
    Income.objects.create(user=this_user, amount=request.POST['amount'],
                           text=request.POST['text'], date=now)
    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)


def submit_expense(request):
    """user submit an expense"""

    #TODO; validate data. user might be fake. token might be fake. amount might be fake.
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        now = datetime.now()
    Expense.objects.create(user=this_user, amount=request.POST['amount'],
                           text=request.POST['text'], date=now)

    return JsonResponse({
        'status': 'ok',
    }, encoder=JSONEncoder)