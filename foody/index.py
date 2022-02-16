import collections
import typing

class SearchIndex:

    def __init__(self):
        self.index: typing.Dict[str, typing.Set[str]] = collections.defaultdict(set)

    def update_index(self, restaurant_id: str, food_item: str):
        self.index[food_item].add(restaurant_id)

    def search(self, food_item: str) -> typing.List[str]:
        restaurants = self.index.get(food_item)
        if not restaurants:
            return []
        else:
            return list(restaurants)


