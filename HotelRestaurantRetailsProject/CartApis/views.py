from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,get_object_or_404
from HotelApis.serializers import *
from HotelApis.models import *
from HotelApis.serializers import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db import transaction

#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from HotelApis.serializers import *
from RestaurantApis.serializers import *
from RetailsApis.serializers import *
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

#   def get(self,request, format=None):
#       return Response("User Account View", status=200)

#   def post(self,request, format=None):

#       return Response("Creating User", status=200)



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed










#-----------------------------------------------


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HotelApis.models import MyUser  # Make sure to import your MyUser model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination
# Create your views here.





#ORDER PAGINATION-------------------------
#http://127.0.0.1:8000/Cart/HotelFoodOrder/?page=1&page_size=1





def HomeView(request):

    return HttpResponse("CART APIS")

#GET /your-api-endpoint/?page=2&page_size=5

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


#---------------HOTEL CART FOOD APIS--------------------------

# Eg:
# {
#     "product":1,
#     "quantity":1,
#     "CustomerFullName":"dimoso junior",
#     "PhoneNumber":"0765456743",
#     "CustomerAddress":"magomeni",
#     "room":1,
#     "table":1
# }
    
    



class HotelFoodCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelFoodCartItems.objects.filter(cart=cart)
        serializer = HotelFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelFoodCart.objects.get_or_create(user=user, ordered=False)
        product = HotelFoodProducts.objects.get(id=data.get('product'))

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            table=table,
            room=room,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelFoodCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelFoodCartItems.objects.get(id=data.get('cartId'))
        cart_item.delete()

        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelFoodCartItems.objects.filter(cart=cart)
        serializer = HotelFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelFoodDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelFoodCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelFoodCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelFoodOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = HotelFoodOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = HotelFoodCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create HotelFoodOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = HotelFoodOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create HotelFoodOrderItems instances for better performance
    #     HotelFoodOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)



#----------------MAKE ORDER FOOD WITH ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelFoodCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelFoodOrder.objects.create(user=user, total_price=total_price)

        total_cart_items = HotelFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                room=cart_item.room,
                table=cart_item.table,
                price=cart_item.price,
                quantity=cart_item.quantity,
                Customer=cart_item.Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)



    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelFoodOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#-------------------WITHOU ROOM-------------------------




#-------------------ADD TO CART AND MAKE ORDER WITHOUT ROOM

class HotelFoodAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelFoodCart.objects.get_or_create(user=user, ordered=False)
        product = HotelFoodProducts.objects.get(id=data.get('product'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        
        table = HotelTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})











#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class HotelFoodOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = HotelFoodOrder.objects.create(user=user, total_price=total_price)

        cart_items = HotelFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = HotelFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(HotelFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = HotelFoodOrder.objects.filter(user=user)
        serializer = HotelFoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)










































#---------------HOTEL CART DRINKS APIS--------------------------




class HotelDrinksCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelDrinksCartItems.objects.filter(cart=cart)
        serializer = HotelDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = HotelDrinksProducts.objects.get(id=data.get('product'))

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            table=table,
            room=room,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelDrinksCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelDrinksCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelDrinksCartItems.objects.filter(cart=cart)
        serializer = HotelDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelDrinksDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelDrinksCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelDrinksOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = HotelDrinksOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = HotelDrinksCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create HotelDrinksOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = HotelDrinksOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create HotelDrinksOrderItems instances for better performance
    #     HotelDrinksOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelDrinksCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelDrinksOrder.objects.create(user=user, total_price=total_price)

        total_cart_items = HotelDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                room=cart_item.room,
                table=cart_item.table,
                price=cart_item.price,
                quantity=cart_item.quantity,
                Customer=cart_item.Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = HotelDrinksOrder.objects.filter(user=user)
    #     serializer = HotelDrinksOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelDrinksOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#-------------------WITHOU ROOM-------------------------




#-------------------ADD TO CART AND MAKE ORDER WITHOUT ROOM

class HotelDrinksAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = HotelDrinksProducts.objects.get(id=data.get('product'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        
        table = HotelTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})
















