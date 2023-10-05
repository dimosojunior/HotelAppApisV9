from rest_framework.validators import UniqueValidator
#from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from HotelApis.models import *
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User

class RestaurantTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTables
        fields = '__all__'


class RestaurantInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInventory
        fields = '__all__'

class RestaurantFoodCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodCategories
        fields = '__all__'

class RestaurantDrinksCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksCategories
        fields = '__all__'



class RestaurantCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCustomers
        fields = '__all__'














#-----------------Restaurant FOOD PRODUCTS------------------
class RestaurantFoodProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodProducts
        fields = '__all__'

#-----------------Restaurant DRINKS PRODUCTS------------------
class RestaurantDrinksProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksProducts
        fields = '__all__'












#---------------------Restaurant FOOD CART SERIALIZER---------


class RestaurantFoodCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodCart
        fields = '__all__'


class RestaurantFoodCartItemsSerializer(serializers.ModelSerializer):
    cart = RestaurantFoodCartSerializer()
    product = RestaurantFoodProductsSerializer()

    table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantFoodCartItems
        fields = '__all__'



class RestaurantFoodOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFoodOrder
        fields = '__all__'


class RestaurantFoodOrderItemsSerializer(serializers.ModelSerializer):
    order = RestaurantFoodOrderSerializer()
    product = RestaurantFoodProductsSerializer()

    table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantFoodOrderItems
        fields = '__all__'








#---------------------HOTEL DRINKS CART SERIALIZER---------


class RestaurantDrinksCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksCart
        fields = '__all__'


class RestaurantDrinksCartItemsSerializer(serializers.ModelSerializer):
    cart = RestaurantDrinksCartSerializer()
    product = RestaurantDrinksProductsSerializer()

    table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantDrinksCartItems
        fields = '__all__'



class RestaurantDrinksOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDrinksOrder
        fields = '__all__'


class RestaurantDrinksOrderItemsSerializer(serializers.ModelSerializer):
    order = RestaurantDrinksOrderSerializer()
    product = RestaurantDrinksProductsSerializer()

    table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantDrinksOrderItems
        fields = '__all__'









#-----------GET HOTEL WAITERS----------------
class RestaurantWaitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'