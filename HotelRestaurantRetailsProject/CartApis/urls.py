from . import views
from django.urls import path,include

from rest_framework.routers import DefaultRouter






urlpatterns = [


    path('', views.HomeView, name='CartHome'),

    #-------------------HOTEL FOOD CART---------------------------
    path('HotelFoodCart/', views.HotelFoodCartView.as_view(), name='HotelFoodCart'),
    path('HotelFoodOrder/', views.HotelFoodOrderView.as_view(), name='hotel-food-order-list'),
    path('HotelFoodOrdernNoDelete/', views.HotelFoodOrdernNoDeleteView.as_view(), name='hotel-food-order-list-no-delete'),
    path('HotelFoodDeleteCartItem/', views.HotelFoodDeleteCartItemView.as_view(), name='HotelDeleteCart'),




    #----------------HOTEL DRINKS CART--------------------------------------

    path('HotelDrinksCart/', views.HotelDrinksCartView.as_view(), name='HotelDrinksCart'),
    path('HotelDrinksOrder/', views.HotelDrinksOrderView.as_view(), name='hotel-Drinks-order-list'),
    path('HotelDrinksOrdernNoDelete/', views.HotelDrinksOrdernNoDeleteView.as_view(), name='hotel-Drinks-order-list-no-delete'),
    path('HotelDrinksDeleteCartItem/', views.HotelDrinksDeleteCartItemView.as_view(), name='HotelDrinksDeleteCart'),




    #-------------------HOTEL ROOMS---------------------------

    path('HotelRoomsCart/', views.HotelRoomsCartView.as_view(), name='HotelRoomsCart'),
    path('HotelRoomsOrder/', views.HotelRoomsOrderView.as_view(), name='hotel-Rooms-order-list'),
    path('HotelRoomsDeleteCartItem/', views.HotelRoomsDeleteCartItemView.as_view(), name='HotelRoomsDeleteCart'),
    #path('HotelRoomsOrdernNoDelete/', views.HotelRoomsOrdernNoDeleteView.as_view(), name='hotel-Rooms-order-list-no-delete'),
















    #-------------------Restaurant FOOD CART---------------------------
    path('RestaurantFoodCart/', views.RestaurantFoodCartView.as_view(), name='RestaurantFoodCart'),
    path('RestaurantFoodOrder/', views.RestaurantFoodOrderView.as_view(), name='Restaurant-food-order-list'),
    path('RestaurantFoodOrdernNoDelete/', views.RestaurantFoodOrdernNoDeleteView.as_view(), name='Restaurant-food-order-list-no-delete'),
    path('RestaurantFoodDeleteCartItem/', views.RestaurantFoodDeleteCartItemView.as_view(), name='RestaurantFoodDeleteCart'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),




    #----------------Restaurant DRINKS CART--------------------------------------

    path('RestaurantDrinksCart/', views.RestaurantDrinksCartView.as_view(), name='RestaurantDrinksCart'),
    path('RestaurantDrinksOrder/', views.RestaurantDrinksOrderView.as_view(), name='Restaurant-Drinks-order-list'),
    path('RestaurantDrinksOrdernNoDelete/', views.RestaurantDrinksOrdernNoDeleteView.as_view(), name='Restaurant-Drinks-order-list-no-delete'),
    path('RestaurantDrinksDeleteCartItem/', views.RestaurantDrinksDeleteCartItemView.as_view(), name='RestaurantDrinksDeleteCart'),












    #-------------------Retails FOOD CART---------------------------
    path('RetailsFoodCart/', views.RetailsFoodCartView.as_view(), name='RetailsFoodCart'),
    path('RetailsFoodOrder/', views.RetailsFoodOrderView.as_view(), name='Retails-food-order-list'),
    path('RetailsFoodOrdernNoDelete/', views.RetailsFoodOrdernNoDeleteView.as_view(), name='Retails-food-order-list-no-delete'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),
    path('RetailsFoodDeleteCartItem/', views.RetailsFoodDeleteCartItemView.as_view(), name='RetailsFoodDeleteCart'),




    #----------------Retails DRINKS CART--------------------------------------

    path('RetailsDrinksCart/', views.RetailsDrinksCartView.as_view(), name='RetailsDrinksCart'),
    path('RetailsDrinksOrder/', views.RetailsDrinksOrderView.as_view(), name='Retails-Drinks-order-list'),
    path('RetailsDrinksOrdernNoDelete/', views.RetailsDrinksOrdernNoDeleteView.as_view(), name='Retails-Drinks-order-list-no-delete'),
    path('RetailsDrinksDeleteCartItem/', views.RetailsDrinksDeleteCartItemView.as_view(), name='RetailsDrinksDeleteCart'),







    #------------------HOTEL  REPORT--------------------
    path('HotelFoodOrderReport/', views.HotelFoodOrderReportView.as_view(), name='HotelFoodOrderReport'),
    path('HotelDrinksOrderReport/', views.HotelDrinksOrderReportView.as_view(), name='HotelDrinksOrderReport'),
    path('HotelRoomsOrderReport/', views.HotelRoomsOrderReportView.as_view(), name='HotelRoomsOrderReport'),





    #------------------RESTAURANT  REPORT--------------------
    path('RestaurantFoodOrderReport/', views.RestaurantFoodOrderReportView.as_view(), name='RestaurantFoodOrderReport'),
    path('RestaurantDrinksOrderReport/', views.RestaurantDrinksOrderReportView.as_view(), name='RestaurantDrinksOrderReport'),
    



    #------------------RETAILS  REPORT--------------------
    path('RetailsFoodOrderReport/', views.RetailsFoodOrderReportView.as_view(), name='RetailsFoodOrderReport'),
    path('RetailsDrinksOrderReport/', views.RetailsDrinksOrderReportView.as_view(), name='RetailsDrinksOrderReport'),





    #------------------FILTER REPORT----------------------

    #----------HOTEL FILTER REPORT

    path('FilterHotelFoodOrderReport/', views.FilterHotelFoodOrderReportView.as_view(), name='FilterHotelFoodOrderReport'),
    path('FilterHotelDrinksOrderReport/', views.FilterHotelDrinksOrderReportView.as_view(), name='FilterHotelDrinksOrderReport'),
    path('FilterHotelRoomsOrderReport/', views.FilterHotelRoomsOrderReportView.as_view(), name='FilterHotelRoomsOrderReport'),



    #__________RESTAURANT FILTER REPORT-----------------------
    path('FilterRestaurantFoodOrderReport/', views.FilterRestaurantFoodOrderReportView.as_view(), name='FilterRestaurantFoodOrderReport'),
    path('FilterRestaurantDrinksOrderReport/', views.FilterRestaurantDrinksOrderReportView.as_view(), name='FilterRestaurantDrinksOrderReport'),
   





    #------------------RETAILS FILTER REPORT----------------

    path('FilterRetailsFoodOrderReport/', views.FilterRetailsFoodOrderReportView.as_view(), name='FilterRetailsFoodOrderReport'),
    path('FilterRetailsDrinksOrderReport/', views.FilterRetailsDrinksOrderReportView.as_view(), name='FilterRetailsDrinksOrderReport'),
    



    
    

    #------------------RECEIPT------------------------

    #-----------HOTEL FOOD RECEIPT-------------------
    path('HotelFoodReceipt/', views.HotelFoodReceiptView.as_view(), name='HotelFoodReceipt'),










    #---------------------------GET ALL ORDER ITEMS  HOTEL ----------------------
    path('GetHotelFoodOrderItems/', views.GetHotelFoodOrderItemsView.as_view(), name='GetHotelFoodOrderItems'),
    path('GetHotelDrinksOrderItems/', views.GetHotelDrinksOrderItemsView.as_view(), name='GetHotelDrinksOrderItems'),
    path('GetHotelRoomsOrderItems/', views.GetHotelRoomsOrderItemsView.as_view(), name='GetHotelRoomsOrderItems'),



    #---------------------------GET ALL ORDER ITEMS  Restaurant ----------------------
    path('GetRestaurantFoodOrderItems/', views.GetRestaurantFoodOrderItemsView.as_view(), name='GetRestaurantFoodOrderItems'),
    path('GetRestaurantDrinksOrderItems/', views.GetRestaurantDrinksOrderItemsView.as_view(), name='GetRestaurantDrinksOrderItems'),




    #---------------------------GET ALL ORDER ITEMS  Retails ----------------------
    path('GetRetailsFoodOrderItems/', views.GetRetailsFoodOrderItemsView.as_view(), name='GetRetailsFoodOrderItems'),
    path('GetRetailsDrinksOrderItems/', views.GetRetailsDrinksOrderItemsView.as_view(), name='GetRetailsDrinksOrderItems'),







    #----------------CHANGE ORDERSTATUS----------------------
    #---------------HOTEL -----------------------
    path('HotelFoodOrderChangeStatusToTrue/', views.HotelFoodOrderChangeStatusToTrueView.as_view(), name='HotelFoodOrderChangeStatusToTrue'),
    path('HotelFoodOrderChangeStatusToFalse/', views.HotelFoodOrderChangeStatusToFalseView.as_view(), name='HotelFoodOrderChangeStatusToFalse'),

    path('HotelDrinksOrderChangeStatusToTrue/', views.HotelDrinksOrderChangeStatusToTrueView.as_view(), name='HotelDrinksOrderChangeStatusToTrue'),
    path('HotelDrinksOrderChangeStatusToFalse/', views.HotelDrinksOrderChangeStatusToFalseView.as_view(), name='HotelDrinksOrderChangeStatusToFalse'),

    path('HotelRoomsOrderChangeStatusToTrue/', views.HotelRoomsOrderChangeStatusToTrueView.as_view(), name='HotelRoomsOrderChangeStatusToTrue'),
    path('HotelRoomsOrderChangeStatusToFalse/', views.HotelRoomsOrderChangeStatusToFalseView.as_view(), name='HotelRoomsOrderChangeStatusToFalse'),


    #-----------------RESTAURANT------------------------
    path('RestaurantFoodOrderChangeStatusToTrue/', views.RestaurantFoodOrderChangeStatusToTrueView.as_view(), name='RestaurantFoodOrderChangeStatusToTrue'),
    path('RestaurantFoodOrderChangeStatusToFalse/', views.RestaurantFoodOrderChangeStatusToFalseView.as_view(), name='RestaurantFoodOrderChangeStatusToFalse'),

    path('RestaurantDrinksOrderChangeStatusToTrue/', views.RestaurantDrinksOrderChangeStatusToTrueView.as_view(), name='RestaurantDrinksOrderChangeStatusToTrue'),
    path('RestaurantDrinksOrderChangeStatusToFalse/', views.RestaurantDrinksOrderChangeStatusToFalseView.as_view(), name='RestaurantDrinksOrderChangeStatusToFalse'),



    #---------------------------RETAILS----------------------
    path('RetailsFoodOrderChangeStatusToTrue/', views.RetailsFoodOrderChangeStatusToTrueView.as_view(), name='RetailsFoodOrderChangeStatusToTrue'),
    path('RetailsFoodOrderChangeStatusToFalse/', views.RetailsFoodOrderChangeStatusToFalseView.as_view(), name='RetailsFoodOrderChangeStatusToFalse'),

    path('RetailsDrinksOrderChangeStatusToTrue/', views.RetailsDrinksOrderChangeStatusToTrueView.as_view(), name='RetailsDrinksOrderChangeStatusToTrue'),
    path('RetailsDrinksOrderChangeStatusToFalse/', views.RetailsDrinksOrderChangeStatusToFalseView.as_view(), name='RetailsDrinksOrderChangeStatusToFalse'),








    #------------------DELETE ORDERS-----------------------

    #---------DELETE HOTEL ORDERED ITEMS----------------
    path('HotelFoodDeleteOrderItem/', views.HotelFoodDeleteOrderItemView.as_view(), name='HotelFoodDeleteOrderItem'),
    path('HotelDrinksDeleteOrderItem/', views.HotelDrinksDeleteOrderItemView.as_view(), name='HotelDrinksDeleteOrderItem'),
    path('HotelRoomsDeleteOrderItem/', views.HotelRoomsDeleteOrderItemView.as_view(), name='HotelRoomsDeleteOrderItem'),


    #---------DELETE Restaurant ORDERED ITEMS----------------
    path('RestaurantFoodDeleteOrderItem/', views.RestaurantFoodDeleteOrderItemView.as_view(), name='RestaurantFoodDeleteOrderItem'),
    path('RestaurantDrinksDeleteOrderItem/', views.RestaurantDrinksDeleteOrderItemView.as_view(), name='RestaurantDrinksDeleteOrderItem'),


    #---------DELETE Retails ORDERED ITEMS----------------
    path('RetailsFoodDeleteOrderItem/', views.RetailsFoodDeleteOrderItemView.as_view(), name='RetailsFoodDeleteOrderItem'),
    path('RetailsDrinksDeleteOrderItem/', views.RetailsDrinksDeleteOrderItemView.as_view(), name='RetailsDrinksDeleteOrderItem'),
















    #-------------------------ADD TO CART MAKE ORDER WITHOUT ROOM BUT BY USING TABLEONLY
    path('HotelFoodAddToCartWithoutRoom/', views.HotelFoodAddToCartWithoutRoomView.as_view(), name='HotelFoodAddToCartWithoutRoom'),
    path('HotelDrinksAddToCartWithoutRoom/', views.HotelDrinksAddToCartWithoutRoomView.as_view(), name='HotelDrinksAddToCartWithoutRoom'),

    path('RestaurantFoodAddToCartWithoutRoom/', views.RestaurantFoodAddToCartWithoutRoomView.as_view(), name='RestaurantFoodAddToCartWithoutRoom'),
    path('RestaurantDrinksAddToCartWithoutRoom/', views.RestaurantDrinksAddToCartWithoutRoomView.as_view(), name='RestaurantDrinksAddToCartWithoutRoom'),

    path('RetailsFoodAddToCartWithoutRoom/', views.RetailsFoodAddToCartWithoutRoomView.as_view(), name='RetailsFoodAddToCartWithoutRoom'),
    path('RetailsDrinksAddToCartWithoutRoom/', views.RetailsDrinksAddToCartWithoutRoomView.as_view(), name='RetailsDrinksAddToCartWithoutRoom'),
    
    
]

