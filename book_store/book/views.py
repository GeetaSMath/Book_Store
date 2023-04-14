import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer, AllBookSerializer
from user.models import User
from user.utils import verify_superuser,verify_token



class BookAPI(APIView):
    @verify_superuser
    def post(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Book added", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_superuser
    def get(self, request):
        try:
            book_list = Book.objects.all()
            serializer = AllBookSerializer(book_list, many=True)
            return Response({"message": "Data retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_superuser
    # @verify_token
    def put(self, request):
        try:
            book_object = Book.objects.get(id=request.data.get("id"))
            serializer = BookSerializer(book_object, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Update successful", "data": serializer.data},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_superuser
    def delete(self, request):
        try:
            book_object = Book.objects.get(id=request.data.get("id"))
            book_object.delete()
            return Response({"message": "Book deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
