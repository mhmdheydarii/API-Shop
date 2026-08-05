from .cart import CartSession


def cart_products(request):
    cart = CartSession(request.session)
    return {"cart":cart}