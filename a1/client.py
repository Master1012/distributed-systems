import grpc
import market_pb2
import market_pb2_grpc
from uuid import uuid5, NAMESPACE_DNS
from concurrent import futures

class BuyerClient:
    def __init__(self, server_address,port_id):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = market_pb2_grpc.MarketServiceStub(self.channel)

    def register_buyer(self, buyer_address, buyer_uuid):
        request = market_pb2.RegisterBuyerRequest(buyer_address=buyer_address,uuid=buyer_uuid)
        response = self.stub.RegisterBuyer(request)
        # print("Market prints:", response)

    def search_item(self, item_name="", category=market_pb2.SearchItemRequest.ItemCategory.ANY):
        request = market_pb2.SearchItemRequest(item_name=item_name,category=category)
        response = self.stub.SearchItem(request)
        print("Buyer prints:")
        for product in response.products:
            print("Item ID:", product.id)
            print("Name:", product.name)
            print("Price:", product.price)
            print("Category:", market_pb2.Product.ItemCategory.Name(product.category))
            print("Description:", product.description)
            print("Quantity Remaining:", product.quantity)
            print("Rating:", product.rating)
            print("Seller:", product.seller_address)

    def buy_item(self, item_id, quantity, buyer_address):
        request = market_pb2.BuyItemRequest(item_id=item_id,quantity=quantity,buyer_address=buyer_address)
        response = self.stub.BuyItem(request)
        print("Market prints:", response)
        print("Buyer prints: SUCCESS" if response.status == market_pb2.BuyItemResponse.Status.SUCCESS else "Buyer prints: FAIL")

    def add_to_wishlist(self, item_id, buyer_address):
        request = market_pb2.AddToWishlistRequest(item_id=item_id,buyer_address=buyer_address)
        response = self.stub.AddToWishlist(request)
        print("Market prints:", response)
        print("Buyer prints: SUCCESS" if response.status == market_pb2.AddToWishlistResponse.Status.SUCCESS else "Buyer prints: FAIL")

    def rate_item(self, item_id, buyer_address, rating):
        request = market_pb2.RateItemRequest(item_id=item_id,buyer_address=buyer_address,rating=rating)
        response = self.stub.RateItem(request)
        print("Market prints:", response)
        print("Buyer prints: SUCCESS" if response.status == market_pb2.RateItemResponse.Status.SUCCESS else "Buyer prints: FAIL")


    # def Notify(self, request, context):
    #     product=request.product
    #     print("Notification prints:", request.message)
    #     print("Item ID:", product.id)
    #     print("Name:", product.name)
    #     print("Price:", product.price)
    #     print("Category:", product.category)
    #     print("Description:", product.description)
    #     print("Quantity Remaining:", product.quantity)
    #     print("Rating:", product.rating)
    #     print("Seller:", product.seller_address)
    #     return market_pb2.NotifySellerResponse(status=market_pb2.NotifySellerResponse.Status.SUCCESS)
    
def run(port_id,server_ip,client_ip):
    buyer = BuyerClient(server_ip,port_id)
    username = input("Enter Username: ")
    client_uuid = uuid5(NAMESPACE_DNS, username).hex
    buyer.register_buyer(market_pb2.Address(ip=client_ip,port=port_id), client_uuid)
    while(True):
        menu=["Search Item","Buy Item","Add to Wishlist","Rate Item","Exit"]
        for i in range(len(menu)):
            print(f"{i+1}. {menu[i]}")
        c=int(input(""))
        try:
            if c==1:
                item_name = input("Enter Item Name: ")
                category = input("Enter Category: ")
                if(category==""):
                    buyer.search_item(item_name=item_name)
                else:
                    buyer.search_item(item_name=item_name, category=market_pb2.SearchItemRequest.ItemCategory.Value(category.upper()))
            elif c==2:
                item_id = int(input("Enter Item ID: "))
                quantity = int(input("Enter Quantity: "))
                buyer.buy_item(item_id=item_id, quantity=quantity, buyer_address=market_pb2.Address(ip=client_ip, port=port_id))
            elif c==3:
                item_id = int(input("Enter Item ID: "))
                buyer.add_to_wishlist(item_id=item_id, buyer_address=market_pb2.Address(ip=client_ip, port=port_id))
            elif c==4:
                item_id = int(input("Enter Item ID: "))
                rating = int(input("Enter Rating: "))
                buyer.rate_item(item_id=item_id, buyer_address=market_pb2.Address(ip=client_ip, port=port_id), rating=rating)
            elif c==5:
                break
            else:
                print("Invalid Option")
        except Exception as e:
            print("That didn't work:", e)

def serve(port,server_ip,client_ip):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_BuyerNotificationServiceServicer_to_server(BuyerNotify(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Notification server started, listening on " + port)
    run(port,server_ip,client_ip)
    # server.wait_for_termination()

class BuyerNotify(market_pb2_grpc.BuyerNotificationServiceServicer):
    def NotifyClient(self, request, context):
        product=request.product
        print("Notification received:", request.message)
        print("Item ID:", product.id)
        print("Name:", product.name)
        print("Price:", product.price)
        print("Category:", market_pb2.Product.ItemCategory.Name(product.category))
        print("Description:", product.description)
        print("Quantity Remaining:", product.quantity)
        print("Rating:", product.rating)
        print("Seller:", product.seller_address)
        return market_pb2.Notification(message="Notification received")


if __name__ == "__main__":
    # port_id = "50052"
    # server_ip="localhost:50050"
    server_ip = input("Enter server IP(ip:port): ")
    client_ip = input("Enter client IP(ip): ")
    port_id = input("Enter client port(port): ")
    serve(port_id,server_ip,client_ip)
