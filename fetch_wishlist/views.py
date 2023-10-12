from django.http import JsonResponse, HttpResponseServerError
from django.views import View
from MarketPlace.models import Wishlist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist 

class WishlistProductsView(View):
    def get(self, request, user_id):
        try:
            # Get all wishlist items for the user
            wishlist_items = Wishlist.objects.filter(user_id=user_id).order_by('-createdat')
            
            items_per_page = 5

            # Initialize Paginator with the wishlist_items and items_per_page
            paginator = Paginator(wishlist_items, items_per_page)
            
            page_number = request.GET.get('page')
            
            try:
                # Get the requested page
                page = paginator.page(page_number)
            except PageNotAnInteger:
                # If page is not an integer, deliver the first page.
                page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g., 9999), deliver the last page.
                page = paginator.page(paginator.num_pages)

            # Create a list of wishlist items for the current page
            wishlist_data = []
            for item in page:
                data = {
                    'product_id': item.product_id,
                    'created_at': item.createdat,
                    'updated_at': item.updatedat,
                }
                wishlist_data.append(data)
            
            response_data = {
                'wishlist': wishlist_data,
                'paginator': {
                    'num_pages': paginator.num_pages,
                    'per_page': items_per_page,
                }
            }
            
            return JsonResponse(response_data)
        except ObjectDoesNotExist:
            # Handle the case where the user_id or wishlist_items do not exist
            return JsonResponse({'error': 'User or wishlist not found'}, status=404)
        except Exception as e:
            print(e)
            # Handle other exceptions, such as database errors
            return HttpResponseServerError(f'Server Error: {str(e)}', status=500)