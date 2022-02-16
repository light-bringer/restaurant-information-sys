import typing
from menu import Food
import constants


# class FoodOrder:
#     def __init__(self, quantity: int, food_item: str, price: float):
#         self.quantity: quantity = quantity
#         self.food: Food = Food(food_item)
#         self.price: float = price


class Order:
    def __init__(self, food_items: typing.Dict[str, typing.List[int]]):
        self.status: str = constants.OrderStatus.ORDERED
        self.order_details: typing.Dict[str, typing.List[int]] = food_items
        # {paneer_tikka : [quantity, price]}
        self.total_price: float = self.__calculate_total_price()

    def __str__(self):
        order_status = f"""
        order_details : {self.order_details} \n
        total_price : {self.total_price}
        status : {self.status}
        """
        return order_status

    def __repr__(self):
        return self.__str__()

    def __calculate_total_price(self):
        total_price = 0
        for item, price_quantity in self.order_details:
            quantity, price = price_quantity
            total_price += quantity*price
        return total_price

    def get_total_price(self):
        return self.total_price

    def get_order_status(self):
        return self.status

    def complete_order(self):
        self.status = constants.OrderStatus.COMPLETED

    def get_details(self):
        self.__repr__()


class Orders:
    def __init__(self):
        self.__COUNTER__ = 1
        self.orders: typing.Dict[int, Order] = {}

    def create_order(self, food_items: typing.Dict[str, typing.List[int]]):
        self.__COUNTER__ += 1
        order_id = self.__COUNTER__
        self.orders[order_id] = Order(food_items)
        return order_id

    def order_status(self, order_id: int):
        if order_id not in self.orders:
            return None
        return self.orders[order_id].get_order_status()

    def mark_as_completed(self, order_id: int):
        if order_id not in self.orders:
            print('order_id not found')
            return
        self.orders[order_id].complete_order()
