import json
import logging
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer
from .utils import JWT
from .models import User

class Register(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer)
            return Response({"message": "User registered successfully", 'status': 201, 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as err:
            logging.exception(err)
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    # def post(self, request):
    #     """
    #      for logging of the user
    #     """
    #     try:
    #         serializer = LoginSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         token = JWT().encode(data={"user_id": serializer.data.get("id")})
    #         return Response({'message': 'Login successfully!', 'status': 202},
    #                         status=status.HTTP_202_ACCEPTED)
    #     except Exception as err:
    #         logging.exception(err)
    #         return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        """
            This method logins registration based on username and password.
            Returns login success or failed...
        """
        try:
            data = json.loads(request.body)
            # data.update({"user":request.user.id})

            if request.method == 'POST':
                user = authenticate(username=data.get('username'), password=data.get('password'))
                login(request,user)
                token = JWT().encode(data={"user_id": user.id})
                if user:
                    return JsonResponse({"message": "login succesfully", "token": token, "status": 201}, status=201)
                return JsonResponse({"message": "invalid credentials ", "status": 406}, status=406)
            return JsonResponse({"message": "method not allowed", "status": 405}, status=405)
        except Exception as e:
            logging.exception(e)
            return JsonResponse({"data": {}, "message": e.args[0], "status": 400}, status=400)




class VerifyToken(APIView):
    def get(self, request, token=None):
        try:
            decoded = JWT().decode(token)
            user = User.objects.get(username=decoded.get("username"))
            if not user:
                raise Exception("Invalid user")
            user.is_verified = True
            user.save()
            return Response("Token verified")
        except Exception as e:
            logging.exception(e)
            return Response(str(e), status=400)
