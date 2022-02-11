from typing import *
import abc

cyfry = [str(x) for x in range(0, 10)]
znaki = [chr(x) for x in range(97, 122 + 1)]


class Product:
    produkty = []

    def __init__(self, name: str, price: float):
        has_char = False
        has_number = False
        i = 0
        for char in name[1:]: # sprawdzanie czy w nazwie występuje przynajmniej jedna cyfra
            if char in cyfry:
                has_number = True
        for char in name: # sprawdzanie czy w nazwie występuje przynajmniej jeden znak
            if char.lower() in znaki:
                i += 1
                has_char = True
            else:
                if i == 0: # sprawdzenie czy na pierwszym miejscu jest cyfra - błąd
                    raise ValueError("Nazwa nie zaczyna się od litery")
                else:
                    for x in name[i:]: # sprawdzenie czy po pierwszej natrafionej cyfrze występują jakieś litery - błąd
                        if x.lower() in znaki:
                            raise ValueError("Błędna nazwa! Litery występują po cyfrach")
        if has_number and has_char:
            self.name = name
        else:
            raise ValueError("Błędna nazwa produktu")

# sprawdzenie poprawności danych dla ceny
        if type(price) == float or type(price) == int:
            self.price = price
            Product.produkty.append((self.name, self.price))
        else:
            raise ValueError("Błędna cena produktu")

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class AServer:
    n_max_returned_entries = 3
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_entries(self, n_letters: int = 1):
        products_list = []
        for elem in Product.produkty:
            n_letters_product = 0
            n_numbers = 0
            for c in elem[0]:
                if c not in cyfry:
                    n_letters_product += 1
                else:
                    n_numbers += 1
            if n_letters_product <= n_letters and (2 <= n_numbers <= 3):
                products_list.append(elem)
        sorted(products_list, key=lambda x: x[1])
        if len(products_list) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return products_list


class TooManyProductsFoundError(Exception):

    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, message=None):
        if message is None:
            message = 'Too many products'
        super().__init__(message)
        self.message = message


class ListServer(AServer):

    def __init__(self, products: list):
        super().__init__()
        self.products = products

    def get_entries(self, n_letters: int = 1):
        products_list = []
        for elem in self.products:
            n_letters_product = 0
            n_numbers = 0
            for c in elem.name:
                if c.lower() in znaki:
                    n_letters_product += 1
                else:
                    n_numbers += 1
            if n_letters_product == n_letters and (2 <= n_numbers <= 3):
                products_list.append(elem)
        sorted_products = sorted(products_list, key=lambda x: x.price)
        if len(products_list) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted_products


class MapServer(AServer):

    def __init__(self, products: list):
        super().__init__()
        self.list_products = products
        self.products = self.set_product_map()

    def set_product_map(self):
        product_map = {}
        for product in self.list_products:
            product_map[product.name] = product
        return product_map

    def get_entries(self, n_letters: int = 1):
        products_list = []
        products2 = self.products.values()
        for elem in products2:
            n_letters_product = 0
            n_numbers = 0
            for c in elem.name:
                if c.lower() in znaki:
                    n_letters_product += 1
                else:
                    n_numbers += 1
            if n_letters_product == n_letters and (2 <= n_numbers <= 3):
                products_list.append(elem)
        sorted_products = sorted(products_list, key=lambda x: x.price)
        if len(products_list) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted_products


class Client:
    def __init__(self, server: AServer):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            products = self.server.get_entries(n_letters)
        except:
            return None
        if len(products) == 0:
            return None
        result = 0
        for product in products:
            result = product.price+result
        return result
