from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from MarketPlace.models import Product,  Wishlist
from .serializers import  WishlistSerializer
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class WishlistCreateView(views.APIView):

    serializer_class = WishlistSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_STRING, description="The product's ID (uuid string)"),
            }),
        responses={
            201: openapi.Response('product added to wishlist successfully', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Message response from server"),
                    'product_details': openapi.Schema(type=openapi.TYPE_OBJECT, description="The added product's details"),                
                }
            )),
            400: openapi.Response('bad request', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Message response from server"),                
                }
            )),
            404: openapi.Response('cannot find provided product', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Message response from server"),                
                }
            )),
        })

    
    def post(self, request):

        if not request.data.get("product_id"):
            return Response({'message': 'product required in the request data'}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data.get("product_id")

        try:
            # Retrieve product details 
            Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({"message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the product to the user's wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user_id=request.user.id, product_id=product_id)

        serializer = self.serializer_class(wishlist_item)

        if created:
            return Response({'message': 'Product added to wishlist', 'wishlist_item': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Product already exists in wishlist', 'wishlist_item': serializer.data}, status=status.HTTP_200_OK)