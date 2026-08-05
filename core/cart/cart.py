from .models import CartItemModel, CartModel


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


    def save(self):
        self.session.modified = True