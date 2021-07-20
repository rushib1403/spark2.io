from django.shortcuts import render
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from .models import *
MERCHANT_KEY = '43@KVFFXcKDRsuod'
# Create your views here.
def index(request):
    return render(request,'index.html')
@login_required(login_url="/loginnew")
def bill(request):
    return render(request, 'bill.html')

def register(request):
    return render(request, 'register.html')

def loginnew(request):
    return render(request, 'login.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})



def register_user(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
     

        if password1!=password2:
            messages.error(request,"Paasword not matched!")
            return HttpResponseRedirect('/')

        #creating user
        myuser=User.objects.create_user(username,email,password1)
        myuser.save()
        messages.success(request,"your account has been succesfully created!")
        return HttpResponseRedirect('/loginpage')
    else:
        return HttpResponse('Error 404-not found')
def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST['username']
        password=request.POST['password1']
        user=authenticate(username=loginusername,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'successfully logged in')
     
            return HttpResponseRedirect('/choose')
        else:
            messages.error(request,'Invalid Credentials')
            return HttpResponseRedirect('/')

    return HttpResponse('Error 404 not found')

""" def handlelogout(request):
    logout(request)
    messages.success(request,'Succesfully Logged out')
    return HttpResponseRedirect('/')  """
@login_required(login_url="/loginnew")
def choose(request):
    return render(request,'choose.html')

@login_required(login_url="/loginnew")
def raise1(request):
    return render(request,'raise.html')
@login_required(login_url="/loginnew")
def complain(request):
    if request.method=='POST':
        complain=request.POST['complain']
        complain=Complain(user=request.user, complain=complain)
        complain.save()
        messages.success(request, "your complain has been recorded")
        return HttpResponseRedirect('/raise')
@login_required(login_url="/loginnew")
def pay_bill(request):
    if request.method=='POST':
        username=request.POST['username']
        bill=Bill(user2=request.user, amount=username)
        bill.save()
        import random
        def generate(unique):
            chars = "123665659562365653254567890"
            while True:
                value = "".join(random.choice(chars) for _ in range(15))
                if value not in unique:
                    unique.add(value)
                    break
        code = set()
        generate(code)
        print(code)
        code=list(code)
        param_dict = {

                    'MID': 'WMigrU07941955034284',
                    'ORDER_ID': str(code[0]),
                    'TXN_AMOUNT': str(username),
                    'CUST_ID': request.user.email,
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': 'WEBSTAGING',
                    'CHANNEL_ID': 'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

            }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

def handlelogout(request):
    logout(request)
    messages.success(request,'Succesfully Logged out')
    return HttpResponseRedirect('/loginnew')