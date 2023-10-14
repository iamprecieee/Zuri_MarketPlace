from django.urls import path
from .views import GetCategoryNames, GetImages, GetProductsSubCategory

urlpatterns = [
        path('categoryNames/', GetCategoryNames.as_view(), name='category-names'),
        # path('image/<imageId>/', GetImage.as_view(), name='images'),
        path('image/<productId>/', GetImages.as_view(), name='product-images'),
        path('products/<str:category>/<str:subcategory>/', GetProductsSubCategory.as_view(), name='product-sub-category'),
        # not working yet

]
