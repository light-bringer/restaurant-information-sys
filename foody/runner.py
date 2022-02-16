import os
import sys

import typing


current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path))
print(sys.path)


from user import Users
from restaurant import Restaurants


restaurants = Restaurants()
users = Users()


def create_user(name):
    users.create_user(name)


def onboard_restaurant(restaurant_name: str, rating: float, max_orders: int,  menu: typing.Dict[str, int]):
    restaurants.onboard_restaurant(restaurant_name, rating, max_orders, menu)


def order(food_details):
    restaurants.build_order(food_items=food_details)



def run():
    create_user('Harish')
    create_user('Manish')
    menu = {'shahi paneer': 275, 'matar paneer': 275}
    onboard_restaurant('restaurant_1', 4.5, 4, menu)


run()