import collections
import typing


class User:
    def __init__(self, name, age, orders):
        self.name = name
        self.orders: typing.Dict[str, typing.List[int]] = collections.defaultdict(list)

    def create_order(self, restaurant_id, order_id):
        self.orders[restaurant_id].append(order_id)


class Users:
    def __init__(self):
        # {'deb': User(deb)}
        self.users: typing.Dict[str, User] = {}

    def create_user(self, name):
        if name in self.users:
            print('User already exists')
            return
        self.users[name] = User(name)

