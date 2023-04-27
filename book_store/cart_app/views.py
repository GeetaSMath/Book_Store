from rest_framework.response import Response
from rest_framework.views import APIView
from cart_app.models import UserCart, UserCartItem
from cart_app.serializers import CartItemSerializer, CartSerializer

# Create your views here.
from user.utils import verify_user


class CartItemAPI(APIView):
    def post(self, request):
        try:
            request.data.update({"user": request.user})
            serializer = CartItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Cart Item Added Successfully', "status": 201, 'data': serializer.data},
                            status=201)
        except Exception as e:
            return Response({'message': str(e), 'status': 400}, status=400)

    def get(self, request, cart_id):
        try:
            cart = UserCart.objects.get(id=cart_id)
            cart_serializer = CartSerializer(cart, many=False)
            return Response({"message": "List of Cart Items", "data": cart_serializer.data, "status": 200})

        except Exception as e:
            return Response({"message": str(e)}, status=400)

    def delete(self, request, cart_item_id):
        try:
            cart_item = UserCartItem.objects.get(id=cart_item_id)
            cart_item.delete()
            return Response({"mesaage": "Cart Item Deleted Successfully", "status": 204})
        except Exception as e:
            return Response({"message": str(e)}, status=400)


class CheckoutAPI(APIView):
    @verify_user
    def put(self, request):
        user = UserCart.objects.get(user_id=request.user.id, status=False)
        if user is not None:
            user.status = True
            user.save()
        return Response({"Message": "status updated Successfully", 'status': 200})

    def get(self, request):
        try:
            cart = UserCartItem.objects.all()
            print(cart)
            serializer = CartItemSerializer(cart, many=True)
            return Response({'message': 'Book data retrieved successfully', 'data': serializer.data, 'status': 200},
                            status=200)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def delete(self, request):
        try:
            user_cart = UserCart.objects.get(user_id=request.data.get("user_id"), id=request.data.get('id'))
            print(user_cart)
            user_cart.delete()
            return Response({'message': 'Cart items deleted successfully', 'status': 204}, status=204)
        except UserCart.DoesNotExist:
            return Response({'message': 'User cart not found', 'status': 404}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
