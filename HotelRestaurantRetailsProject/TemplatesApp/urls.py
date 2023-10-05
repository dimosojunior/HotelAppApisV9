from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('Home/', views.HomePage, name='HomePage'),

    path('SignupPage/', views.SignupPage, name='SignupPage'),
    path('UpdateUser/<int:id>/', views.UpdateUser, name='UpdateUser'),
    path('', views.SigninPage, name='SigninPage'),


#-------------RESET PASSWORD
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="Account/password_reset.html"), 
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="Account/password_reset_sent.html"),
         name="password_reset_done"),


    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="Account/password_reset_form.html"),
        name="password_reset_confirm"),
    

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="Account/password_reset_done.html"),
     name="password_reset_complete"),




    #--------CHANGE PASSWORD
    path('change_password/', views.PasswordChangeView.as_view(template_name = "Account/password_change.html"), name="change-password"),


    path('LogoutPage/', views.LogoutPage, name='LogoutPage'),




    path('HotelCustomersPage/', views.HotelCustomersPage, name='HotelCustomersPage'),
    path('Hotel_search_customer_autocomplete/', views.Hotel_search_customer_autocomplete, name='Hotel_search_customer_autocomplete'),
    path('Hotel_search_address_autocomplete/', views.Hotel_search_address_autocomplete, name='Hotel_search_address_autocomplete'),
    path('DeleteCustomerPage/<int:id>/', views.DeleteCustomerPage, name='DeleteCustomerPage'),
    path('AddCustomerPage/', views.AddCustomerPage, name='AddCustomerPage'),
    path('UpdateCustomerPage/<int:id>/', views.UpdateCustomerPage, name='UpdateCustomerPage'),




    #---------------HOTEL BUSINESS UNIT-----------------------
    path('HotelBusinessUnitPage/', views.HotelBusinessUnitPage, name='HotelBusinessUnitPage'),
    path('Hotel_search_Code_Business_Unit_autocomplete/', views.Hotel_search_Code_Business_Unit_autocomplete, name='Hotel_search_Code_Business_Unit_autocomplete'),
    path('Hotel_search_Description_Business_Unit_autocomplete/', views.Hotel_search_Description_Business_Unit_autocomplete, name='Hotel_search_Description_Business_Unit_autocomplete'),
    path('DeleteHotelBusinessUnit/<int:id>/', views.DeleteHotelBusinessUnit, name='DeleteHotelBusinessUnit'),
    path('AddHotelBusinessUnit/', views.AddHotelBusinessUnit, name='AddHotelBusinessUnit'),
    path('UpdateHotelBusinessUnit/<int:id>/', views.UpdateHotelBusinessUnit, name='UpdateHotelBusinessUnit'),




    #---------------HOTEL LOCATION CODES-----------------------
    path('HotelLocationCodePage/', views.HotelLocationCodePage, name='HotelLocationCodePage'),
    path('Hotel_search_Code_Location_Code_autocomplete/', views.Hotel_search_Code_Location_Code_autocomplete, name='Hotel_search_Code_Location_Code_autocomplete'),
    path('Hotel_search_Description_Location_Code_autocomplete/', views.Hotel_search_Description_Location_Code_autocomplete, name='Hotel_search_Description_Location_Code_autocomplete'),
    path('DeleteHotelLocationCode/<int:id>/', views.DeleteHotelLocationCode, name='DeleteHotelLocationCode'),
    path('AddHotelLocationCode/', views.AddHotelLocationCode, name='AddHotelLocationCode'),
    path('UpdateHotelLocationCode/<int:id>/', views.UpdateHotelLocationCode, name='UpdateHotelLocationCode'),




    #---------------HOTEL PROCESS CONFIG-----------------------
    path('HotelProcessConfigPage/', views.HotelProcessConfigPage, name='HotelProcessConfigPage'),
    path('Hotel_search_ProcesId_process_config_autocomplete/', views.Hotel_search_ProcesId_process_config_autocomplete, name='Hotel_search_ProcesId_process_config_autocomplete'),
    path('Hotel_search_Description_process_config_autocomplete/', views.Hotel_search_Description_process_config_autocomplete, name='Hotel_search_Description_process_config_autocomplete'),
    path('DeleteHotelProcessConfig/<int:id>/', views.DeleteHotelProcessConfig, name='DeleteHotelProcessConfig'),
    path('AddHotelProcessConfig/', views.AddHotelProcessConfig, name='AddHotelProcessConfig'),
    path('UpdateHotelProcessConfig/<int:id>/', views.UpdateHotelProcessConfig, name='UpdateHotelProcessConfig'),


    #---------------HOTEL STORE CODES-----------------------
    path('HotelStoreCodePage/', views.HotelStoreCodePage, name='HotelStoreCodePage'),
    path('Hotel_search_Code_store_code_autocomplete/', views.Hotel_search_Code_store_code_autocomplete, name='Hotel_search_Code_store_code_autocomplete'),
    path('Hotel_search_Description_store_code_autocomplete/', views.Hotel_search_Description_store_code_autocomplete, name='Hotel_search_Description_store_code_autocomplete'),
    path('DeleteHotelStoreCode/<int:id>/', views.DeleteHotelStoreCode, name='DeleteHotelStoreCode'),
    path('AddHotelStoreCode/', views.AddHotelStoreCode, name='AddHotelStoreCode'),
    path('UpdateHotelStoreCode/<int:id>/', views.UpdateHotelStoreCode, name='UpdateHotelStoreCode'),




    #---------------HOTEL STORE BIN CODES-----------------------
    path('HotelStoreBinCodePage/', views.HotelStoreBinCodePage, name='HotelStoreBinCodePage'),
    path('Hotel_search_StoreBinCode_store_bin_code_autocomplete/', views.Hotel_search_StoreBinCode_store_bin_code_autocomplete, name='Hotel_search_StoreBinCode_store_bin_code_autocomplete'),
    path('Hotel_search_CardNo_store_bin_code_autocomplete/', views.Hotel_search_CardNo_store_bin_code_autocomplete, name='Hotel_search_CardNo_store_bin_code_autocomplete'),
    path('Hotel_search_Description_store_bin_code_autocomplete/', views.Hotel_search_Description_store_bin_code_autocomplete, name='Hotel_search_Description_store_bin_code_autocomplete'),
    path('DeleteHotelStoreBinCode/<int:id>/', views.DeleteHotelStoreBinCode, name='DeleteHotelStoreBinCode'),
    path('AddHotelStoreBinCode/', views.AddHotelStoreBinCode, name='AddHotelStoreBinCode'),
    path('UpdateHotelStoreBinCode/<int:id>/', views.UpdateHotelStoreBinCode, name='UpdateHotelStoreBinCode'),



    #---------------HOTEL EVENT CODES-----------------------
    path('HotelEventCodePage/', views.HotelEventCodePage, name='HotelEventCodePage'),
    path('Hotel_search_Code_Event_Code_autocomplete/', views.Hotel_search_Code_Event_Code_autocomplete, name='Hotel_search_Code_Event_Code_autocomplete'),
    path('Hotel_search_Description_Event_Code_autocomplete/', views.Hotel_search_Description_Event_Code_autocomplete, name='Hotel_search_Description_Event_Code_autocomplete'),
    path('DeleteHotelEventCode/<int:id>/', views.DeleteHotelEventCode, name='DeleteHotelEventCode'),
    path('AddHotelEventCode/', views.AddHotelEventCode, name='AddHotelEventCode'),
    path('UpdateHotelEventCode/<int:id>/', views.UpdateHotelEventCode, name='UpdateHotelEventCode'),



    #---------------HOTEL EVENT ALERT-----------------------
    path('HotelEventAlertPage/', views.HotelEventAlertPage, name='HotelEventAlertPage'),
    path('Hotel_search_Code_AlertID_autocomplete/', views.Hotel_search_Code_AlertID_autocomplete, name='Hotel_search_Code_AlertID_autocomplete'),
    path('DeleteHotelEventAlert/<int:id>/', views.DeleteHotelEventAlert, name='DeleteHotelEventAlert'),
    path('AddHotelEventAlert/', views.AddHotelEventAlert, name='AddHotelEventAlert'),
    path('UpdateHotelEventAlert/<int:id>/', views.UpdateHotelEventAlert, name='UpdateHotelEventAlert'),




    #---------------HOTEL UOM SHORT CODES-----------------------
    path('HotelUOMPage/', views.HotelUOMPage, name='HotelUOMPage'),
    path('Hotel_search_UOMShortCode_HotelUOM_autocomplete/', views.Hotel_search_UOMShortCode_HotelUOM_autocomplete, name='Hotel_search_UOMShortCode_HotelUOM_autocomplete'),
    path('DeleteHotelUOM/<int:id>/', views.DeleteHotelUOM, name='DeleteHotelUOM'),
    path('AddHotelUOM/', views.AddHotelUOM, name='AddHotelUOM'),
    path('UpdateHotelUOM/<int:id>/', views.UpdateHotelUOM, name='UpdateHotelUOM'),



    #---------------HOTEL UOM SHORT CODES-----------------------
    path('HotelBOMPage/', views.HotelBOMPage, name='HotelBOMPage'),
    path('Hotel_search_Code_HotelBOM_autocomplete/', views.Hotel_search_Code_HotelBOM_autocomplete, name='Hotel_search_Code_HotelBOM_autocomplete'),
    path('Hotel_search_Name_HotelBOM_autocomplete/', views.Hotel_search_Name_HotelBOM_autocomplete, name='Hotel_search_Name_HotelBOM_autocomplete'),
    path('DeleteHotelBOM/<int:id>/', views.DeleteHotelBOM, name='DeleteHotelBOM'),
    path('AddHotelBOM/', views.AddHotelBOM, name='AddHotelBOM'),
    path('UpdateHotelBOM/<int:id>/', views.UpdateHotelBOM, name='UpdateHotelBOM'),

    path('HotelBOMDetailPage/', views.HotelBOMDetailPage, name='HotelBOMDetailPage'),
    path('AddHotelBOMFiles/', views.AddHotelBOMFiles, name='AddHotelBOMFiles'),







    #-------------------HOTE FOODL PRODUCTS CATEGORY----------------
    #-----All Categories----------
    path('HotelProductsCategoriesPage/', views.HotelProductsCategoriesPage, name='HotelProductsCategoriesPage'),

    path('ViewHotelFoodCategoriesPage/<int:id>/', views.ViewHotelFoodCategoriesPage, name='ViewHotelFoodCategoriesPage'),
    path('UpdateHotelFoodCategories/<int:id>/', views.UpdateHotelFoodCategories, name='UpdateHotelFoodCategories'),
    path('DeleteHotelFoodCategories/<int:id>/', views.DeleteHotelFoodCategories, name='DeleteHotelFoodCategories'),


    #-------------------HOTEL DRINKS  PRODUCTS CATEGORIES-------------
    path('ViewHotelDrinksCategoriesPage/<int:id>/', views.ViewHotelDrinksCategoriesPage, name='ViewHotelDrinksCategoriesPage'),
    path('UpdateHotelDrinksCategories/<int:id>/', views.UpdateHotelDrinksCategories, name='UpdateHotelDrinksCategories'),
    path('DeleteHotelDrinksCategories/<int:id>/', views.DeleteHotelDrinksCategories, name='DeleteHotelDrinksCategories'),



    #-------------------HOTEL ROOMS PRODUCTS CATEGORIES-------------
    path('ViewRoomsClassesPage/<int:id>/', views.ViewRoomsClassesPage, name='ViewRoomsClassesPage'),
    path('UpdateRoomsClasses/<int:id>/', views.UpdateRoomsClasses, name='UpdateRoomsClasses'),
    path('DeleteRoomsClasses/<int:id>/', views.DeleteRoomsClasses, name='DeleteRoomsClasses'),








    #---------------------PRODUCTS ITSELF MAINTENANCE---------

    path('HotelProductsPage/', views.HotelProductsPage, name='HotelProductsPage'),
    

    #--------------------FOOD PRODUCTS-------------
    path('HotelFoodProductsPage/', views.HotelFoodProductsPage, name='HotelFoodProductsPage'),
    path('search_product_name_HotelFoodProducts_autocomplete/', views.search_product_name_HotelFoodProducts_autocomplete, name='search_product_name_HotelFoodProducts_autocomplete'),
    path('search_product_second_name_HotelFoodProducts_autocomplete/', views.search_product_second_name_HotelFoodProducts_autocomplete, name='search_product_second_name_HotelFoodProducts_autocomplete'),
    path('AddHotelFoodProducts/', views.AddHotelFoodProducts, name='AddHotelFoodProducts'),
    path('DeleteHotelFoodProducts/<int:id>/', views.DeleteHotelFoodProducts, name='DeleteHotelFoodProducts'),
    path('UpdateHotelFoodProducts/<int:id>/', views.UpdateHotelFoodProducts, name='UpdateHotelFoodProducts'),

    #--------------------DRINKS PRODUCTS-------------
    path('HotelDrinksProductsPage/', views.HotelDrinksProductsPage, name='HotelDrinksProductsPage'),
    path('search_product_name_HotelDrinksProducts_autocomplete/', views.search_product_name_HotelDrinksProducts_autocomplete, name='search_product_name_HotelDrinksProducts_autocomplete'),
    path('search_product_second_name_HotelDrinksProducts_autocomplete/', views.search_product_second_name_HotelDrinksProducts_autocomplete, name='search_product_second_name_HotelDrinksProducts_autocomplete'),
    path('AddHotelDrinksProducts/', views.AddHotelDrinksProducts, name='AddHotelDrinksProducts'),
    path('DeleteHotelDrinksProducts/<int:id>/', views.DeleteHotelDrinksProducts, name='DeleteHotelDrinksProducts'),
    path('UpdateHotelDrinksProducts/<int:id>/', views.UpdateHotelDrinksProducts, name='UpdateHotelDrinksProducts'),




    #--------------------ROOMS PRODUCTS-------------
    path('HotelRoomsPage/', views.HotelRoomsPage, name='HotelRoomsPage'),
    path('search_RoomName_HotelRooms_autocomplete/', views.search_RoomName_HotelRooms_autocomplete, name='search_RoomName_HotelRooms_autocomplete'),
    path('AddHotelRooms/', views.AddHotelRooms, name='AddHotelRooms'),
    path('DeleteHotelRooms/<int:id>/', views.DeleteHotelRooms, name='DeleteHotelRooms'),
    path('UpdateHotelRooms/<int:id>/', views.UpdateHotelRooms, name='UpdateHotelRooms'),

    path('HotelBookedRoomsPage/', views.HotelBookedRoomsPage, name='HotelBookedRoomsPage'),







    #----------------UPLOAD PRODUCTS----------------------------------------
    path('UploadHotelProductsPage/', views.UploadHotelProductsPage, name='UploadHotelProductsPage'),
    
    path('UploadHotelFoodProductsPage/', views.UploadHotelFoodProductsPage, name='UploadHotelFoodProductsPage'),
    path('UploadHotelDrinksProductsPage/', views.UploadHotelDrinksProductsPage, name='UploadHotelDrinksProductsPage'),
    path('UploadHotelRoomsProductsPage/', views.UploadHotelRoomsProductsPage, name='UploadHotelRoomsProductsPage'),





    #------------------------------ORDERS--------------------------------

    path('HotelOrdersPage/', views.HotelOrdersPage, name='HotelOrdersPage'),

    path('HotelFoodOrderPage/', views.HotelFoodOrderPage, name='HotelFoodOrderPage'),
    path('DeleteHotelFoodOrder/<int:id>/', views.DeleteHotelFoodOrder, name='DeleteHotelFoodOrder'),




    


    #------------------------STAFF MAINTENANCE_-----------------
    path('HotelMyUserPage/', views.HotelMyUserPage, name='HotelMyUserPage'),
    path('Hotel_search_username_HotelMyUser_autocomplete/', views.Hotel_search_username_HotelMyUser_autocomplete, name='Hotel_search_username_HotelMyUser_autocomplete'),
    path('Hotel_search_email_HotelMyUser_autocomplete/', views.Hotel_search_email_HotelMyUser_autocomplete, name='Hotel_search_email_HotelMyUser_autocomplete'),
    path('DeleteHotelMyUser/<int:id>/', views.DeleteHotelMyUser, name='DeleteHotelMyUser'),





    #--------------------HOTEL SUPPLIERS_------------------------

    path('HotelSuppliersPage/', views.HotelSuppliersPage, name='HotelSuppliersPage'),
    path('Hotel_search_SupplierFullName_HotelSuppliers_autocomplete/', views.Hotel_search_SupplierFullName_HotelSuppliers_autocomplete, name='Hotel_search_SupplierFullName_HotelSuppliers_autocomplete'),
    path('Hotel_search_Keyword_HotelSuppliers_autocomplete/', views.Hotel_search_Keyword_HotelSuppliers_autocomplete, name='Hotel_search_Keyword_HotelSuppliers_autocomplete'),
    path('DeleteHotelHotelSuppliers/<int:id>/', views.DeleteHotelHotelSuppliers, name='DeleteHotelHotelSuppliers'),
    path('AddHotelSuppliers/', views.AddHotelSuppliers, name='AddHotelSuppliers'),
    path('UpdateHotelSuppliers/<int:id>/', views.UpdateHotelSuppliers, name='UpdateHotelSuppliers'),



    
]