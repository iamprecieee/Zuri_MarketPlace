from rest_framework import serializers
from MarketPlace.models import UserProductInteraction
from MarketPlace.models import Product,ProductImage
from .currencies import currency_data
from all_products.serializers import AllProductImageSerializer

class UserProductInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductInteraction
        fields = '__all__'

class ProductItemSerializer(serializers.ModelSerializer):
    currency_symbol = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
			'id', 'shop', 'name', 'description', 'quantity', 'category', 'price', 'images',
			'discount_price', 'tax', 'admin_status', 'is_deleted', 'rating', 'is_published',
			'currency', 'currency_symbol', 'createdat', 'updatedat', 'user'
		]

    def get_currency_symbol(self, obj):
        currency_code = getattr(obj, 'currency')#getting the currency code of the product 
        currency_code = str(currency_code).upper()#changing the currency code to string and then to uppercase
        currency_symobol = currency_data.get(currency_code, "$")#getting the corresponding currency symbol default of dollar symbol if the symbol is not found
        return currency_symobol

    def get_images(self, obj):
        qs = ProductImage.objects.filter(product=obj)
        return AllProductImageSerializer(qs, many=True, context=self.context).data