#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class HotelDrinksOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = HotelDrinksOrder.objects.create(user=user, total_price=total_price)

        cart_items = HotelDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = HotelFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(HotelDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = HotelDrinksOrder.objects.filter(user=user)
        serializer = HotelDrinksOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






















#---------------HOTEL CART ROOMS APIS--------------------------


# ADD ROOM TO THE CART
#  {
#      "room":3,
#      "quantity":1,
#      "CustomerFullName":"saidi abdallah",
#      "PhoneNumber":"+25567534562",
#      "CustomerAddress":"iyunga",
#      "DaysNumber":3,
#       "table":1


#  }


class HotelRoomsCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelRoomsCartItems.objects.filter(cart=cart)
        serializer = HotelRoomsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelRoomsCart.objects.get_or_create(user=user, ordered=False)
        room = HotelRooms.objects.get(id=data.get('room'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))
        #table = HotelTables.objects.get(id=data.get('table'))
        price = room.price
        #quantity = data.get('quantity')
        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')
        DaysNumber = data.get('DaysNumber')

        # Check if the requested quantity is available in stock
        if room.ProductQuantity != 1:
            return Response({'error': 'This room has not available'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelRoomsCartItems(
            cart=cart,
             user=user,
             room=room,
             price=price,
             Customer=Customer,
             # CustomerFullName=CustomerFullName,
             # PhoneNumber=PhoneNumber,
             # CustomerAddress=CustomerAddress,
             DaysNumber=DaysNumber
             )
        cart_items.save()

        # Decrease the room quantity in stock
        room.ProductQuantity -= 1
        room.save()

        cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelRoomsCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelRoomsCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelRoomsCartItems.objects.filter(cart=cart)
        serializer = HotelRoomsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelRoomsDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelRoomsCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.room.ProductQuantity += cart_item.quantity
            cart_item.room.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsCartItems.DoesNotExist:
            return Response({"error": "Room not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelRoomsOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    # def post(self, request):
    #     user = request.user
    #     data = request.data

    #     CustomerFullName = data.get('CustomerFullName')
    #     PhoneNumber = data.get('PhoneNumber')
    #     CustomerAddress = data.get('CustomerAddress')
    #     DaysNumber = data.get('DaysNumber')

    #     total_price = request.data.get('total_price', 0)  # You may calculate this on the server
    #     cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     with transaction.atomic():  # Use a transaction to ensure data consistency

    #         order = HotelRoomsOrder.objects.create(user=user, total_price=total_price)

    #         total_cart_items = HotelRoomsCartItems.objects.filter(user=user)

    #         total_price = 0
    #         for items in total_cart_items:
    #             total_price += items.price
    #         order.total_price = total_price
    #         order.save()

    #         # Retrieve cart items and add them to the order
    #         cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart)
            

    #         order_items = []
    #         for cart_item in total_cart_items:
                
    #             order_item = HotelRoomsOrderItems(
    #                 user=user,
    #                 order=order,
    #                 room=cart_item.room,
    #                 price=cart_item.price,
    #                 quantity=cart_item.quantity,
    #                 CustomerFullName=cart_item.CustomerFullName,
    #                 PhoneNumber=cart_item.PhoneNumber,
    #                 CustomerAddress=cart_item.CustomerAddress,
    #                 DaysNumber=cart_item.DaysNumber
    #             )
    #             order_items.append(order_item)

    #         # Bulk create HotelDrinksOrderItems instances for better performance
    #         HotelRoomsOrderItems.objects.bulk_create(order_items)

    #         # Add the cart items to the order's ManyToManyField
    #         order.orderItems.set(order_items)


    #         # Update RoomStatus to True for ordered rooms
    #         for cart_item in cart_items:
    #             cart_item.room.RoomStatus = True
    #             cart_item.room.save()

    #         # Clear the user's cart
    #         cart_items.delete()
    #         cart.total_price = 0
    #         cart.ordered = True
    #         cart.save()




    #     return Response(HotelRoomsOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        data = request.data

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')
        DaysNumber = data.get('DaysNumber')

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        with transaction.atomic():  # Use a transaction to ensure data consistency

            order = HotelRoomsOrder.objects.create(user=user, total_price=total_price)

            total_cart_items = HotelRoomsCartItems.objects.filter(user=user)

            total_price = 0
            for items in total_cart_items:
                total_price += items.price
            order.total_price = total_price
            order.save()

            # Retrieve cart items and add them to the order
            cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart)
            for cart_item in cart_items:
                HotelRoomsOrderItems.objects.create(
                    user=user,
                    order=order,
                    room=cart_item.room,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    Customer=cart_item.Customer,
                    # CustomerFullName=cart_item.CustomerFullName,
                    # PhoneNumber=cart_item.PhoneNumber,
                    # CustomerAddress=cart_item.CustomerAddress,
                    DaysNumber=cart_item.DaysNumber
                )


            # Update RoomStatus to True for ordered rooms
            for cart_item in cart_items:
                cart_item.room.RoomStatus = True
                cart_item.room.save()

            # Clear the user's cart
            cart_items.delete()
            cart.total_price = 0
            cart.ordered = True
            cart.save()




        return Response(HotelRoomsOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = HotelRoomsOrder.objects.filter(user=user)
    #     serializer = HotelRoomsOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = HotelRoomsOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelRoomsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



































#------------------------RESTAURANT CARTS ZINAANZIA HAPA--------------







#---------------Restaurant CART FOOD APIS--------------------------




class RestaurantFoodCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantFoodCartItems.objects.filter(cart=cart)
        serializer = RestaurantFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantFoodProducts.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantFoodCartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RestaurantFoodCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RestaurantFoodCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantFoodCartItems.objects.filter(cart=cart)
        serializer = RestaurantFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RestaurantFoodDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RestaurantFoodCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RestaurantFoodOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RestaurantFoodOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RestaurantFoodCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RestaurantFoodOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RestaurantFoodOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RestaurantFoodOrderItems instances for better performance
    #     RestaurantFoodOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RestaurantFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RestaurantFoodCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RestaurantFoodOrder.objects.create(user=user, total_price=total_price)

        total_cart_items = RestaurantFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = RestaurantFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RestaurantFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                # room=cart_item.room,
                table=cart_item.table,
                price=cart_item.price,
                quantity=cart_item.quantity,
                Customer=cart_item.Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RestaurantFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RestaurantFoodOrder.objects.filter(user=user)
    #     serializer = RestaurantFoodOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RestaurantFoodOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RestaurantFoodOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RestaurantFoodOrder.objects.create(user=user, total_price=total_price)

        cart_items = RestaurantFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RestaurantFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RestaurantFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RestaurantFoodOrder.objects.filter(user=user)
        serializer = RestaurantFoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RestaurantFoodAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantFoodProducts.objects.get(id=data.get('product'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        
        table = RestaurantTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})






























#---------------Restaurant CART DRINKS APIS--------------------------




class RestaurantDrinksCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantDrinksCartItems.objects.filter(cart=cart)
        serializer = RestaurantDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantDrinksProducts.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantDrinksCartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RestaurantDrinksCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RestaurantDrinksCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantDrinksCartItems.objects.filter(cart=cart)
        serializer = RestaurantDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RestaurantDrinksDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RestaurantDrinksCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RestaurantDrinksOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RestaurantDrinksOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RestaurantDrinksCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RestaurantDrinksOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RestaurantDrinksOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RestaurantDrinksOrderItems instances for better performance
    #     RestaurantDrinksOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RestaurantDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RestaurantDrinksCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RestaurantDrinksOrder.objects.create(user=user, total_price=total_price)

        total_cart_items = RestaurantDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = RestaurantDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RestaurantDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                # room=cart_item.room,
                table=cart_item.table,
                price=cart_item.price,
                quantity=cart_item.quantity,
                Customer=cart_item.Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RestaurantDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RestaurantDrinksOrder.objects.filter(user=user)
    #     serializer = RestaurantDrinksOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RestaurantDrinksOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RestaurantDrinksOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RestaurantDrinksOrder.objects.create(user=user, total_price=total_price)

        cart_items = RestaurantDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RestaurantFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RestaurantDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RestaurantDrinksOrder.objects.filter(user=user)
        serializer = RestaurantDrinksOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RestaurantDrinksAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantDrinksProducts.objects.get(id=data.get('product'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        
        table = RestaurantTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})
















#RESTAURANTS CART ZINAISHIA HAPA-------------------------------







































#---------------------------RETAILS CART ZINAANZIA HAPA----------------












#---------------Retails CART FOOD APIS--------------------------




class RetailsFoodCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsFoodCartItems.objects.filter(cart=cart)
        serializer = RetailsFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsFoodProducts.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsFoodCartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RetailsFoodCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RetailsFoodCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsFoodCartItems.objects.filter(cart=cart)
        serializer = RetailsFoodCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RetailsFoodDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RetailsFoodCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RetailsFoodOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RetailsFoodOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RetailsFoodCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RetailsFoodOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RetailsFoodOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RetailsFoodOrderItems instances for better performance
    #     RetailsFoodOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RetailsFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RetailsFoodCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RetailsFoodOrder.objects.create(user=user, total_price=total_price)

        total_cart_items = RetailsFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = RetailsFoodCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RetailsFoodOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                # room=cart_item.room,
                table=cart_item.table,
                price=cart_item.price,
                quantity=cart_item.quantity,
                Customer=cart_item.Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RetailsFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    # def get(self, request):
    #     user = request.user
    #     orders = RetailsFoodOrder.objects.filter(user=user)
    #     serializer = RetailsFoodOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RetailsFoodOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RetailsFoodOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RetailsFoodOrder.objects.create(user=user, total_price=total_price)

        cart_items = RetailsFoodCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RetailsFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RetailsFoodOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RetailsFoodOrder.objects.filter(user=user)
        serializer = RetailsFoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    



#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RetailsFoodAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsFoodCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsFoodProducts.objects.get(id=data.get('product'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        
        table = RetailsTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsFoodCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsFoodCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})






























#---------------Retails CART DRINKS APIS--------------------------




class RetailsDrinksCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsDrinksCartItems.objects.filter(cart=cart)
        serializer = RetailsDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsDrinksProducts.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsDrinksCartItems(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RetailsDrinksCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RetailsDrinksCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsDrinksCartItems.objects.filter(cart=cart)
        serializer = RetailsDrinksCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RetailsDrinksDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RetailsDrinksCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RetailsDrinksOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RetailsDrinksOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RetailsDrinksCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RetailsDrinksOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RetailsDrinksOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RetailsDrinksOrderItems instances for better performance
    #     RetailsDrinksOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RetailsDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RetailsDrinksCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = RetailsDrinksOrder.objects.create(user=user, total_price=total_price)

        total_cart_items = RetailsDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = RetailsDrinksCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RetailsDrinksOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                # room=cart_item.room,
                table=cart_item.table,
                price=cart_item.price,
                quantity=cart_item.quantity,
                Customer=cart_item.Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RetailsDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RetailsDrinksOrder.objects.filter(user=user)
    #     serializer = RetailsDrinksOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelFoodOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelFoodOrder.objects.all().order_by('-id')
            orders = RetailsDrinksOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RetailsDrinksOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RetailsDrinksOrder.objects.create(user=user, total_price=total_price)

        cart_items = RetailsDrinksCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RetailsFoodCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RetailsDrinksOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RetailsDrinksOrder.objects.filter(user=user)
        serializer = RetailsDrinksOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    





#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RetailsDrinksAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsDrinksCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsDrinksProducts.objects.get(id=data.get('product'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        
        table = RetailsTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsDrinksCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsDrinksCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})

























#-----------------REPORT------------------------------------------


#------------HOTEL FOOD REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelFoodOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelFoodOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelFoodOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelFoodOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class HotelFoodOrderReportView(APIView):
    #-------------TO GET ALL ORDERS WITH PAGINATION
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelFoodOrder.objects.all().order_by('-id')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelFoodOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelFoodOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

























#------------HOTEL Drinks REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelDrinksOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelDrinksOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelDrinksOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelDrinksOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class HotelDrinksOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelDrinksOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelDrinksOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelDrinksOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#------------HOTEL Rooms REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelRoomsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelRoomsOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelRoomsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelRoomsOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelRoomsOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelRoomsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION

class HotelRoomsOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelRoomsOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelRoomsOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelRoomsOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = HotelRoomsOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelRoomsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





























#------------Restaurant FOOD REPORT--------------------------







#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RestaurantFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RestaurantFoodOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RestaurantFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RestaurantFoodOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RestaurantFoodOrderReportView(APIView):
#     def get(self, request):
#         orders = RestaurantFoodOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RestaurantFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RestaurantFoodOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RestaurantFoodOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RestaurantFoodOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RestaurantFoodOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

















#------------Restaurant Drinks REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RestaurantDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RestaurantDrinksOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RestaurantDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RestaurantDrinksOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RestaurantDrinksOrderReportView(APIView):
#     def get(self, request):
#         orders = RestaurantDrinksOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RestaurantDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION

class RestaurantDrinksOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RestaurantDrinksOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RestaurantDrinksOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RestaurantDrinksOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


























#------------Retails FOOD REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RetailsFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RetailsFoodOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RetailsFoodOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RetailsFoodOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RetailsFoodOrderReportView(APIView):
#     def get(self, request):
#         orders = RetailsFoodOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RetailsFoodOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RetailsFoodOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RetailsFoodOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RetailsFoodOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RetailsFoodOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RetailsFoodOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsFoodOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




























#------------Retails Drinks REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RetailsDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RetailsDrinksOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RetailsDrinksOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RetailsDrinksOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RetailsDrinksOrderReportView(APIView):
#     def get(self, request):
#         orders = RetailsDrinksOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RetailsDrinksOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RetailsDrinksOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RetailsDrinksOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RetailsDrinksOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RetailsDrinksOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))

            orders = RetailsDrinksOrder.objects.filter(
                user__id__icontains = userId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsDrinksOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)























#------------------FILTER   REPORT--------------------------






#---------------HOTEL FILTER REPORT---------------

#-------------TO FILTER ORDER ITEMS-------------------
# class FilterHotelFoodOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelFoodOrderItems.objects.filter(
#             Created__gte=startDate, Created__lte=endDate
#         )

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("price"))["price__sum"]

#         serializer = HotelFoodOrderItemsSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)







class FilterHotelFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = HotelFoodOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)














class FilterHotelDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = HotelDrinksOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)




class FilterHotelRoomsOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = HotelRoomsOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelRoomsOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)

















#---------------Restaurant FILTER REPORT---------------


class FilterRestaurantFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = RestaurantFoodOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RestaurantFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)







class FilterRestaurantDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = RestaurantDrinksOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RestaurantDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)
























#---------------RETAILS FILTER REPORT---------------


class FilterRetailsFoodOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = RetailsFoodOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RetailsFoodOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)







class FilterRetailsDrinksOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # Filter orders based on date range
        orders = RetailsDrinksOrder.objects.filter(
            created__gte=startDate, created__lte=endDate
        ).order_by('-id')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RetailsDrinksOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)








#-----------------RECEIPT ORDER--------------------

#kama untaka order za mda huo tu anapoadd kwenye cart huyo user tumia hii ya chini
# class HotelFoodReceiptView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     # kama unatumia JWT weka hiyo tu
#     # permission_classes =[IsAuthenticated]

# #RETRIEVE CART ITEMS FROM A CART
#     def get(self, request):
#         user = request.user
#         order = HotelFoodOrder.objects.filter(user=user).first()
#         queryset = HotelFoodOrderItems.objects.filter(order=order)
#         serializer = HotelFoodOrderItemsSerializer(queryset, many=True)

