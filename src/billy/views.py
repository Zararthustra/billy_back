from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.models import User
from .models import Summary, Movement
from .serializers import SummarySerializer, MovementSerializer, UserSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    def post(self, request):
        try:
            User.objects.create_user(username=request.data["username"],
                                     password=request.data["password"])
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": "User already exist !"}, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AccountsMethods(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountMethods(APIView):
    permission_classes = [IsAdminUser]

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


class SummariesMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summaries = Summary.objects.filter(user=request.user)
        serializer = SummarySerializer(summaries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SummarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


class SummaryMethods(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        summary = Summary.objects.get(id=pk)
        serializer = SummarySerializer(summary, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        summary = get_object_or_404(Summary, pk=pk)
        movements = Movement.objects.filter(
            year=summary.year, month=summary.month, user=request.user)
        for movement in movements:
            movement.delete()
        summary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovementsMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movements = Movement.objects.filter(user=request.user)
        serializer = MovementSerializer(movements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data)


class MovementMethods(APIView):
    permission_classes = [IsAuthenticated]

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
