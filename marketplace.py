"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import unittest


class Cart:
    """
    Class that represents a cart.
    Used to store a list of tuples (product, quantity)
    and a cart id.
    """

    def __init__(self):
        self.products_and_id = []
        self.id = 0


class Producers_and_products:
    """
    Class that represents a producer and his/hers
    list of products.
    Used to store a list of products, the id of the producer
    and the number of products.
    """

    def __init__(self):
        self.products = []
        self.id = 0
        self.number_of_products = 0


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        # producer id
        self.producer_id = 0
        # list of available products from each producer
        self.producers = []
        self.cart_id_counter = 0
        self.carts = []
        self.new_cart_lock = Lock()
        self.lock_for_products_in_the_cart = Lock()
        self.register_producer_lock = Lock()
        self.publish_lock = Lock()
        self.lock_print = Lock()
        self.queue_size_per_producer = queue_size_per_producer

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.register_producer_lock:
            # create new producer
            new_producer = Producers_and_products()
            new_producer.id = str(self.producer_id)
            self.producer_id = self.producer_id + 1
            new_producer.number_of_products = 0
            new_producer.products = []
            # add new producer to the list of producers
            self.producers.append(new_producer)
            return str(new_producer.id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        with self.lock_for_products_in_the_cart:
            for producer in self.producers:
                if producer.id == producer_id:
                    # verify if the producer has reached the maximum number of products
                    if producer.number_of_products < self.queue_size_per_producer:
                        producer.products.append(product)
                        producer.number_of_products = producer.number_of_products + 1
                        return True
                    else:
                        return False
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        with self.lock_for_products_in_the_cart:
            # create new cart
            new_cart = Cart()
            new_cart.id = self.cart_id_counter
            self.cart_id_counter += 1
            new_cart.products_and_id = []
            # add new cart to the list of carts
            self.carts.append(new_cart)
            return new_cart.id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for cart in self.carts:
            if cart.id == cart_id:
                for producer in self.producers:
                    # if the product is in the list of products from the producer
                    if product in producer.products:
                        # we need to remove the product from the list of products
                        producer.products.remove(product)
                        producer.number_of_products = producer.number_of_products - 1
                        # we need to add the product and producer id to the list
                        cart.products_and_id.append((product, producer.id))
                        return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        found_id = -1
        for cart in self.carts:
            if cart.id == cart_id:
                # product, id_prod is a tuple
                for (product_x, id_prod) in cart.products_and_id:
                    if product_x == product:
                        found_id = id_prod
                        cart.products_and_id.remove((product_x, id_prod))
                        break
        # if the product is not in the cart
        if found_id == -1:
            return False

        for producer in self.producers:
            if found_id == producer.id:
                producer.products.append(product)
                return True

        return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products_list = []
        with self.lock_print:
            for cart in self.carts:
                if cart.id == cart_id:
                    for product in cart.products_and_id:
                        products_list.append(product[0])
                    break
            return products_list


class TestMarketplace(unittest.TestCase):
    """
    Unittest class
    """

    def setUp(self):
        """
        Setup for testing.
        """
        self.marketplace = Marketplace(2)

    def test_register_producer_true(self):
        """
        Test register_producer
        """
        for i in range(100):
            self.assertEqual(
                self.marketplace.register_producer(), str(i), True)

    def test_register_producer_false(self):
        """
        Test register_producer
        """
        for i in range(100):
            self.assertEqual(
                self.marketplace.register_producer(), str(i), False)

    def test_publish_true(self):
        """
        Test publish
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        result = self.marketplace.publish(producer_id, product)
        self.assertTrue(result)

    def test_publish_false(self):
        """
        Test publish
        """
        self.marketplace.register_producer()
        product = "product1"
        result = self.marketplace.publish(None, product)
        self.assertFalse(result)

    def test_new_cart_true(self):
        """
        Test new_cart
        """
        for i in range(100):
            self.assertEqual(self.marketplace.new_cart(), i, True)

    def test_new_cart_false(self):
        """
        Test new_cart
        """
        for i in range(100):
            self.assertEqual(self.marketplace.new_cart(), i, False)

    def test_add_to_cart_true(self):
        """
        Test add_to_cart
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        result = self.marketplace.add_to_cart(cart_id, product)
        self.assertTrue(result)

    def test_add_to_cart_false(self):
        """
        Test add_to_cart false assertion
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        self.marketplace.publish(producer_id, product)
        self.marketplace.new_cart()
        result = self.marketplace.add_to_cart(None, product)
        self.assertFalse(result)

    def test_remove_from_cart_true(self):
        """
        Test remove_from_cart
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product)
        result = self.marketplace.remove_from_cart(cart_id, product)
        self.assertTrue(result)

    def test_remove_from_cart_false(self):
        """
        Test remove_from_cart false assertion
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product)
        result = self.marketplace.remove_from_cart(None, product)
        self.assertFalse(result)

    def test_place_order_true(self):
        """
        Test place_order true assertion
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product)
        result = self.marketplace.place_order(cart_id)
        self.assertTrue(result, [product])

    def test_place_order_false(self):
        """
        Test place_order false assertion
        """
        producer_id = self.marketplace.register_producer()
        product = "product1"
        self.marketplace.publish(producer_id, product)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product)
        result = self.marketplace.place_order(cart_id)
        self.assertTrue(result, [product])
