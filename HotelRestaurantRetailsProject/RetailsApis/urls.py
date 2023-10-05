
from django.urls import path
from . import views



urlpatterns = [

    path('RetailsFoodProducts/', views.RetailsFoodProductsViewSet.as_view(), name='RetailsFoodProducts'),
    path('RetailsDrinksProducts/', views.RetailsDrinksProductsViewSet.as_view(), name='RetailsDrinksProducts'),


    path('RetailsInventory/', views.RetailsInventoryViewSet.as_view(), name='RetailsInventory'),
    path('RetailsFoodCategories/', views.RetailsFoodCategoriesViewSet.as_view(), name='RetailsFoodCategories'),
    path('RetailsDrinksCategories/', views.RetailsDrinksCategoriesViewSet.as_view(), name='RetailsDrinksCategories'),
    #path('RoomsClasses/', views.RoomsClassesViewSet.as_view(), name='RoomsClasses'),
    path('RetailsCustomers/', views.RetailsCustomersViewSet.as_view(), name='RetailsCustomers'),
    path('MyUser/', views.MyUserViewSet.as_view(), name='MyUser'),
   
    path('RetailsPizzaProducts/', views.RetailsPizzaProductsViewSet.as_view(), name='RetailsPizzaProducts'),
    path('RetailsOtherFoodProducts/', views.RetailsOtherFoodProductsViewSet.as_view(), name='RetailsOtherFoodProducts'),

    path('RetailsSoftDrinksProducts/', views.RetailsSoftDrinksProductsViewSet.as_view(), name='RetailsSoftDrinksProducts'),
    path('RetailsBeersProducts/', views.RetailsBeersProductsViewSet.as_view(), name='RetailsBeersProducts'),


    

]
