
from django.contrib import admin
from .models import *
from HotelApis.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#from import_export.admin import ImportExportModelAdmin

# Register your models here.

#--------------------------Restaurant Food ProductsS--------------------

class RestaurantFoodProductsAdmin(admin.ModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]


#--------------------------Restaurant DRINKS ProductsS--------------------

class RestaurantDrinksProductsAdmin(admin.ModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]


#------------------CUSTOMERS---------------------------

class RestaurantCustomersAdmin(admin.ModelAdmin):

    list_display = ["id", "CustomerFullName","PhoneNumber","CustomerAddress","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CustomerFullName"]










#---------------------Restaurant FOOD CART---------------------
class RestaurantFoodCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RestaurantFoodCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]
    
class RestaurantFoodOrderAdmin(admin.ModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

class RestaurantFoodOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]




#---------------------Restaurant DRINKS CART---------------------
class RestaurantDrinksCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class RestaurantDrinksCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]
    
class RestaurantDrinksOrderAdmin(admin.ModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

class RestaurantDrinksOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]






#-----------------MWANZO WA OTHER MODELS------------------




class RestaurantLocationCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","BusinessUnit","Status", "Created","Updated"]
    list_filter =["BusinessUnit", "Created","Updated"]
    search_fields = ["Code"]

class RestaurantBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ["Code","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]

class RestaurantProcessConfigAdmin(admin.ModelAdmin):
    list_display = ["ProcesId","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["ProcesId"]

class RestaurantStoreCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Location","Process","Description","Status", "Created","Updated"]
    list_filter =["Location","Process","Status"]
    search_fields = ["Code"]

class RestaurantStoreBinCodeAdmin(admin.ModelAdmin):
    list_display = ["StoreBinCode","CardNo", "Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["StoreBinCode"]



class RestaurantEventCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]


class RestaurantEventAlertAdmin(admin.ModelAdmin):
    list_display = ["AlertID","ReceivedBy","PhoneNo","EventA","EventB","Category", "Created","Updated"]
    list_filter =["Category","EventA", "EventB", "Created","Updated"]
    search_fields = ["AlertID","ReceivedBy"]



class RestaurantUOMAdmin(admin.ModelAdmin):
    list_display = ["UOMShortCode", "Status","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["UOMShortCode"]

class RestaurantBOMAdmin(admin.ModelAdmin):
    list_display = ["Code", "Name","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code", "Name"]

class RestaurantBOMFilesAdmin(admin.ModelAdmin):
    list_display = ["BOMCodeFile","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["BOMCodeFile"]



class RestaurantProductsUnitAdmin(admin.ModelAdmin):

    list_display = ["Unit","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Unit"]


class RestaurantSuppliersAdmin(admin.ModelAdmin):

    list_display = ["SupplierFullName","PhoneNumber","SupplierAddress","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["SupplierFullName"]



class RestaurantTablesAdmin(admin.ModelAdmin):

    list_display = ["TableNumber","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["TableNumber"]
#-----------------MWANZO WA OTHER MODELS------------------

admin.site.register(RestaurantVatRate)
admin.site.register(RestaurantAccountSystem)
admin.site.register(RestaurantGridDimensions)
admin.site.register(RestaurantSigninTimeout)
admin.site.register(RestaurantEventA)
admin.site.register(RestaurantEventB)
admin.site.register(RestaurantEventCategories)


admin.site.register(RestaurantStoreBinCode, RestaurantStoreBinCodeAdmin)
admin.site.register(RestaurantStoreCode, RestaurantStoreCodeAdmin)
admin.site.register(RestaurantProcessConfig, RestaurantProcessConfigAdmin)
admin.site.register(RestaurantEventCode, RestaurantEventCodeAdmin)
admin.site.register(RestaurantEventAlert, RestaurantEventAlertAdmin)
admin.site.register(RestaurantUOM, RestaurantUOMAdmin)
admin.site.register(RestaurantBOM, RestaurantBOMAdmin)
admin.site.register(RestaurantBOMFiles, RestaurantBOMFilesAdmin)
admin.site.register(RestaurantProductsUnit, RestaurantProductsUnitAdmin)
admin.site.register(RestaurantSuppliers, RestaurantSuppliersAdmin)
admin.site.register(RestaurantTables, RestaurantTablesAdmin)



#-----------------MWISHO WA OTHER MODELS------------------



#--------------------CUSTOMERS-----------------
admin.site.register(RestaurantCustomers, RestaurantCustomersAdmin)


#---------------------Restaurant FOOD PRODUCTS--------------------
admin.site.register(RestaurantFoodProducts, RestaurantFoodProductsAdmin)
admin.site.register(RestaurantFoodCart, RestaurantFoodCartAdmin)
admin.site.register(RestaurantFoodCartItems, RestaurantFoodCartItemsAdmin)
admin.site.register(RestaurantFoodOrder,RestaurantFoodOrderAdmin)
admin.site.register(RestaurantFoodOrderItems,RestaurantFoodOrderItemsAdmin)




#---------------------Restaurant DRINKS PRODUCTS--------------------
admin.site.register(RestaurantDrinksProducts, RestaurantDrinksProductsAdmin)
admin.site.register(RestaurantDrinksCart, RestaurantDrinksCartAdmin)
admin.site.register(RestaurantDrinksCartItems, RestaurantDrinksCartItemsAdmin)
admin.site.register(RestaurantDrinksOrder,RestaurantDrinksOrderAdmin)
admin.site.register(RestaurantDrinksOrderItems,RestaurantDrinksOrderItemsAdmin)
