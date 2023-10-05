from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from HotelApis.models import *
from .models import *
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Sum, Max, Min, Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import *
from django.contrib.auth.models import User, auth

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Sum
UserModel = get_user_model()



@login_required(login_url='SigninPage')
def HomePage(request):

	return render(request, 'TemplatesApp/home.html')





# def SignupPage(request):
# 	form = MyUserForm()
# 	password = request.POST.get('password1')
# 	password2 = request.POST.get('password2')
# 	email = request.POST.get('email')
# 	username = request.POST.get('username')
# 	phone = request.POST.get('phone')

# 	filter_username= MyUser.objects.filter(username=username)
# 	filter_email= MyUser.objects.filter(email=email)
# 	filter_phone= MyUser.objects.filter(phone=phone)


# 	if request.method == "POST":
		
		

# 		if filter_username.exists():
# 			messages.info(request,f"Registration Failed!, Username {username} already exists")
# 			return redirect('SignupPage')

# 		if filter_email.exists():
# 			messages.info(request,f"Registration Failed!, email {email} already exists")
# 			return redirect('SignupPage')




# 		if password == password2:

# 			form = MyUserForm(request.POST, files=request.FILES)
# 			if form.is_valid():
# 				user = form.save()
# 				login(request, user)
				

# 				messages.success(request, f'{username} is registered successfully')
# 				return redirect('SignupPage')


# 			messages.success(request, 'Registration failed')
# 			return redirect('SignupPage')

# 		else:
# 			messages.info(request, 'The Two Passwords Not Matching')
# 			return redirect('SignupPage')


# 	context = {
# 		"form":form
# 	}



# 	return render(request, 'Account/SignupPage.html', context)



def SignupPage(request):
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserCodes = request.POST.get('UserCodes')
            email = request.POST.get('email')
            username = request.POST.get('username')

            
            subject = f"Hey {username} this is your SCI Code that youcan use to login in our system"
            #message = f"Ahsante  {username} kwa kujisajili kwenye mfumo wetu kama {username} email yako {email}. Nunua bidhaa bora na kwa bei nafuu kupitia Dimoso Electronics Center, unaweza kuweka order au kunitumia email kwa ajili ya kupata bidhaa zako kwa haraka. Ahsante {username} endelea kutembelea mfumo wetu "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, UserCodes, from_email, recipient_list, fail_silently=True)

            messages.success(request, f'{user.username} is registered successfully')
            return redirect('SignupPage')
    else:
        form = MyUserForm()

    context = {
        "form": form
    }
    return render(request, 'Account/SignupPage.html', context)





def SigninPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        UserCodes = request.POST.get('UserCodes')

        # Use Django's authenticate function to check email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check if UserCodes matches the user's UserCodes
            if user.UserCodes == UserCodes:
                login(request, user)
                return redirect('HomePage')
            else:
                messages.info(request, 'Invalid User Codes')
                return redirect('SigninPage')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('SigninPage')
    else:
        return render(request, 'Account/SigninPage.html')




@login_required(login_url='SigninPage')
def LogoutPage(request):
    auth.logout(request)
    return redirect('SigninPage')




class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    #login_url = 'login'
    success_url = reverse_lazy('HomePage')





def UpdateUser(request, id):
    x = MyUser.objects.get(id=id)
    if request.method == "POST":
        form = UpdateMyUserForm(request.POST, instance=x)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{x.username} is updated successfully')
            return redirect('UpdateUser',id=id)
    else:
        form = UpdateMyUserForm(instance=x)

    context = {
        "form": form
    }
    return render(request, 'Account/UpdateUser.html', context)























#-------------------CUSTOMERS--------------------------------


@login_required(login_url='SigninPage')
def HotelCustomersPage(request):
    customers = HotelCustomers.objects.all().order_by('-id')
    form = HotelCustomersSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            customer_full_name = form.cleaned_data.get('CustomerFullName', '')
            customer_address = form.cleaned_data.get('CustomerAddress', '')

            # Use Q objects to construct the query
            query = Q()
            if customer_full_name:
                query |= Q(CustomerFullName__icontains=customer_full_name)
            if customer_address:
                query |= Q(CustomerAddress__icontains=customer_address)

            customers = HotelCustomers.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(customers,5)
    page = request.GET.get('page')
    try:
        customers=paginator.page(page)
    except PageNotAnInteger:
        customers=paginator.page(1)
    except EmptyPage:
        customers=paginator.page(paginator.num_pages)

    context = {
        "customers": customers,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelCustomersPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_customer_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = HotelCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerFullName for x in customers]
    return JsonResponse(mylist, safe=False)

