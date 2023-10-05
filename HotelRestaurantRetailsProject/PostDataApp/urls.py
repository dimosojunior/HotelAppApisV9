
from django.urls import path
from . import views

# # MWANZO IN ORDER TO USE MODEL VIEW SET
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('PostMyUser', views.MyUserViewSet)
router.register('PostHotelTables', views.HotelTablesViewSet)
router.register('PostRestaurantTables', views.RestaurantTablesViewSet)
router.register('PostRetailsTables', views.RetailsTablesViewSet)



router.register('PostHotelInventory', views.HotelInventoryViewSet)
router.register('PostHotelFoodCategories', views.HotelFoodCategoriesViewSet)
router.register('PostHotelDrinksCategories', views.HotelDrinksCategoriesViewSet)
router.register('PostRoomsClasses', views.RoomsClassesViewSet)
router.register('PostHotelCustomers', views.HotelCustomersViewSet)




# HOTEL  PRODUCT
router.register('PostHotelFoodProducts', views.HotelFoodProductsViewSet)
router.register('PostHotelDrinksProducts', views.HotelDrinksProductsViewSet)
router.register('PostHotelRooms', views.HotelRoomsViewSet)








#--------------BOOKED HOTEL ROOMS-----------------
router.register('PostHotelBookedRoomsClassA', views.HotelBookedRoomsClassAViewSet)
router.register('PostHotelBookedRoomsClassB', views.HotelBookedRoomsClassBViewSet)
router.register('PostHotelBookedRoomsClassC', views.HotelBookedRoomsClassCViewSet)
router.register('PostHotelBookedRoomsClassD', views.HotelBookedRoomsClassDViewSet)
router.register('PostHotelBookedRoomsClassE', views.HotelBookedRoomsClassEViewSet)











#-----------------------RESTAURANT----------------------


router.register('PostRestaurantInventory', views.RestaurantInventoryViewSet)
router.register('PostRestaurantFoodCategories', views.RestaurantFoodCategoriesViewSet)
router.register('PostRestaurantDrinksCategories', views.RestaurantDrinksCategoriesViewSet)

router.register('PostRestaurantCustomers', views.RestaurantCustomersViewSet)






# REstaurant FOOD PRODUCT
router.register('PostRestaurantFoodProducts', views.RestaurantFoodProductsViewSet)
router.register('PostRestaurantDrinksProducts', views.RestaurantDrinksProductsViewSet)












#-----------------------RETAILS-------------------------




router.register('PostRetailsInventory', views.RetailsInventoryViewSet)
router.register('PostRetailsFoodCategories', views.RetailsFoodCategoriesViewSet)
router.register('PostRetailsDrinksCategories', views.RetailsDrinksCategoriesViewSet)

router.register('PostRetailsCustomers', views.RetailsCustomersViewSet)












# RETAILS  PRODUCT
router.register('PostRetailsFoodProducts', views.RetailsFoodProductsViewSet)
router.register('PostRetailsDrinksProducts', views.RetailsDrinksProductsViewSet)








#---------------GET WAITERS---------------------

router.register('PostHotelWaiters', views.HotelWaitersViewSet)
router.register('PostRestaurantWaiters', views.RestaurantWaitersViewSet)
router.register('PostRetailsWaiters', views.RetailsWaitersViewSet)




urlpatterns = router.urls