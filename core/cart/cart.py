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
        else:
            new_item = {
                "product_id":product_id,
                "quantity":1
            } 
            self._cart["items"].append(new_item)
        self.save()


    def update_product_quantity(self, product_id):
        product = ProductModel.objects.get(id=product_id)

        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                if product.stock > item["quantity"] and item["quantity"] > 0:
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
        

    
    def save(self):
        self.session.modified = True