#         return Response(serializer.data)


#kama unataka orders zote za huyo users basi tunatumia hii ya chini
class HotelFoodReceiptView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = HotelFoodOrder.objects.filter(user=user)
        order_items = []

        for order in orders:
            queryset = HotelFoodOrderItems.objects.filter(order=order)
            serializer = HotelFoodOrderItemsSerializer(queryset, many=True)
            order_items.extend(serializer.data)

        return Response(order_items, status=status.HTTP_200_OK)



































# ------------------------HOTEL ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS FOOD----------------------

class GetHotelFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#----------------GET ALL ORDERED ITEMS DRINKS----------------------

class GetHotelDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#----------------GET ALL ORDERED ITEMS ROOMS----------------------

class GetHotelRoomsOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelRoomsOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelRoomsOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


























# ------------------------Restaurant ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS FOOD----------------------

class GetRestaurantFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RestaurantFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RestaurantFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#----------------GET ALL ORDERED ITEMS DRINKS----------------------

class GetRestaurantDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RestaurantDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RestaurantDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)























# ------------------------Retails ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS FOOD----------------------

class GetRetailsFoodOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RetailsFoodOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RetailsFoodOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#----------------GET ALL ORDERED ITEMS DRINKS----------------------

class GetRetailsDrinksOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RetailsDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RetailsDrinksOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


























