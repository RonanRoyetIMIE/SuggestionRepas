from django.shortcuts import render

from django.http.response import JsonResponse
import requests
from rest_framework import views, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from api.models import User, Product

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from api.serializers import UserSerializer, RegisterSerializer, LoginSerializer, ProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to register.
    """
    def list(self, request):
        return Response('Register')

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(views.APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

# def getProductsWithCode(code):
#     return requests.get(
#         f'https://world.openfoodfacts.org/api/v2/product/{code}&fields=code,_keywords,brands,categories_tags,countries,name_fr,image_url,stores,ingredients_text,compared_to_category').json()


class ProductsByCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    def list(self, request, category):
        r = requests.get(
            f'https://world.openfoodfacts.org/?json=true&categories_tags={category}&page=1&fields=code,_keywords,brands,categories_tags,countries,name_fr,image_url,stores,ingredients_text').json()
        result = r['products']
        return JsonResponse(result, status=status.HTTP_201_CREATED, safe=False)

class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
        user_id=1
        return Product.objects.filter(user_id=user_id)

    def create(self, request):
        product = request.data
        serialized_product = ProductSerializer(data=product)
        print(serialized_product)
        if not serialized_product.is_valid():
            response = {}
            response['success'] = False
            response['message'] = serialized_product.errors
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

        serialized_product.save()
        response = serialized_product.data
        response['success'] = True
        return JsonResponse(response, status=status.HTTP_201_CREATED)
