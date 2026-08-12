from .models import CartItemModel, CartModel
from shop.models import ProductModel

class CartSession:

    def __init__(self, session):
        self.session = session
        self._cart = self.session.get(
            "cart",
            {
                "items":[]
            }
        )
        self.session["cart"] = self._cart


    def add_product(self, product_id, product_stock):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if product_stock > item["quantity"]:
                    item["quantity"] += 1
                    self.save()
                    return True
                else:
                    return False
        new_item = {
            "product_id":product_id,
            "quantity":1
        } 
        if product_stock > 0:
            self._cart["items"].append(new_item)

            self.save()
            return True
        
        return False

    def update_product_quantity(self, product_id):
        product = ProductModel.objects.get(id=product_id, status=True)

        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if product.stock > item["quantity"]:
                    item["quantity"] += 1
                    self.save()
                    return True
                else:
                    return False

        return False


    def remove_product(self, product_id):

        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                self.save()
                return True
            
        return False
        

    def get_product_item(self):
        cart_items = self._cart["items"]
        for item in cart_items:
            try:
                product = ProductModel.objects.get(id=item["product_id"])
                item["product_obj"] = {
                    "id":product.id,
                    "name":product.name,
                    "image":product.image.url,
                    "stock":product.stock,
                    "price":int(product.get_price())
                }
                item.update(
                    {
                        "product_obj":item["product_obj"],
                        "total_price":item["quantity"] * product.get_price(),
                    }
                )
            except ProductModel.DoesNotExist:
                self._cart["items"].remove(item)
                self.save()
        return cart_items

    

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])    

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])

    
    def save(self):
            self.session.modified = True

    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()


    def sync_session_cart_to_db(self, user):
        cart, created = CartModel.objects.get_or_create(user=user)

        for item in self._cart["items"]:
            product = ProductModel.objects.get(
                id=item["product_id"],
                status=True
            )

            cart_item, created = CartItemModel.objects.get_or_create(
                cart=cart,
                product=product
            )

            cart_item.quantity = item["quantity"]
            cart_item.save()

    def merge_session_cart_in_db(self, user):

        cart, created = CartModel.objects.get_or_create(user=user)

        for item in self._cart["items"]:
            product = ProductModel.objects.get(id=item["product_id"], status=True)
            cart_item, created = CartItemModel.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += item["quantity"]
            cart_item.save()
        session_product_ids = (item["product_id"] for item in self._cart["items"])
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()