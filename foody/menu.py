import typing

import exceptions


class Food(object):
    def __init__(self, name: str):
        self.name: str = name

    def get_food_name(self) -> str:
        return self.name


class Menu(object):
    def __init__(self, food_item: str, price: float):
        self.food_item: Food = Food(food_item)
        self.price: float = price

    def get_item(self) -> str:
        return self.food_item.get_food_name()

    def get_price(self) -> float:
        return self.price

    def update_price(self, price: float):
        self.price = price


class MenuCard(object):

    def __init__(self):
        # {paneer_tikka : Menu(paneer_tikka)}
        self.menu_card: typing.Dict[str, Menu] = {}

    def add_item(self, food_item: str, value: float) -> bool:
        if food_item in self.menu_card:
            raise exceptions.ItemAlreadyExistsRestaurantException
        self.menu_card[food_item] = Menu(food_item, value)
        return True

    def update_item(self, food_item: str, value: float) -> bool:
        if food_item not in self.menu_card:
            raise exceptions.ItemDoesNotExistsRestaurantException
        menu_item = self.menu_card[food_item]
        menu_item.update_price(value)
        return True

    def food_exists(self, food_item: str):
        if food_item not in self.menu_card:
            return False
        return True

    def get_price(self, food_item: str):
        return self.menu_card[food_item].get_price()
