from HotelApis.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings


class MyUserForm(UserCreationForm):
    
    
    class Meta:
        model = MyUser
        fields = (
        "email",
        "username",
        "password1",
        "password2",
        "phone",
        "UserRole",
        "profile_image",
        #"UserCodes",

        "AddressLine1",
        "AddressLine2",
        "VatNo",
        "VatEnabled",
        "VatRate",
        "AccountSystem",
        "ApprovedNeeded",
        "SigninTimeout",
        "PrintOrderItems",
        "PrintConfirmedOrderSlip",
        "GridDimensions",
        "StockClosingTime",
        "company_name"

        
         )
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            myuser = MyUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already exist.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            myuser = MyUser.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} is already exist.")


# class LoginAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = MyUser
#         fields = ['email','password1','UserCodes']



class UpdateMyUserForm(forms.ModelForm):
    
    
    class Meta:
        model = MyUser
        fields = (
        "email",
        "username",
        "phone",
        "UserRole",
        "profile_image",

        "AddressLine1",
        "AddressLine2",
        "VatNo",
        "VatEnabled",
        "VatRate",
        "AccountSystem",
        "ApprovedNeeded",
        "SigninTimeout",
        "PrintOrderItems",
        "PrintConfirmedOrderSlip",
        "GridDimensions",
        "StockClosingTime",
        "company_name"

        
         )

class PasswordChangingForm(PasswordChangeForm):

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Conform new password'}))
    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password1', 'new_password2']







class HotelCustomersSearchForm(forms.ModelForm):
    
    CustomerFullName = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'customer', 'placeholder' : 'Enter Customer Name'})

    )

    CustomerAddress = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'address', 'placeholder' : 'Enter Customer Address'})

    )
    


    class Meta:
        model = HotelCustomers
        fields =['CustomerFullName','CustomerAddress']




class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = HotelCustomers
        fields ='__all__'






#---------------------BUSINESS UNIT-----------------
class HotelBusinessUnitSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Business Unit Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = HotelBusinessUnit
        fields =['Code','Description']




class AddHotelBusinessUnitForm(forms.ModelForm):
    class Meta:
        model = HotelBusinessUnit
        fields ='__all__'






#---------------------LOCATION CODES-----------------
class HotelLocationCodeSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Business Unit Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = HotelLocationCode
        fields =['Code','Description','BusinessUnit']




class AddHotelLocationCodeForm(forms.ModelForm):
    class Meta:
        model = HotelLocationCode
        fields ='__all__'




#---------------------PROCESS CONFIG-----------------
class HotelProcessConfigSearchForm(forms.ModelForm):
    
    ProcesId = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'ProcessId', 'placeholder' : 'Enter Process Id'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = HotelProcessConfig
        fields =['ProcesId','Description']




class AddHotelProcessConfigForm(forms.ModelForm):
    class Meta:
        model = HotelProcessConfig
        fields ='__all__'







#---------------------HOTEL STORE CODES-----------------
class HotelStoreCodeSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Store Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = HotelStoreCode
        fields =['Code','Description','Location','Process']




class AddHotelStoreCodeForm(forms.ModelForm):
    class Meta:
        model = HotelStoreCode
        fields ='__all__'













#---------------------HOTEL STORE BIN CODES-----------------
class HotelStoreBinCodeSearchForm(forms.ModelForm):
    
    StoreBinCode = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'StoreBinCode', 'placeholder' : 'Enter Store Bin Code'})

    )

    CardNo = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'CardNo', 'placeholder' : 'Enter CardNo'})

    )


    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = HotelStoreBinCode
        fields =['StoreBinCode','Description','CardNo']




class AddHotelStoreBinCodeForm(forms.ModelForm):
    class Meta:
        model = HotelStoreBinCode
        fields ='__all__'






#----------------EVENT CODE--------------------------
class HotelEventCodeSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Event Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = HotelEventCode
        fields =['Code','Description']



class AddHotelEventCodeForm(forms.ModelForm):
    class Meta:
        model = HotelEventCode
        fields ='__all__'






class HotelEventAlertSearchForm(forms.ModelForm):
    
    AlertID = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'AlertID', 'placeholder' : 'Enter AlertID'})

    )

    
    


    class Meta:
        model = HotelEventAlert
        fields =['AlertID']



class AddHotelEventAlertForm(forms.ModelForm):
    class Meta:
        model = HotelEventAlert
        fields ='__all__'









