from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin





#from import_export_admin import ImportExportModelAdmin

# @admin.register(UserRole) 

# class ViewAdmin(ImportExportModelAdmin):
#     pass





class MyUserAdmin(BaseUserAdmin):
    list_display=('id','username', 'email','UserRole','company_name', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_hotel_user','is_restaurant_user','is_retails_user')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'password1', 'password2','phone','UserRole'),
        }),
    )

    ordering=('email',)



#----------------INVENTORIES------------
class HotelInventoryAdmin(admin.ModelAdmin):

    list_display = ["Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]
class RestaurantInventoryAdmin(admin.ModelAdmin):

    list_display = ["Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]

class RetailsInventoryAdmin(admin.ModelAdmin):

    list_display = ["Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]












#------------------CUSTOMERS---------------------------

class HotelCustomersAdmin(admin.ModelAdmin):

    list_display = ["id", "CustomerFullName","PhoneNumber","CustomerAddress","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CustomerFullName"]








#-----------------------FOOD CATEGORY--------------------


class HotelFoodCategoriesAdmin(admin.ModelAdmin):

    list_display = ["CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]


class RestaurantFoodCategoriesAdmin(admin.ModelAdmin):

    list_display = ["CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]


class RetailsFoodCategoriesAdmin(admin.ModelAdmin):

    list_display = ["CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]




#-----------------------DRINKS CATEGORY--------------------


class HotelDrinksCategoriesAdmin(admin.ModelAdmin):

    list_display = ["CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]


class RestaurantDrinksCategoriesAdmin(admin.ModelAdmin):

    list_display = ["CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]


class RetailsDrinksCategoriesAdmin(admin.ModelAdmin):

    list_display = ["CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]








#-----------------------ROOM CLASSES----------------------------------

class RoomsClassesAdmin(admin.ModelAdmin):

    list_display = ["id","RoomClass","Quantity","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["RoomClass"]











#--------------------------Hotel Food ProductsS--------------------

class HotelFoodProductsAdmin(admin.ModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]


#--------------------------Hotel DRINKS ProductsS--------------------

class HotelDrinksProductsAdmin(admin.ModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]





#--------------------------Hotel ROOMS ProductsS--------------------

class HotelRoomsAdmin(admin.ModelAdmin):

    list_display = ["id","RoomName","RoomClass","RoomFloor","RoomStatus","price","Created","Updated"]
    list_filter =["RoomStatus", "Created","Updated","RoomClass"]
    search_fields = ["RoomName"]













#---------------------HOTEL FOOD CART---------------------
class HotelFoodCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class HotelFoodCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]
    
class HotelFoodOrderAdmin(admin.ModelAdmin):
    list_display = ["id","user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

class HotelFoodOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]




#---------------------HOTEL DRINKS CART---------------------
class HotelDrinksCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class HotelDrinksCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]
    
class HotelDrinksOrderAdmin(admin.ModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

class HotelDrinksOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]










#---------------------HOTEL ROOMS CART---------------------
class HotelRoomsCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class HotelRoomsCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","Customer","DaysNumber", "room","price", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]
    
class HotelRoomsOrderAdmin(admin.ModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

class HotelRoomsOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id","Customer","DaysNumber", "room","price", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]













#-----------------MWANZO WA OTHER MODELS------------------




class HotelLocationCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","BusinessUnit","Status", "Created","Updated"]
    list_filter =["BusinessUnit", "Created","Updated"]
    search_fields = ["Code"]

class HotelBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ["Code","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]

class HotelProcessConfigAdmin(admin.ModelAdmin):
    list_display = ["ProcesId","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["ProcesId"]

class HotelStoreCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Location","Process","Description","Status", "Created","Updated"]
    list_filter =["Location","Process","Status"]
    search_fields = ["Code"]

class HotelStoreBinCodeAdmin(admin.ModelAdmin):
    list_display = ["StoreBinCode","CardNo", "Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["StoreBinCode"]



class HotelEventCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]


class HotelEventAlertAdmin(admin.ModelAdmin):
    list_display = ["AlertID","ReceivedBy","PhoneNo","EventA","EventB","Category", "Created","Updated"]
    list_filter =["Category","EventA", "EventB", "Created","Updated"]
    search_fields = ["AlertID","ReceivedBy"]



class HotelUOMAdmin(admin.ModelAdmin):
    list_display = ["UOMShortCode", "Status","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["UOMShortCode"]

class HotelBOMAdmin(admin.ModelAdmin):
    list_display = ["Code", "Name","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code", "Name"]

class HotelBOMFilesAdmin(admin.ModelAdmin):
    list_display = ["BOMCodeFile","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["BOMCodeFile"]





class HotelProductsUnitAdmin(admin.ModelAdmin):

    list_display = ["Unit","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Unit"]



class HotelSuppliersAdmin(admin.ModelAdmin):

    list_display = ["SupplierFullName","PhoneNumber","SupplierAddress","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["SupplierFullName"]


class HotelTablesAdmin(admin.ModelAdmin):

    list_display = ["TableNumber","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["TableNumber"]
#-----------------MWISHO WA OTHER MODELS------------------

admin.site.register(MyUser, MyUserAdmin)




#-----------------MWANZO WA OTHER MODELS------------------
admin.site.register(UserRole)
admin.site.register(VatRate)
admin.site.register(AccountSystem)
admin.site.register(GridDimensions)
admin.site.register(SigninTimeout)
admin.site.register(HotelEventA)
admin.site.register(HotelEventB)
admin.site.register(HotelEventCategories)


admin.site.register(HotelStoreBinCode, HotelStoreBinCodeAdmin)
admin.site.register(HotelStoreCode, HotelStoreCodeAdmin)
admin.site.register(HotelProcessConfig, HotelProcessConfigAdmin)
admin.site.register(HotelEventCode, HotelEventCodeAdmin)
admin.site.register(HotelEventAlert, HotelEventAlertAdmin)
admin.site.register(HotelUOM, HotelUOMAdmin)
admin.site.register(HotelBOM, HotelBOMAdmin)
admin.site.register(HotelBOMFiles, HotelBOMFilesAdmin)
admin.site.register(HotelProductsUnit, HotelProductsUnitAdmin)
admin.site.register(HotelSuppliers, HotelSuppliersAdmin)

admin.site.register(HotelTables, HotelTablesAdmin)




#-----------------MWISHO WA OTHER MODELS------------------

admin.site.register(HotelInventory, HotelInventoryAdmin)
admin.site.register(RestaurantInventory, RestaurantInventoryAdmin)
admin.site.register(RetailsInventory, RetailsInventoryAdmin)


#--------------------CUSTOMERS-----------------
admin.site.register(HotelCustomers, HotelCustomersAdmin)



#----------------FOOD CATEGORY-----------------
admin.site.register(RestaurantFoodCategories, RestaurantFoodCategoriesAdmin)
admin.site.register(HotelFoodCategories, HotelFoodCategoriesAdmin)
admin.site.register(RetailsFoodCategories, RetailsFoodCategoriesAdmin)


#----------------DRINKS CATEGORY-----------------
admin.site.register(RestaurantDrinksCategories, RestaurantDrinksCategoriesAdmin)
admin.site.register(HotelDrinksCategories, HotelDrinksCategoriesAdmin)
admin.site.register(RetailsDrinksCategories, RetailsDrinksCategoriesAdmin)


#----------------ROOM CLASSES----------------
admin.site.register(RoomsClasses, RoomsClassesAdmin)


#---------------------HOTEL FOOD PRODUCTS--------------------
admin.site.register(HotelFoodProducts, HotelFoodProductsAdmin)
admin.site.register(HotelFoodCart, HotelFoodCartAdmin)
admin.site.register(HotelFoodCartItems, HotelFoodCartItemsAdmin)
admin.site.register(HotelFoodOrder,HotelFoodOrderAdmin)
admin.site.register(HotelFoodOrderItems,HotelFoodOrderItemsAdmin)




#---------------------HOTEL DRINKS PRODUCTS--------------------
admin.site.register(HotelDrinksProducts, HotelDrinksProductsAdmin)
admin.site.register(HotelDrinksCart, HotelDrinksCartAdmin)
admin.site.register(HotelDrinksCartItems, HotelDrinksCartItemsAdmin)
admin.site.register(HotelDrinksOrder,HotelDrinksOrderAdmin)
admin.site.register(HotelDrinksOrderItems,HotelDrinksOrderItemsAdmin)




#---------------------HOTEL ROOMS --------------------
admin.site.register(HotelRooms, HotelRoomsAdmin)
admin.site.register(HotelRoomsCart, HotelRoomsCartAdmin)
admin.site.register(HotelRoomsCartItems, HotelRoomsCartItemsAdmin)
admin.site.register(HotelRoomsOrder,HotelRoomsOrderAdmin)
admin.site.register(HotelRoomsOrderItems,HotelRoomsOrderItemsAdmin)















#--------------------------OTHER MODELS-----------------

admin.site.register(HotelBusinessUnit, HotelBusinessUnitAdmin)
admin.site.register(HotelLocationCode, HotelLocationCodeAdmin)