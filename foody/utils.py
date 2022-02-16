import string


def validate_restaurant_name(restaurant_name: str) -> bool:
    for char in restaurant_name:
        if char in string.punctuation:
            return False
    return True


def convert_name_to_rid(restaurant_name: str) -> str:
    return f'rid_{restaurant_name.lower()}'


def convert_rid_to_name(restaurant_rid: str) -> str:
    return restaurant_rid[4:]
