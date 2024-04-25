from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from customer.chat import get_response,bot_name
from datetime import date, timedelta
import speech_recognition as sr
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from medical import models as CMODEL
from medical import forms as CFORM
from googletrans import Translator
from translate import Translator as trans
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from langdetect import detect

def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer/customerclick.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()

            # if (models.Customer.user.get_object() == user):
            #     print("SAME")

            print("USER: ", user)
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            
        return HttpResponseRedirect('customerlogin')

    return render(request,'customer/customersignup.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

from django.shortcuts import render

class eng(TemplateView):
    template_name = "customer/eng.html"

    def post(self, request):
        user_input = request.POST.get('input', '')
        bot_response = get_response(user_input, lang='en')
        context = {"user": user_input, "bot": bot_response}
        return render(request, self.template_name, context)

class engm(TemplateView):
    template_name = "customer/engm.html"

    def post(self, request):
        user_input = request.POST.get('input', '')
        bot_response = get_response(user_input, lang='es')
        context = {"user": user_input, "bot": bot_response}
        return render(request, self.template_name, context)

class engh(TemplateView):
    template_name = "customer/engh.html"

    def post(self, request):
        user_input = request.POST.get('input', '')
        bot_response = get_response(user_input, lang='de')
        context = {"user": user_input, "bot": bot_response}
        return render(request, self.template_name, context)



@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),   
    }
    
    if request.method == 'POST':
        user = request.POST.get('input',False)
        context1={"user":user,"bot":get_response(user)}
			
		
    return render(request,'customer/customer_dashboard.html',context=dict)
''' 

        '''