from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.models import User
from .models import Summary, Movement
from .serializers import SummarySerializer, MovementSerializer, UserSerializer

from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    def post(self, request):
        try:
            User.objects.create_user(username=request.data["name"],
                                     password=request.data["password"])
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": "User already exist"}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class AccountsMethods(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class AccountMethods(APIView):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(
            user,
            data={
                "username": request.data["name"],
                "password": request.data["password"]
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class SummariesMethods(APIView):

    def get(self, request):
        summary = Summary.objects.all()
        serializer = SummarySerializer(summary, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class SummaryMethods(APIView):

    def put(self, request, pk):
        summary = Summary.objects.get(id=pk)
        serializer = SummarySerializer(summary, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        summary = get_object_or_404(Summary, pk=pk)
        summary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class MovementsMethods(APIView):

    def get(self, request):
        movements = Movement.objects.all()
        serializer = MovementSerializer(movements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class MovementMethods(APIView):

    def put(self, request, pk):
        movement = get_object_or_404(Movement, pk=pk)
        serializer = MovementSerializer(movement, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movement = get_object_or_404(Movement, pk=pk)
        movement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)