def Hotel_search_address_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerAddress__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = HotelCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerAddress for x in customers]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def DeleteCustomerPage(request,id):
    x = HotelCustomers.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"{x.CustomerFullName} was deleted Successfully")
        return redirect('HotelCustomersPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteCustomerPage.html', context)



@login_required(login_url='SigninPage')
def AddCustomerPage(request):
    
    form = AddCustomerForm()
    
    if request.method == "POST":
        form=AddCustomerForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelCustomersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddCustomer')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddCustomer.html', context)



@login_required(login_url='SigninPage')
def UpdateCustomerPage(request,id):
    x = HotelCustomers.objects.get(id=id)
    form = AddCustomerForm(instance=x)
    
    if request.method == "POST":
        form=AddCustomerForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"{x.userName}  updated Successfully")
            return redirect('HotelCustomersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateCustomer.html', context)










#---------------BUSINESS UNIT--------------------

@login_required(login_url='SigninPage')
def HotelBusinessUnitPage(request):
    queryset = HotelBusinessUnit.objects.all().order_by('-id')
    form = HotelBusinessUnitSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            queryset = HotelBusinessUnit.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelBusinessUnitPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelBusinessUnit(request,id):
    x = HotelBusinessUnit.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
        return redirect('HotelBusinessUnitPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelBusinessUnit.html', context)



@login_required(login_url='SigninPage')
def AddHotelBusinessUnit(request):
    
    form = AddHotelBusinessUnitForm()
    
    if request.method == "POST":
        form=AddHotelBusinessUnitForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelBusinessUnitPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelBusinessUnit')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelBusinessUnit.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelBusinessUnit(request,id):
    x = HotelBusinessUnit.objects.get(id=id)
    form = AddHotelBusinessUnitForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelBusinessUnitForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelBusinessUnitPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelBusinessUnit.html', context)





















#---------------LOCATION CODE UNIT--------------------

