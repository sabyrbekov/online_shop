from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import ProductModel
from .permissions import IsAdminUser
from .serializers import ProductSerializer, WishAPISerializer
from rest_framework.views import APIView
from rest_framework import serializers
from .models import Wish
from django.http import HttpResponseRedirect


User = get_user_model() 


class ProductListApiView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'title', 'price',)

    def get_queryset(self):
        price = self.request.query_params.get('price')
        queryset = super().get_queryset()
        if price:
            price_from, price_to = price.split('-')
            queryset = queryset.filter(
                price__gt=price_from, 
                price__lt=price_to
            )
        return queryset

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser )
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer



class WishListApiView(generics.ListCreateAPIView):
    serializer_class = WishAPISerializer

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user.id)

    def post(self, request, *args, **kwargs):
        if len(request.data.keys()) == 1 and request.data.get('product'):
            user = request.user.id
            product = request.data['product']
            favorites = Wish.objects.filter(product=product, user=user.id)
            if favorites:
                raise serializers.ValidationError('Product in WishList')
            request.data['user'] = request.user.id

        else:
            raise serializers.ValidationError('Error')
            pass
        return self.create(request, *args, **kwargs)


class WishAdd(APIView):
    
    def get(self, request, pk):
        product_= ProductModel.objects.all()
        #   Wish.objects.user = request.user 
        #     print(Wish.objects.user)
        #     # product = ProductModel.objects.all()
        product = ProductModel.objects.get(pk=product_.id)
        user = request.user
        # print(request.user)
        # print(user)
        url = request.build_absolute_uri()
        if Wish.objects.filter(user=user.id, product=product.id):
            raise serializers.ValidationError('This product in WishList')
        new_favorite = Wish.objects.create(user=user.id, product=product.id)
        return HttpResponseRedirect(redirect_to=url)


class WishDelete(APIView):

    def get(self, request, id):
        user = request.user
        favor = Wish.objects.filter(user=user.id, product=id)
        if favor:
            favor.delete()
            raise serializers.ValidationError('Deleted!')
        raise serializers.ValidationError('Not Found!')
