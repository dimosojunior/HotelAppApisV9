
from django.urls import path
from . import views

# MWANZO IN ORDER TO USE MODEL VIEW SET


urlpatterns = [

    path('RestaurantFoodProducts/', views.RestaurantFoodProductsViewSet.as_view(), name='RestaurantFoodProducts'),
    path('RestaurantDrinksProducts/', views.RestaurantDrinksProductsViewSet.as_view(), name='RestaurantDrinksProducts'),


    path('RestaurantInventory/', views.RestaurantInventoryViewSet.as_view(), name='RestaurantInventory'),
    path('RestaurantFoodCategories/', views.RestaurantFoodCategoriesViewSet.as_view(), name='RestaurantFoodCategories'),
    path('RestaurantDrinksCategories/', views.RestaurantDrinksCategoriesViewSet.as_view(), name='RestaurantDrinksCategories'),
    #path('RoomsClasses/', views.RoomsClassesViewSet.as_view(), name='RoomsClasses'),
    path('RestaurantCustomers/', views.RestaurantCustomersViewSet.as_view(), name='RestaurantCustomers'),
    path('MyUser/', views.MyUserViewSet.as_view(), name='MyUser'),
   
    path('RestaurantPizzaProducts/', views.RestaurantPizzaProductsViewSet.as_view(), name='RestaurantPizzaProducts'),
    path('RestaurantOtherFoodProducts/', views.RestaurantOtherFoodProductsViewSet.as_view(), name='RestaurantOtherFoodProducts'),

    path('RestaurantSoftDrinksProducts/', views.RestaurantSoftDrinksProductsViewSet.as_view(), name='RestaurantSoftDrinksProducts'),
    path('RestaurantBeersProducts/', views.RestaurantBeersProductsViewSet.as_view(), name='RestaurantBeersProducts'),


    

]