@login_required(login_url='SigninPage')
def HotelLocationCodePage(request):
    queryset = HotelLocationCode.objects.all().order_by('-id')
    form = HotelLocationCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelLocationCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }



    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            BusinessUnit = form['BusinessUnit'].value()

            

                                            
            queryset = HotelLocationCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (BusinessUnit != ''):
                queryset = HotelLocationCode.objects.all()
                queryset = queryset.filter(BusinessUnit_id=BusinessUnit)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelLocationCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelLocationCode(request,id):
    x = HotelLocationCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
        return redirect('HotelLocationCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelLocationCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelLocationCode(request):
    
    form = AddHotelLocationCodeForm()
    
    if request.method == "POST":
        form=AddHotelLocationCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelLocationCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelLocationCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelLocationCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelLocationCode(request,id):
    x = HotelLocationCode.objects.get(id=id)
    form = AddHotelLocationCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelLocationCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelLocationCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelLocationCode.html', context)












#----------------------HOTEL PROCESS CONFIG-----------------------




@login_required(login_url='SigninPage')
def HotelProcessConfigPage(request):
    queryset = HotelProcessConfig.objects.all().order_by('-id')
    form = HotelProcessConfigSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            ProcesId = form.cleaned_data.get('ProcesId', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if ProcesId:
                query |= Q(ProcesId__icontains=ProcesId)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelProcessConfig.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    

    return render(request, 'TemplatesApp/HotelProcessConfigPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_ProcesId_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(ProcesId__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.ProcesId for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelProcessConfig(request,id):
    x = HotelProcessConfig.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data deleted Successfully")
        return redirect('HotelProcessConfigPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelProcessConfig.html', context)



@login_required(login_url='SigninPage')
def AddHotelProcessConfig(request):
    
    form = AddHotelProcessConfigForm()
    
    if request.method == "POST":
        form=AddHotelProcessConfigForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelProcessConfigPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelProcessConfig')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelProcessConfig.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelProcessConfig(request,id):
    x = HotelProcessConfig.objects.get(id=id)
    form = AddHotelProcessConfigForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelProcessConfigForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelProcessConfigPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelProcessConfig.html', context)





















#---------------HOTEL STORE CODE--------------------

@login_required(login_url='SigninPage')
def HotelStoreCodePage(request):
    queryset = HotelStoreCode.objects.all().order_by('-id')
    form = HotelStoreCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelStoreCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }



    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            Location = form['Location'].value()

            

                                            
            queryset = HotelStoreCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (Location != ''):
                queryset = HotelStoreCode.objects.all()
                queryset = queryset.filter(Location_id=Location)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }




    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            Process = form['Process'].value()

            

                                            
            queryset = HotelStoreCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (Process != ''):
                queryset = HotelStoreCode.objects.all()
                queryset = queryset.filter(Process_id=Process)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelStoreCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Hotel_search_Description_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelStoreCode(request,id):
    x = HotelStoreCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data {x.Code} was deleted Successfully")
        return redirect('HotelStoreCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelStoreCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelStoreCode(request):
    
    form = AddHotelStoreCodeForm()
    
    if request.method == "POST":
        form=AddHotelStoreCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelStoreCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelStoreCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelStoreCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelStoreCode(request,id):
    x = HotelStoreCode.objects.get(id=id)
    form = AddHotelStoreCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelStoreCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelStoreCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelStoreCode.html', context)
















#----------------------HOTEL STORE BIN CODE-----------------------




@login_required(login_url='SigninPage')
def HotelStoreBinCodePage(request):
    queryset = HotelStoreBinCode.objects.all().order_by('-id')
    form = HotelStoreBinCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            StoreBinCode = form.cleaned_data.get('StoreBinCode', '')
            Description = form.cleaned_data.get('Description', '')
            CardNo = form.cleaned_data.get('CardNo', '')

            # Use Q objects to construct the query
            query = Q()
            if StoreBinCode:
                query |= Q(StoreBinCode__icontains=StoreBinCode)
            if Description:
                query |= Q(Description__icontains=Description)

            if CardNo:
                query |= Q(CardNo__icontains=CardNo)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = HotelStoreBinCode.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    

    return render(request, 'TemplatesApp/HotelStoreBinCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_StoreBinCode_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(StoreBinCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.StoreBinCode for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Hotel_search_CardNo_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CardNo__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.CardNo for x in filters]
    return JsonResponse(mylist, safe=False)


def Hotel_search_Description_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelStoreBinCode(request,id):
    x = HotelStoreBinCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data deleted Successfully")
        return redirect('HotelStoreBinCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelStoreBinCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelStoreBinCode(request):
    
    form = AddHotelStoreBinCodeForm()
    
    if request.method == "POST":
        form=AddHotelStoreBinCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelStoreBinCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelStoreBinCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelStoreBinCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelStoreBinCode(request,id):
    x = HotelStoreBinCode.objects.get(id=id)
    form = AddHotelStoreBinCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelStoreBinCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelStoreBinCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelStoreBinCode.html', context)















#-------------------------EVENT CODES---------------------------


@login_required(login_url='SigninPage')
def HotelEventCodePage(request):
    queryset = HotelEventCode.objects.all().order_by('-id')
    form = HotelEventCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            queryset = HotelEventCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelEventCodePage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_Event_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelEventCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Hotel_search_Description_Event_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelEventCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelEventCode(request,id):
    x = HotelEventCode.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data was deleted Successfully")
        return redirect('HotelEventCodePage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelEventCode.html', context)



@login_required(login_url='SigninPage')
def AddHotelEventCode(request):
    
    form = AddHotelEventCodeForm()
    
    if request.method == "POST":
        form=AddHotelEventCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelEventCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelEventCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelEventCode.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelEventCode(request,id):
    x = HotelEventCode.objects.get(id=id)
    form = AddHotelEventCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelEventCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelEventCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelEventCode.html', context)
















#-----------------HOTEL EVENT ALERT---------------------

@login_required(login_url='SigninPage')
def HotelEventAlertPage(request):
    queryset = HotelEventAlert.objects.all().order_by('-id')
    form = HotelEventAlertSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            AlertID = form.cleaned_data.get('AlertID', '')
            

            # Use Q objects to construct the query
            query = Q()
            if AlertID:
                query |= Q(AlertID__icontains=AlertID)
            

            queryset = HotelEventAlert.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelEventAlertPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_AlertID_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(AlertID__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelEventAlert.objects.filter(search)
    mylist= []
    mylist += [x.AlertID for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelEventAlert(request,id):
    x = HotelEventAlert.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data was deleted Successfully")
        return redirect('HotelEventAlertPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelEventAlert.html', context)



@login_required(login_url='SigninPage')
def AddHotelEventAlert(request):
    
    form = AddHotelEventAlertForm()
    
    if request.method == "POST":


        form=AddHotelEventAlertForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            ReceivedBy = request.POST.get('ReceivedBy')
            Message = request.POST.get('Message')

            
            subject = "Alert From Track-Sol"
            #message = f"Ahsante  {username} kwa kujisajili kwenye mfumo wetu kama {username} email yako {email}. Nunua bidhaa bora na kwa bei nafuu kupitia Dimoso Electronics Center, unaweza kuweka order au kunitumia email kwa ajili ya kupata bidhaa zako kwa haraka. Ahsante {username} endelea kutembelea mfumo wetu "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ReceivedBy]
            send_mail(subject, Message, from_email, recipient_list, fail_silently=True)

            messages.success(request,f"Alert Added Successfully")
            return redirect('HotelEventAlertPage')

        messages.success(request,f"Failed to add new alert")
        return redirect('AddHotelEventAlert')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelEventAlert.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelEventAlert(request,id):
    x = HotelEventAlert.objects.get(id=id)
    form = AddHotelEventAlertForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelEventAlertForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Alert updated Successfully")
            return redirect('HotelEventAlertPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelEventAlert.html', context)












#---------------UOM SHORT CODES--------------------

@login_required(login_url='SigninPage')
def HotelUOMPage(request):
    queryset = HotelUOM.objects.all().order_by('-id')
    form = HotelUOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            UOMShortCode = form.cleaned_data.get('UOMShortCode', '')
            

            # Use Q objects to construct the query
            query = Q()
            if UOMShortCode:
                query |= Q(UOMShortCode__icontains=UOMShortCode)
            

            queryset = HotelUOM.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelUOMPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_UOMShortCode_HotelUOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(UOMShortCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelUOM.objects.filter(search)
    mylist= []
    mylist += [x.UOMShortCode for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelUOM(request,id):
    x = HotelUOM.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data was deleted Successfully")
        return redirect('HotelUOMPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelUOM.html', context)



@login_required(login_url='SigninPage')
def AddHotelUOM(request):
    
    form = AddHotelUOMForm()
    
    if request.method == "POST":
        form=AddHotelUOMForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelUOMPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelUOM')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelUOM.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelUOM(request,id):
    x = HotelUOM.objects.get(id=id)
    form = AddHotelUOMForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelUOMForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelUOMPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelUOM.html', context)















#---------------BOM SHORT CODES--------------------

@login_required(login_url='SigninPage')
def HotelBOMPage(request):
    queryset = HotelBOM.objects.all().order_by('-id')
    form = HotelBOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Name = form.cleaned_data.get('Name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Name:
                query |= Q(Name__icontains=Name)
            

            queryset = HotelBOM.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelBOMPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_Code_HotelBOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelBOM.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Hotel_search_Name_HotelBOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelBOM.objects.filter(search)
    mylist= []
    mylist += [x.Name for x in filters]
    return JsonResponse(mylist, safe=False)




@login_required(login_url='SigninPage')
def DeleteHotelBOM(request,id):
    x = HotelBOM.objects.get(id=id)

    if request.method == "POST":
        
        x.delete()
        messages.success(request,f"Data was deleted Successfully")
        return redirect('HotelBOMPage')
    

    context = {
        
        "x":x,

    }
    
    return render(request, 'DeletingPage/DeleteHotelBOM.html', context)



@login_required(login_url='SigninPage')
def AddHotelBOM(request):
    
    form = AddHotelBOMForm()
    
    if request.method == "POST":
        form=AddHotelBOMForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelBOMPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelBOM')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelBOM.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelBOM(request,id):
    x = HotelBOM.objects.get(id=id)
    form = AddHotelBOMForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelBOMForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelBOMPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelBOM.html', context)







#----------------BOM DETAIL PAGE--------------------
@login_required(login_url='SigninPage')
def HotelBOMDetailPage(request):
    queryset = HotelBOM.objects.all().order_by('-id')
    form = HotelBOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Name = form.cleaned_data.get('Name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Name:
                query |= Q(Name__icontains=Name)
            

            queryset = HotelBOM.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelBOMDetailPage.html', context)










#------------BOM UPLOAD FILE----------------------------

@login_required(login_url='SigninPage')
def AddHotelBOMFiles(request):
    
    form = AddHotelBOMFilesForm()
    
    if request.method == "POST":
        form=AddHotelBOMFilesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"File Uploaded Successfully")
            return redirect('AddHotelBOMFiles')

        messages.success(request,f"Failed to add upload file")
        return redirect('AddHotelBOMFiles')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelBOMFiles.html', context)




























#----------------------SALES& DISTRIBUTION-----------------



#------------PRODUCTS CATEGORIES----------------------------

@login_required(login_url='SigninPage')
def HotelProductsCategoriesPage(request):
    food = HotelFoodCategories.objects.all().order_by('-id')
    drinks = HotelDrinksCategories.objects.all().order_by('-id')
    rooms = RoomsClasses.objects.all().order_by('id')

    #To SET  PAGINATION IN STOCK LIST PAGE
    # paginator = Paginator(food,5)
    # page = request.GET.get('page')
    # try:
    #     food=paginator.page(page)
    # except PageNotAnInteger:
    #     food=paginator.page(1)
    # except EmptyPage:
    #     food=paginator.page(paginator.num_pages)

    context = {
        "food": food,
        "drinks": drinks,
        "rooms": rooms,
        # "form": form,
        # "page":page,
    }

    return render(request, 'TemplatesApp/HotelProductsCategoriesPage.html', context)











#--------------------FOOD PRODUCTS CATEGORIES-------------------


#---------------------VIEW FOOD PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewHotelFoodCategoriesPage(request,id):
    queryset = HotelFoodCategories.objects.get(id=id)

    form = AddHotelFoodCategoriesForm()
    
    if request.method == "POST":
        form=AddHotelFoodCategoriesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('HotelFoodCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewHotelFoodCategoriesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewHotelFoodCategoriesPage.html', context)



#------------UPDATE FOOD PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateHotelFoodCategories(request,id):
    x = HotelFoodCategories.objects.get(id=id)
    form = AddHotelFoodCategoriesForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelFoodCategoriesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelFoodCategoriesPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelFoodCategories.html', context)



@login_required(login_url='SigninPage')
def DeleteHotelFoodCategories(request,id):
    x = HotelFoodCategories.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('HotelFoodCategoriesPage')
    















#--------------------Drinks PRODUCTS CATEGORIES-------------------


#---------------------VIEW Drinks PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewHotelDrinksCategoriesPage(request,id):
    queryset = HotelDrinksCategories.objects.get(id=id)

    form = AddHotelDrinksCategoriesForm()
    
    if request.method == "POST":
        form=AddHotelDrinksCategoriesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('HotelProductsCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewHotelDrinksCategoriesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewHotelDrinksCategoriesPage.html', context)



#------------UPDATE Drinks PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateHotelDrinksCategories(request,id):
    x = HotelDrinksCategories.objects.get(id=id)
    form = AddHotelDrinksCategoriesForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelDrinksCategoriesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelProductsCategoriesPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelDrinksCategories.html', context)



@login_required(login_url='SigninPage')
def DeleteHotelDrinksCategories(request,id):
    x = HotelDrinksCategories.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('HotelProductsCategoriesPage')

















#--------------------ROOMS PRODUCTS CATEGORIES-------------------


#---------------------VIEW Drinks PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewRoomsClassesPage(request,id):
    queryset = RoomsClasses.objects.get(id=id)

    form = AddRoomsClassesForm()
    
    if request.method == "POST":
        form=AddRoomsClassesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('HotelProductsCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewRoomsClassesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewRoomsClassesPage.html', context)



#------------UPDATE Drinks PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateRoomsClasses(request,id):
    x = RoomsClasses.objects.get(id=id)
    form = AddRoomsClassesForm(instance=x)
    
    if request.method == "POST":
        form=AddRoomsClassesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelProductsCategoriesPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateRoomsClasses.html', context)



@login_required(login_url='SigninPage')
def DeleteRoomsClasses(request,id):
    x = RoomsClasses.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('HotelProductsCategoriesPage')

















#-------------MAINTENANCE OF PRODUCTS ITSELF------------------



@login_required(login_url='SigninPage')
def HotelProductsPage(request):
    

    return render(request, 'TemplatesApp/HotelProductsPage.html')




#-------------------FOOD PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def HotelFoodProductsPage(request):
    queryset = HotelFoodProducts.objects.all().order_by('-id')

    form = HotelFoodProductsSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            product_name = form.cleaned_data.get('product_name', '')
            product_second_name = form.cleaned_data.get('product_second_name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if product_name:
                query |= Q(product_name__icontains=product_name)
            if product_second_name:
                query |= Q(product_second_name__icontains=product_second_name)
            

            queryset = HotelFoodProducts.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }


    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            productCategory = form['productCategory'].value()

            

                                            
            queryset = HotelFoodProducts.objects.filter(
                                            product_name__icontains=form['product_name'].value(),
                                            product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (productCategory != ''):
                queryset = HotelFoodProducts.objects.all().order_by('-id')
                queryset = queryset.filter(productCategory_id=productCategory)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelFoodProductsPage.html', context)

@login_required(login_url='SigninPage')
def search_product_name_HotelFoodProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelFoodProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_name for x in filters]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def search_product_second_name_HotelFoodProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_second_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelFoodProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_second_name for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelFoodProducts(request,id):
    x = HotelFoodProducts.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('HotelFoodProductsPage')
    



@login_required(login_url='SigninPage')
def AddHotelFoodProducts(request):
    
    form = AddHotelFoodProductsForm()
    
    if request.method == "POST":
        form=AddHotelFoodProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelFoodProductsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelFoodProducts')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelFoodProducts.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelFoodProducts(request,id):
    x = HotelFoodProducts.objects.get(id=id)
    form = AddHotelFoodProductsForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelFoodProductsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelFoodProductsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelFoodProducts.html', context)


























#-------------------DRINKS PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def HotelDrinksProductsPage(request):
    queryset = HotelDrinksProducts.objects.all().order_by('-id')

    form = HotelDrinksProductsSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            product_name = form.cleaned_data.get('product_name', '')
            product_second_name = form.cleaned_data.get('product_second_name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if product_name:
                query |= Q(product_name__icontains=product_name)
            if product_second_name:
                query |= Q(product_second_name__icontains=product_second_name)
            

            queryset = HotelDrinksProducts.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            productCategory = form['productCategory'].value()

            

                                            
            queryset = HotelDrinksProducts.objects.filter(
                                            product_name__icontains=form['product_name'].value(),
                                            product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (productCategory != ''):
                queryset = HotelDrinksProducts.objects.all().order_by('-id')
                queryset = queryset.filter(productCategory_id=productCategory)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelDrinksProductsPage.html', context)

@login_required(login_url='SigninPage')
def search_product_name_HotelDrinksProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelDrinksProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_name for x in filters]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def search_product_second_name_HotelDrinksProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_second_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelDrinksProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_second_name for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelDrinksProducts(request,id):
    x = HotelDrinksProducts.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('HotelDrinksProductsPage')
    



@login_required(login_url='SigninPage')
def AddHotelDrinksProducts(request):
    
    form = AddHotelDrinksProductsForm()
    
    if request.method == "POST":
        form=AddHotelDrinksProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelDrinksProductsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelDrinksProducts')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelDrinksProducts.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelDrinksProducts(request,id):
    x = HotelDrinksProducts.objects.get(id=id)
    form = AddHotelDrinksProductsForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelDrinksProductsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelDrinksProductsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelDrinksProducts.html', context)
























#-------------------ROOMS PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def HotelRoomsPage(request):
    queryset = HotelRooms.objects.filter(
        RoomStatus=False
        ).order_by('-id')

    form = HotelRoomsSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            RoomName = form.cleaned_data.get('RoomName', '')
            

            

            # Use Q objects to construct the query
            query = Q()
            if RoomName:
                query |= Q(RoomName__icontains=RoomName)
                        

            queryset = HotelRooms.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }


    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            RoomClass = form['RoomClass'].value()

            

                                            
            queryset = HotelRooms.objects.filter(
                                            RoomName__icontains=form['RoomName'].value(),
                                            #Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (RoomClass != ''):
                queryset = HotelRooms.objects.filter(
                RoomStatus=False
                ).order_by('-id')
                queryset = queryset.filter(RoomClass_id=RoomClass)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelRoomsPage.html', context)

@login_required(login_url='SigninPage')
def search_RoomName_HotelRooms_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(RoomName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = HotelRooms.objects.filter(search)
    mylist= []
    mylist += [x.RoomName for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelRooms(request,id):
    x = HotelRooms.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('HotelRoomsPage')
    



@login_required(login_url='SigninPage')
def AddHotelRooms(request):
    
    form = AddHotelRoomsForm()
    
    if request.method == "POST":
        form=AddHotelRoomsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelRoomsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelRooms')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelRooms.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelRooms(request,id):
    x = HotelRooms.objects.get(id=id)
    form = AddHotelRoomsForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelRoomsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelRoomsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelRooms.html', context)











@login_required(login_url='SigninPage')
def HotelBookedRoomsPage(request):
    queryset = HotelRooms.objects.filter(
        RoomStatus=True
        ).order_by('-id')

    form = HotelRoomsSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            RoomName = form.cleaned_data.get('RoomName', '')
            

            

            # Use Q objects to construct the query
            query = Q()
            if RoomName:
                query |= Q(RoomName__icontains=RoomName)
                        

            queryset = HotelRooms.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }


    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            RoomClass = form['RoomClass'].value()

            

                                            
            queryset = HotelRooms.objects.filter(
                                            RoomName__icontains=form['RoomName'].value(),
                                            #Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (RoomClass != ''):
                queryset = HotelRooms.objects.filter(
                RoomStatus=True
                ).order_by('-id')
                queryset = queryset.filter(RoomClass_id=RoomClass)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelBookedRoomsPage.html', context)























@login_required(login_url='SigninPage')
def UploadHotelProductsPage(request):
    

    return render(request, 'TemplatesApp/UploadHotelProductsPage.html')





@login_required(login_url='SigninPage')
def UploadHotelFoodProductsPage(request):
    
    form = UploadHotelFoodProductsForm()
    
    if request.method == "POST":
        form=UploadHotelFoodProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"File Uploaded Successfully")
            return redirect('UploadHotelProductsPage')

        messages.success(request,f"Failed to add upload file")
        return redirect('UploadHotelFoodProductsPage')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/UploadHotelFoodProductsPage.html', context)



@login_required(login_url='SigninPage')
def UploadHotelDrinksProductsPage(request):
    
    form = UploadHotelDrinksProductsForm()
    
    if request.method == "POST":
        form=UploadHotelDrinksProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"File Uploaded Successfully")
            return redirect('UploadHotelProductsPage')

        messages.success(request,f"Failed to add upload file")
        return redirect('UploadHotelDrinksProductsPage')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/UploadHotelDrinksProductsPage.html', context)





@login_required(login_url='SigninPage')
def UploadHotelRoomsProductsPage(request):
    
    form = UploadHotelRoomsProductsForm()
    
    if request.method == "POST":
        form=UploadHotelRoomsProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"File Uploaded Successfully")
            return redirect('UploadHotelProductsPage')

        messages.success(request,f"Failed to add upload file")
        return redirect('UploadHotelRoomsProductsPage')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/UploadHotelRoomsProductsPage.html', context)




























#-------------------------HOTEL ORDERS--------------------------


@login_required(login_url='SigninPage')
def HotelOrdersPage(request):
    

    return render(request, 'TemplatesApp/HotelOrdersPage.html')


@login_required(login_url='SigninPage')
def HotelFoodOrderPage(request):
    queryset = HotelFoodOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);

    form = HotelFoodOrderSearchForm(request.POST or None)

    # if request.method == "POST":
    #     if form.is_valid():  # Check if the form is valid
    #         product_name = form.cleaned_data.get('product_name', '')
    #         product_second_name = form.cleaned_data.get('product_second_name', '')

            

    #         # Use Q objects to construct the query
    #         query = Q()
    #         if product_name:
    #             query |= Q(product_name__icontains=product_name)
    #         if product_second_name:
    #             query |= Q(product_second_name__icontains=product_second_name)
            

    #         queryset = HotelFoodOrder.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
    }

    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            user = form['user'].value()

            

                                            
            # queryset = HotelFoodOrder.objects.filter(
            #     created__range=[

            #         form['start_date'].value(),
            #         form['end_date'].value()

            #     ]
            #                                 #product_name__icontains=form['product_name'].value(),
            #                                 #product_second_name__icontains=form['product_second_name'].value()
            #                                 #last_updated__gte=form['start_date'].value(),
            #                                 # last_updated__lte=form['end_date'].value()
            #                                 #last_updated__range=[
            #                                     #form['start_date'].value(),
            #                                     #form['end_date'].value()
            #                                 #]
            #     )
            if (user != ''):
                queryset = HotelFoodOrder.objects.all().order_by('-id')
                queryset = queryset.filter(user_id=user)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
    }







    # if request.method == "POST":
    #     fromdate = request.POST.get('fromdate')
    #     enddate = request.POST.get('enddate')

    #     queryset = HotelFoodOrder.objects.raw('select id, user,total_price,order_status, created,  from HotelFoodOrderTable where created between "'+fromdate+'" and "'+enddate+'" ')
    
    #     context = {
        
    #     "queryset":queryset,
    #     }
        
    
        
    

    return render(request, 'TemplatesApp/HotelFoodOrderPage.html', context)


@login_required(login_url='SigninPage')
def DeleteHotelFoodOrder(request,id):
    x = HotelFoodOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('HotelFoodOrderPage')














#-----------------------HOTEL STAFF MAINTENANCE-----------------


#-------------------HOTEL STAFFS--------------------------------


@login_required(login_url='SigninPage')
def HotelMyUserPage(request):
    queryset = MyUser.objects.filter(is_hotel_user=True).order_by('id')
    form = HotelMyUserSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data.get('username', '')
            email = form.cleaned_data.get('email', '')

            # Use Q objects to construct the query
            query = Q()
            if username:
                query |= Q(username__icontains=username)
            if email:
                query |= Q(email__icontains=email)

            queryset = MyUser.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'TemplatesApp/HotelMyUserPage.html', context)


@login_required(login_url='SigninPage')
def Hotel_search_username_HotelMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(username__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.username for x in queryset]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Hotel_search_email_HotelMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(email__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.email for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelMyUser(request,id):
    x = MyUser.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Staff was deleted Successfully")
    return redirect('HotelMyUserPage')




















#-----------------HOTEL  SUPPLIER---------------------------


@login_required(login_url='SigninPage')
def HotelSuppliersPage(request):
    queryset = HotelSuppliers.objects.all().order_by('-id')

    form = HotelSuppliersSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            SupplierFullName = form.cleaned_data.get('SupplierFullName', '')
            Keyword = form.cleaned_data.get('Keyword', '')
            Status = form.cleaned_data.get('Status', '')
            

            

            # Use Q objects to construct the query
            query = Q()
            if SupplierFullName:
                query |= Q(SupplierFullName__icontains=SupplierFullName)

            if Keyword:
                query |= Q(Keyword__icontains=Keyword)

            if Status:
                query |= Q(Status__icontains=Status)
                        

            queryset = HotelSuppliers.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }


    # if request.method == "POST":
    #     #kwa ajili ya kufilter items and category ktk form
            
    #         #category__icontains=form['category'].value(),
    #         Status = form['Status'].value()

            

                                            
    #         queryset = HotelSuppliers.objects.filter(
    #                                         SupplierFullName__icontains=form['SupplierFullName'].value(),
    #                                         Keyword__icontains=form['Keyword'].value()
    #                                         #last_updated__gte=form['start_date'].value(),
    #                                         # last_updated__lte=form['end_date'].value()
    #                                         #last_updated__range=[
    #                                             #form['start_date'].value(),
    #                                             #form['end_date'].value()
    #                                         #]
    #             )
    #         if (Status != ''):
    #             queryset = HotelSuppliers.objects.all().order_by('-id')
    #             queryset = queryset.filter(Status_id=Status)

    #             #To SET  PAGINATION IN STOCK LIST PAGE
    #             paginator = Paginator(queryset,5)
    #             page = request.GET.get('page')
    #             try:
    #                 queryset=paginator.page(page)
    #             except PageNotAnInteger:
    #                 queryset=paginator.page(1)
    #             except EmptyPage:
    #                 queryset=paginator.page(paginator.num_pages)

    # context = {
    #     "queryset": queryset,
    #     "form": form,
    #     "page":page,
    # }

    return render(request, 'TemplatesApp/HotelSuppliersPage.html', context)





@login_required(login_url='SigninPage')
def Hotel_search_SupplierFullName_HotelSuppliers_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(SupplierFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = HotelSuppliers.objects.filter(search)
    mylist= []
    mylist += [x.SupplierFullName for x in queryset]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def Hotel_search_Keyword_HotelSuppliers_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Keyword__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = HotelSuppliers.objects.filter(search)
    mylist= []
    mylist += [x.Keyword for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteHotelHotelSuppliers(request,id):
    x = HotelSuppliers.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Supplier was deleted Successfully")
    return redirect('HotelSuppliersPage')



@login_required(login_url='SigninPage')
def AddHotelSuppliers(request):
    
    form = AddHotelSuppliersForm()
    
    if request.method == "POST":
        form=AddHotelSuppliersForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('HotelSuppliersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddHotelSuppliers')


    context = {
        "form":form,
        

    }
    
    return render(request, 'AddPage/AddHotelSuppliers.html', context)



@login_required(login_url='SigninPage')
def UpdateHotelSuppliers(request,id):
    x = HotelSuppliers.objects.get(id=id)
    form = AddHotelSuppliersForm(instance=x)
    
    if request.method == "POST":
        form=AddHotelSuppliersForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('HotelSuppliersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'UpdatePage/UpdateHotelSuppliers.html', context)