#-------------------CHANGE  ORDER STATUS----------------------






#----------------------HOTEL FOOD CHANGE ORDER STATUS-------------------


class HotelFoodOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelFoodOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelFoodOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelFoodOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#----------------------HOTEL DRINKS CHANGE ORDER STATUS-------------------


class HotelDrinksOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelDrinksOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelDrinksOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelDrinksOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------------HOTEL ROOMS CHANGE ORDER STATUS-------------------


class HotelRoomsOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelRoomsOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelRoomsOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelRoomsOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

























#----------------------------RESTAURANT ORDER STATUS---------------------------


#----------------------RESTAURANT FOOD CHANGE ORDER STATUS-------------------


class RestaurantFoodOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantFoodOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RestaurantFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantFoodOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantFoodOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RestaurantFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------------RESTAURANT DRINKS  CHANGE ORDER STATUS-------------------


class RestaurantDrinksOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantDrinksOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RestaurantDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantDrinksOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantDrinksOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RestaurantDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





















#----------------------------Retails ORDER STATUS---------------------------


#----------------------Retails FOOD CHANGE ORDER STATUS-------------------


class RetailsFoodOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsFoodOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RetailsFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsFoodOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsFoodOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RetailsFoodOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------------Retails DRINKS  CHANGE ORDER STATUS-------------------


class RetailsDrinksOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsDrinksOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RetailsDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsDrinksOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsDrinksOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RetailsDrinksOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#-------------------DELETE ORDERS  ITEMS--------------------------

# EG: http://127.0.0.1:8000/Cart/HotelFoodDeleteOrderItem/?cartId=14





#----------------DELETE HOTEL FOOD ORDERED ITEMS---------------------
class HotelFoodDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelFoodOrderItems.objects.get(id=cartId)
            plus_order = HotelFoodOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelFoodOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE HOTEL DRINKS ORDERED ITEMS---------------------
class HotelDrinksDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelDrinksOrderItems.objects.get(id=cartId)
            plus_order = HotelDrinksOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelDrinksOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#----------------DELETE HOTEL ROOMS ORDERED ITEMS---------------------
class HotelRoomsDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelRoomsOrderItems.objects.get(id=cartId)
            plus_order = HotelRoomsOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.room.ProductQuantity += order_item.quantity
            #order_item.room.ProductQuantity += 1

            order_item.room.RoomStatus = False

            order_item.room.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrderItems.DoesNotExist:
            return Response({"error": "room not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





















#----------------DELETE Restaurant FOOD ORDERED ITEMS---------------------
class RestaurantFoodDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RestaurantFoodOrderItems.objects.get(id=cartId)
            plus_order = RestaurantFoodOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantFoodOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE Restaurant DRINKS ORDERED ITEMS---------------------
class RestaurantDrinksDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RestaurantDrinksOrderItems.objects.get(id=cartId)
            plus_order = RestaurantDrinksOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantDrinksOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------DELETE Retails FOOD ORDERED ITEMS---------------------
class RetailsFoodDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RetailsFoodOrderItems.objects.get(id=cartId)
            plus_order = RetailsFoodOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsFoodOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE Retails DRINKS ORDERED ITEMS---------------------
class RetailsDrinksDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RetailsDrinksOrderItems.objects.get(id=cartId)
            plus_order = RetailsDrinksOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            order_item.delete()

            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsDrinksOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

