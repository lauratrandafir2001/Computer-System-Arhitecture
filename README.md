# Project Memory Allocator

# About
Computing Systems Architecture course
https://ocw.cs.pub.ro/courses/asc

April 2023

Student:  Trandafir Laura;

# Implementation:

# class Cart:
    Class that represents a cart.
    Used to store a list of tuples (product, quantity)
    and a cart id.
    - helper class


# class Producers_and_products:
    Class that represents a producer and his/hers
    list of products.
    Used to store a list of products, the id of the producer
    , and the number of products.
    - helper class

# class Marketplace:
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    
    - def register_producer(self):
     creates a new Producers_and_products and adds it to the list
     of Producers_and_products, returning the new producer id

    - def publish(self, producer_id, product):
    finds the producer with the producer_id given and adds the product
    to his list of products if the queue_size_per_producer hasn't reach
    the maximum size

    - def new_cart(self):
    creates a new Cart() object, increases  self.cart_id_counter,
    adds it to the list of carts, and returns the new cart id

    - def add_to_cart(self, cart_id, product):
    looks for the cart with the given id, and for the product in the list
    from each producer and if it finds the product it adds it
    to the cart list of tuples, with the producer id corresponding to it
    it also removes it from the producer list of products

    - def remove_from_cart(self, cart_id, product):
    looks for the cart with the given id
    looks for the given product in the cart, and saves the producer id
    removes it from the cart
    looks for the producer with the found_it and appends the product to his/hers list

    - def place_order(self, cart_id):
    it adds the products from the given cart in a list and returns the list

# class Producer:
    Class that represents a producer.

    - def run(self):
    first, the class registers a producer
    and in the while true loop, it iterates through the products
    we create another loop to consider the quantity specified in the input data
    we call publish function with the producer id and the product given
    if publish returns True, we increase num_ops(that helps us with the quantity of the product)
    and we put it to sleep within the given time
    if the publishing method returns False, then the queue is full and it has to wait
    the republish_wait_time before it tries to publish it again

# class Consumer:
    Class that represents a consumer.
    - def run(self):
    we iterate through the carts given in the input data
    we create a new cart with the new_cart() method
    we iterate through the operations we have to do 
    we use a while to keep count of the quantity given
    if the operation type is "add" we call self.marketplace.add_to_cart()
    if it returns True, we increase num_ops and move on
    if it returns False, we sleep for the retry_wait_time
    and after it, we try again
    if the operation is "remove", we call self.marketplace.remove_from_cart()
    and increase num_ops
    the order is placed and we print the result using a lock, for the threads
    to not write simultaneously



References:
- [""Fire de executie in Python](https://ocw.cs.pub.ro/courses/asc/laboratoare/02)
- [Programare concurentă în Python](https://ocw.cs.pub.ro/courses/asc/laboratoare/03)
- [Producer consumer problem](https://www.youtube.com/watch?v=l6zkaJFjUbM)
- [Classes in python](https://www.w3schools.com/python/python_classes.asp)


