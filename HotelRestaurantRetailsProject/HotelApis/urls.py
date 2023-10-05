
from django.urls import path
from . import views



urlpatterns = [

    path('HotelLocationCode/', views.HotelLocationCodeViewSet.as_view(), name='HotelLocationCode'),
    path('HotelBusinessUnit/', views.HotelBusinessUnitViewSet.as_view(), name='HotelBusinessUnit'),

    path('HotelFoodProducts/', views.HotelFoodProductsViewSet.as_view(), name='HotelFoodProducts'),
    path('HotelDrinksProducts/', views.HotelDrinksProductsViewSet.as_view(), name='HotelDrinksProducts'),
    path('HotelRoomsProducts/', views.HotelRoomsProductsViewSet.as_view(), name='HotelRoomsProducts'),
    path('HotelBookedRoomsProducts/', views.HotelBookedRoomsProductsViewSet.as_view(), name='HotelBookedRoomsProducts'),



    path('HotelInventory/', views.HotelInventoryViewSet.as_view(), name='HotelInventory'),
    path('HotelFoodCategories/', views.HotelFoodCategoriesViewSet.as_view(), name='HotelFoodCategories'),
    path('HotelDrinksCategories/', views.HotelDrinksCategoriesViewSet.as_view(), name='HotelDrinksCategories'),
    path('RoomsClasses/', views.RoomsClassesViewSet.as_view(), name='RoomsClasses'),
    path('HotelCustomers/', views.HotelCustomersViewSet.as_view(), name='HotelCustomers'),
    path('MyUser/', views.MyUserViewSet.as_view(), name='MyUser'),
   
    path('HotelPizzaProducts/', views.HotelPizzaProductsViewSet.as_view(), name='HotelPizzaProducts'),
    path('HotelOtherFoodProducts/', views.HotelOtherFoodProductsViewSet.as_view(), name='HotelOtherFoodProducts'),

    path('HotelSoftDrinksProducts/', views.HotelSoftDrinksProductsViewSet.as_view(), name='HotelSoftDrinksProducts'),
    path('HotelBeersProducts/', views.HotelBeersProductsViewSet.as_view(), name='HotelBeersProducts'),

    path('HotelRoomsClassA/', views.HotelRoomsClassAViewSet.as_view(), name='HotelRoomsClassA'),
    path('HotelRoomsClassB/', views.HotelRoomsClassBViewSet.as_view(), name='HotelRoomsClassB'),
    path('HotelRoomsClassC/', views.HotelRoomsClassCViewSet.as_view(), name='HotelRoomsClassC'),
    path('HotelRoomsClassD/', views.HotelRoomsClassDViewSet.as_view(), name='HotelRoomsClassD'),
    path('HotelRoomsClassE/', views.HotelRoomsClassEViewSet.as_view(), name='HotelRoomsClassE'),



    path('HotelBookedRoomsClassA/', views.HotelBookedRoomsClassAViewSet.as_view(), name='HotelBookedRoomsClassA'),
    path('HotelBookedRoomsClassB/', views.HotelBookedRoomsClassBViewSet.as_view(), name='HotelBookedRoomsClassB'),
    path('HotelBookedRoomsClassC/', views.HotelBookedRoomsClassCViewSet.as_view(), name='HotelBookedRoomsClassC'),
    path('HotelBookedRoomsClassD/', views.HotelBookedRoomsClassDViewSet.as_view(), name='HotelBookedRoomsClassD'),
    path('HotelBookedRoomsClassE/', views.HotelBookedRoomsClassEViewSet.as_view(), name='HotelBookedRoomsClassE'),



    

]


# #--------------UNORDERED HOTEL ROOMS-----------------
# router.register('HotelRoomsClassA', views.HotelRoomsClassAViewSet)
# router.register('HotelRoomsClassB', views.HotelRoomsClassBViewSet)
# router.register('HotelRoomsClassC', views.HotelRoomsClassCViewSet)
# router.register('HotelRoomsClassD', views.HotelRoomsClassDViewSet)
# router.register('HotelRoomsClassE', views.HotelRoomsClassEViewSet)



# #--------------BOOKED HOTEL ROOMS-----------------
# router.register('HotelBookedRoomsClassA', views.HotelBookedRoomsClassAViewSet)
# router.register('HotelBookedRoomsClassB', views.HotelBookedRoomsClassBViewSet)
# router.register('HotelBookedRoomsClassC', views.HotelBookedRoomsClassCViewSet)
# router.register('HotelBookedRoomsClassD', views.HotelBookedRoomsClassDViewSet)
# router.register('HotelBookedRoomsClassE', views.HotelBookedRoomsClassEViewSet)



# urlpatterns = router.urls