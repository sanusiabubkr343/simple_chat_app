from rest_framework import mixins
from rest_framework import generics, status, viewsets, filters
from .models import User
from .serializers import LoginUserSerializer,UserSignUpSerializer,ListUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user



class UserViewSets(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ListUserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST'],
        detail=False,
        serializer_class=UserSignUpSerializer,
        url_path='signup',
    )
    def signup_user(self, request, pk=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user= serializer.save()
        
            response = {"message": "User Created Successfully", "data": ListUserSerializer(instance=user).data}
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        detail=False,
        serializer_class=LoginUserSerializer,
        url_path='login',
        
    )
    def login_user(self, request, pk=None):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(email=email, password=password)
            if user is not None:

                tokens = create_jwt_pair_for_user(user)

                response = {
                        "message": "Login Successful",
                        "tokens": tokens,
                        **ListUserSerializer(instance=user).data,
                    }

                return Response(data=response, status=status.HTTP_200_OK)

            else:
                return Response(
                    data={"message": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
