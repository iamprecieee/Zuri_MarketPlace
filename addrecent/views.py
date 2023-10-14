from django.shortcuts import render
from rest_framework import generics
from MarketPlace.models import LastViewedProduct, UserProductInteraction, User, Product
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.utils import timezone
from django.http import Http404
from .serializers import UserProductInteractionSerializer, ProductItemSerializer
import uuid

# Create your views here.

class CreateRecentlyViewd(generics.GenericAPIView):
    serializer_class = UserProductInteractionSerializer
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('product_id')

        query_response = addRecentlyViewed(user_id=user_id, product_id=product_id)#this function attempts to create a recently viewed and returns a Response 
        return Response(query_response.data)        


class GetProductItem(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductItemSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('id')
        guest = request.query_params.get('guest')
        if guest == 'false':#user is signed up hence we update the recently viewed for that user
            qurery_response = addRecentlyViewed(user_id=user_id, product_id=product_id)#this function attempts to create a recently viewed and returns a Response
            if qurery_response.status_code == status.HTTP_201_CREATED:#this means the product has been added to recently viewed succesfully
                return super().retrieve(request, *args, **kwargs)
            else:
                return Response(qurery_response.data, status= qurery_response.status_code)
        else:#this means the person viewing this product is not signed up
            return super().retrieve(request, *args, **kwargs)


"""This function adds updates the users recently viewed and returns a resonse object"""
def addRecentlyViewed(user_id, product_id):
    current_time = timezone.now()#getting the current time 
    serializer_data = {
        "user": user_id,
        "product": product_id,
        "interaction_type": "viewed",
        "createdat": current_time
    }#constructing a data for the serializer

    serializer = UserProductInteractionSerializer(data=serializer_data)#initailizing a serializer for the provided data
    if serializer.is_valid():
        try: 
            user = User.objects.get(id = user_id)
        except ObjectDoesNotExist:
            return Response({'message', 'User not found'}, status= status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Product not found'}, status= status.HTTP_404_NOT_FOUND)
    

        last_viewed = LastViewedProduct.objects.filter(user=user)
        if last_viewed.exists():
            #deleting the previous last_viewed object corresponding to this user, user cant have two last viewed 
            last_viewed.delete()
        
        last_viewed_object = LastViewedProduct.objects.create(user=user,product=product, viewed_at =current_time)#creating a new last_viewed object 
        last_viewed_object.save()

        recently_viewed = UserProductInteraction.objects.filter(user=user, product=product)#getting the objects this user has recently viewed
        if recently_viewed.exists():
            #deleting the recent views with thesame user and thesame product because user cant reently view one product twice :)
            recently_viewed.delete()
        
        serializer.save()
        context = {
            'message': 'History updated successfully',
            'data': serializer.data
        }
        return Response(context, status= status.HTTP_201_CREATED)
    else:
        error_message = next(iter(serializer.errors.values()))[0]
        return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)

    

    
    
