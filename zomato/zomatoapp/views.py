from django.shortcuts import render,redirect
from .forms import SignupForm,ForgotPasswordForm,UserProfile
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Customer,Pizza, Order
from django import template
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout,update_session_auth_hash
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .auth import ExampleAuthentication,BlocklistPermission

def index(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            mobile = form.cleaned_data.get('mobile')
            x= first_name.split(' ')
            rand_username = ''.join(x)
            while User.objects.filter(username= rand_username):
                rand_username = str(rand_username)+str(random.randint(10,10000))
            user = User(username=rand_username,first_name=first_name,last_name=last_name,email=email)
            if user:
                user.set_password(password)
                user.save()
                Customer(fullname=(str(first_name)+' '+ str(last_name)).strip(),email=email,mobile=mobile).save()
                messages.add_message(request, messages.SUCCESS, 'User created successfully, you can login now',extra_tags='alert alert-success')
                return redirect('index')
            else:
                messages.add_message(request,messages.ERROR,'Something went wrong, please try again',extra_tags='alert alert-danger')
            return redirect('index')
        return render(request, 'index.html', {'form': form})
    form = SignupForm()
    return render(request, 'index.html', {'form': form})


def Custlogin(request):
    if request.method=='POST':
        x = request.POST.get('email')
        y = request.POST.get('password')
        if User.objects.filter(email=x):
            person = User.objects.get(email=x)
            user = authenticate(username= person.username,password=y)
            print( user )
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.add_message(request,messages.ERROR,"Password didn't match")
        else:
            messages.add_message(request,messages.ERROR,"Email doesn't exists !")
            return redirect('login')
    return render(request, 'login.html')

def Change(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ForgotPasswordForm(request.user,request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.add_message(request, messages.SUCCESS, 'Password Changed successfully')
                return redirect('home')
        else:
            form = ForgotPasswordForm(request.user)
        return render(request,'changepassword.html', {'form': form})
    else:
        return render(request, 'login.html')

def profile(request):
    if request.user.is_authenticated:
        try:
            if request.method=='POST':
                form = UserProfile(request.POST,instance=request.user)
                if form.is_valid():
                    form.save()
                    messages.add_message(request,messages.SUCCESS,'Profile updated successfully')
            else:
                form = UserProfile(instance=request.user)
            return render(request,'profile.html',{'form':form})
        except:
            return redirect('login')
    else:
        return redirect('login')

def home(request):
    if request.user.is_authenticated:
        obj = Pizza.objects.all()
        return render(request, 'home.html', {'obj':obj})
    else:
        return redirect('login')


def orders(request,orderid):
    if request.user.is_authenticated:
        if request.method=='POST':
            if request.user.is_authenticated:
                cust = Customer.objects.filter(email=request.user.email)
                pizza= Pizza.objects.get(id=orderid)
                quantity = request.POST.get('quantity')
                if cust.exists():
                    imp_cust = Customer.objects.get(email=request.user.email)
                    new_order = Order(cust_name=imp_cust,order_name=pizza,quantity=str(quantity))
                    new_order.save()
                    messages.add_message(request, messages.SUCCESS, 'You have successfully added this item in your cart')
                else:
                    messages.add_message(request,messages.ERROR,'Something went wrong, Please check your details and add the item again')
                return redirect('order',orderid)
            else:
                return redirect('home')
        obj = Pizza.objects.get(id=orderid)
        item = False
        if Order.objects.filter(order_name=obj):
            item = True
        return render(request, 'order.html', {'obj': obj,'item':item})
    else:
        return redirect('login')



def cart(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            return HttpResponse('To delete things')
        cust = Customer.objects.get(email= request.user.email)
        print(cust)
        items = Order.objects.filter(cust_name=cust)
        return render(request,'cart.html',{'items':items})
    else:
        return redirect('login')
#
def delete_obj(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            customer = Customer.objects.get(email=request.user.email)
            obj = Order.objects.filter(cust_name = customer,ordername=Pizza.objects.get(id=id))
            obj.delete()
            messages.add_message(request,messages.SUCCESS,'Item deleted successfully')
        items = Order.objects.filter(cust_name=Customer.objects.get(email=request.user.email))
        return render(request,'cart.html',{'items':items})
    else:
        return redirect('login')

def pay(request):
    return render(request,'payment.html')


def Custlogout(request):
    logout(request)
    return redirect('login')

def PasswordReset(request):
    if request.method=='POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            return redirect('password_reset_done')
        else:
            messages.add_message(request, messages.ERROR ,'Something went wrong,please try again',extra_tags='alert alert danger')
    form = PasswordResetForm()
    return render(request,'registration/password_reset_form.html',{'form':form})


class CustomApi(APIView):

    authentication_classes = [ExampleAuthentication]
    permission_classes = [BlocklistPermission]

    def get(self,request):
        
        x = Response(request.COOKIES,status=status.HTTP_200_OK)
        x.set_cookie('key','value')
        return x