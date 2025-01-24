import json
from cart import dao
from products import Product

class Cart:
    def __init__(self, id: int, username: str, contents: list, cost: float):
        """
        Initializes the Cart instance.
        
        :param id: The unique identifier for the cart.
        :param username: The username associated with the cart.
        :param contents: The list of Product objects in the cart.
        :param cost: The total cost of the items in the cart.
        """
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data: dict) -> 'Cart':
        """
        Class method to load cart data from a dictionary.

        :param data: The dictionary containing the cart data.
        :return: A Cart instance.
        """
        return cls(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> list:
    """
    Retrieves the user's cart and loads the products into the cart.

    :param username: The username for which the cart should be fetched.
    :return: A list of Product objects in the user's cart.
    """
    cart_details = dao.get_cart(username)  # Fetch cart details from the DAO
    if cart_details is None:
        return []

    items = []
    for cart_detail in cart_details:
        contents = cart_detail['contents']
        
        try:
            evaluated_contents = json.loads(contents)  # Safely load contents from JSON
        except json.JSONDecodeError as e:
            print(f"Error decoding contents for cart {cart_detail['id']}: {e}")
            continue  # Skip this cart if it can't be decoded properly
        
        # Collect items from the contents
        for content in evaluated_contents:
            items.append(content)
    
    # Retrieve the actual product details from the products list
    products_in_cart = []
    for item in items:
        product = products.get_product(item)  # Assuming this fetches a Product object
        if product:
            products_in_cart.append(product)

    return products_in_cart

def add_to_cart(username: str, product_id: int):
    """
    Adds a product to the user's cart.

    :param username: The username of the user adding the product.
    :param product_id: The ID of the product to add to the cart.
    """
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    """
    Removes a product from the user's cart.

    :param username: The username of the user removing the product.
    :param product_id: The ID of the product to remove from the cart.
    """
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    """
    Deletes all products from the user's cart.

    :param username: The username of the user whose cart should be deleted.
    """
    dao.delete_cart(username)
