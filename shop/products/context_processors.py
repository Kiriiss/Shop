from products.models import Cart

def baskets(request):
    user = request.user
    return {'baskets':Cart.objects.filter(user=user) if user.is_authenticated else []}