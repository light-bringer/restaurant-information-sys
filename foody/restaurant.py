import functools
import sys
import typing

import utils
from menu import MenuCard
from order import Orders
from search import SEARCH_IDX


class Restaurant:
    def __init__(self, r_id: str, name: str, rating: float, max_orders: int, menu: typing.Dict[str, float]):
        """
        :param r_id:
        :param name:
        :param rating:
        :param max_orders:
        :param menu: paneer tikka 124, chicken tikka 250
        """
        self.rid: str = r_id
        self.name: str = name
        self.rating: float = rating
        self.max_orders_count: int = max_orders
        self.current_order_count: int = 0
        self.menu_card: MenuCard = MenuCard()
        self.orders: Orders = Orders()
        for food_item, price in menu.items():
            self.update_menu(food_item, price)

    def __str__(self):
        return f'rid_{self.rid}_name_{self.name}'

    def __repr__(self):
        return self.__str__()

    def get_current_order_count(self) -> int:
        return self.current_order_count

    def update_menu(self, food_item: str, price: float):
        SEARCH_IDX.update_index(self.rid, food_item)
        if not self.menu_card.food_exists(food_item):
            self.menu_card.add_item(food_item, price)
            print(f'Item {food_item} price {price} added for restaurant {self.name}')
        else:
            self.menu_card.update_item(food_item, price)
            print(f'Item {food_item} price {price} updated for restaurant {self.name}')

    def can_take_order(self):
        if self.current_order_count >= self.max_orders_count:
            return False
        else:
            return True

    def create_order(self, food_items: typing.Dict[str, int]):
        order_detail = {}
        for food, quantity in food_items.items():
            order_detail[food] = [quantity, self.get_price(food)]

        if not self.can_take_order():
            print('already at max_limit of orders')
            return
        self.current_order_count += 1
        order_id = self.orders.create_order(order_detail)
        print(f'Order {order_id} created for Restaurant {self.rid}')

    def complete_order(self, order_id: int):
        self.current_order_count -= 1
        self.orders.mark_as_completed(order_id)

    def check_order_status(self, order_id: int):
        order_status = self.orders.order_status(order_id)
        if not order_status:
            print('Order does not exist for restaurant')
        print(f'Order status for {order_id} is {order_status}')

    def get_price(self, food_item: str, quantity: int = 1) -> float:
        if self.menu_card.food_exists(food_item):
            return self.menu_card.get_price(food_item)*quantity


class Restaurants:
    def __init__(self):
        self.restaurants: typing.Dict[str, Restaurant] = {}

    def __restaurant_exists(self, r_id: str):
        if r_id not in self.restaurants:
            return False
        return True

    def __get_restaurant(self, r_id: str):
        return self.restaurants.get(r_id)

    def onboard_restaurant(self, restaurant_name: str, rating: int, max_orders: int,  menu: typing.Dict[str, int]):
        if not utils.validate_restaurant_name(restaurant_name):
            print('Invalid Restaurant Name')
            return
        rid = utils.convert_name_to_rid(restaurant_name)
        if rid in self.restaurants:
            print('restaurant already exists')
            return

        self.restaurants[rid] = Restaurant(rid, restaurant_name, rating, max_orders, menu)
        print(f'{restaurant_name} onboarded successfully')

    def update_menu(self, r_id: str,  menu_items: typing.Dict[str, float]):
        if not self.__restaurant_exists(r_id):
            print('Invalid Restaurant ID')
            return
        for food_item, price in menu_items.items():
            restaurant = self.__get_restaurant(r_id)
            restaurant.update_menu(food_item, price)

    def get_total_price(self, r_id, food_items: typing.Dict[str, int]) -> float:
        if not self.__restaurant_exists(r_id):
            print('Invalid Restaurant ID')
            return

        restaurant = self.__get_restaurant(r_id)
        total_price: float = 0
        for food_item, quantity in food_items.items():
            price = restaurant.get_price(food_item)
            price_for_quantity = price * quantity
            total_price += price_for_quantity
        return total_price

    def create_order(self, restaurant_id: str, food_items):
        self.restaurants[restaurant_id].create_order(food_items)

    def build_order(self, food_items: typing[str, int]):
        restaurant_id = self.select_restaurant_price(food_items=food_items)
        if not restaurant_id:
            print('cannot order')
            return
        self.create_order(restaurant_id=restaurant_id)

    def select_restaurant_price(self, food_items, sort_type):
        restaurants_serving = []
        restaurant_can_take_order = []
        for food_item, _ in food_items.items():
            search_result = SEARCH_IDX.search(food_item)
            if not search_result:
                print('cannot take order because restaurants are either not taking order or food items not available')
                return None
            restaurants_serving.append(search_result)
        # [[1, 2, 4], [1, 2]]

        restaurants_serving_all = list(functools.reduce(lambda k, j: k & j, (set(x) for x in restaurants_serving)))
        # [1, 2]

        for restaurant in restaurants_serving_all:
            if self.restaurants[restaurant].can_take_order():
                restaurant_can_take_order.append(restaurant)

        if not restaurant_can_take_order:
            print('cannot take order because restaurants are either not taking order or food items not available')
            return None

        restaurant_to_order = None
        min_price = sys.maxsize
        for i in range(len(restaurant_can_take_order)):
            restaurant_id = restaurant_can_take_order[id]
            cur_min_price = self.get_total_price(restaurant_id, food_items)
            if min_price > cur_min_price:
                restaurant_to_order = restaurant_id
                min_price = cur_min_price
        # restaurant_can_take_order.sort(key=lambda self.restaurants[x] : for x in restaurant_can_take_order)
        # restaurant_to_order = restaurant_can_take_order[0]
        return restaurant_to_order
