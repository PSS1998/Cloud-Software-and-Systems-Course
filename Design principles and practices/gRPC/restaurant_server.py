import grpc
import sys
from concurrent import futures
from proto import restaurant_pb2
from proto import restaurant_pb2_grpc

RESTAURANT_ITEMS_FOOD = ["chips", "fish", "burger", "pizza", "pasta", "salad"]
RESTAURANT_ITEMS_DRINK = ["water", "fizzy drink", "juice", "smoothie", "coffee", "beer"]
RESTAURANT_ITEMS_DESSERT = ["ice cream", "chocolate cake", "cheese cake", "brownie", "pancakes", "waffles"]

def check_orders_availible(menu, orders):
    for order in orders:
        if order not in menu:
            return False
    return True

class Restaurant(restaurant_pb2_grpc.RestaurantServicer):
    def FoodOrder(self, request, context):
        id = request.orderID
        orders = request.items
        if check_orders_availible(RESTAURANT_ITEMS_FOOD, orders):
            status = "ACCEPTED"
        else:
            status = "REJECTED"
        return restaurant_pb2.RestaurantResponse(orderID=id, status=status)

    def DrinkOrder(self, request, context):
        id = request.orderID
        orders = request.items
        if check_orders_availible(RESTAURANT_ITEMS_DRINK, orders):
            status = "ACCEPTED"
        else:
            status = "REJECTED"
        return restaurant_pb2.RestaurantResponse(orderID=id, status=status)

    def DessertOrder(self, request, context):
        id = request.orderID
        orders = request.items
        if check_orders_availible(RESTAURANT_ITEMS_DESSERT, orders):
            status = "ACCEPTED"
        else:
            status = "REJECTED"
        return restaurant_pb2.RestaurantResponse(orderID=id, status=status)

def serve():
    port = int(sys.argv[1])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_pb2_grpc.add_RestaurantServicer_to_server(Restaurant(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