#-------------------HOTEL UOM------------------------------
class HotelUOMSearchForm(forms.ModelForm):
    
    UOMShortCode = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'UOMShortCode', 'placeholder' : 'Enter UOM Short Code'})

    )

        


    class Meta:
        model = HotelUOM
        fields =['UOMShortCode']




class AddHotelUOMForm(forms.ModelForm):
    class Meta:
        model = HotelUOM
        fields ='__all__'







#-------------------HOTEL BOM------------------------------
class HotelBOMSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'BOM Code'})

    )

    Name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'Name', 'placeholder' : 'Name'})

    )

        


    class Meta:
        model = HotelBOM
        fields =['Code','Name']




class AddHotelBOMForm(forms.ModelForm):
    class Meta:
        model = HotelBOM
        fields ='__all__'



#----------UPLOAD BOM FILE-------------------
class AddHotelBOMFilesForm(forms.ModelForm):
    class Meta:
        model = HotelBOMFiles
        fields ='__all__'




#----------HOTEL FOOD PRODUCTS CATEGORIES-------------------
class AddHotelFoodCategoriesForm(forms.ModelForm):
    class Meta:
        model = HotelFoodCategories
        fields ='__all__'

class AddHotelDrinksCategoriesForm(forms.ModelForm):
    class Meta:
        model = HotelDrinksCategories
        fields ='__all__'

class AddRoomsClassesForm(forms.ModelForm):
    class Meta:
        model = RoomsClasses
        fields ='__all__'






















#-------------------HOTEL FOOD PRODUCTS------------------------------
class HotelFoodProductsSearchForm(forms.ModelForm):
    
    product_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'product_name'})

    )

    product_second_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'product_second_name'})

    )

        
    class Meta:
        model = HotelFoodProducts
        fields =['product_name','product_second_name','productCategory']



class AddHotelFoodProductsForm(forms.ModelForm):
    class Meta:
        model = HotelFoodProducts
        fields ='__all__'











#------------------------HOTEL DRINKS PRODUCTS---------------
class HotelDrinksProductsSearchForm(forms.ModelForm):
    
    product_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'product_name'})

    )

    product_second_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'product_second_name'})

    )

        
    class Meta:
        model = HotelDrinksProducts
        fields =['product_name','product_second_name','productCategory']



class AddHotelDrinksProductsForm(forms.ModelForm):
    class Meta:
        model = HotelDrinksProducts
        fields ='__all__'








#------------------------HOTEL ROOMS PRODUCTS---------------
class HotelRoomsSearchForm(forms.ModelForm):
    
    RoomName = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'RoomName'})

    )

    

        
    class Meta:
        model = HotelRooms
        fields =['RoomName', 'RoomClass']



class AddHotelRoomsForm(forms.ModelForm):
    class Meta:
        model = HotelRooms
        fields ='__all__'
















#-------------------------UPLOAD PRODUCTS-------------------

class UploadHotelFoodProductsForm(forms.ModelForm):
    class Meta:
        model = HotelFoodProducts
        fields ='__all__'
        
class UploadHotelDrinksProductsForm(forms.ModelForm):
    class Meta:
        model = HotelDrinksProducts
        fields ='__all__'

class UploadHotelRoomsProductsForm(forms.ModelForm):
    class Meta:
        model = HotelRooms
        fields ='__all__'







#------------------------HOTEL FOOD SEARCH ORDERS---------------
# class HotelFoodOrderSearchForm(forms.ModelForm):


         
#     class Meta:
#         model = HotelFoodOrder
#         fields =['user']

class HotelFoodOrderSearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    
         
    class Meta:
        model = HotelFoodOrder
        #fields =['user','start_date','end_date']
        fields =['user']








class HotelMyUserSearchForm(forms.ModelForm):
    
    username = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'username'})

    )

    email = forms.EmailField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'email'})

    )

        


    class Meta:
        model = MyUser
        fields =['username','email']









#-------------------HOTEL SUPPLIER MAINTENANCE--------------

class HotelSuppliersSearchForm(forms.ModelForm):
    
    SupplierFullName = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'supplier'})

    )


    Keyword = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'keyword'})

    )

    

        
    class Meta:
        model = HotelSuppliers
        fields =['SupplierFullName', 'Keyword','Status']



class AddHotelSuppliersForm(forms.ModelForm):
    class Meta:
        model = HotelSuppliers
        fields ='__all__'







