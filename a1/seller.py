import grpc
import time
import market_pb2
import market_pb2_grpc
from uuid import uuid5, NAMESPACE_DNS
from concurrent import futures

class SellerClient:
    def __init__(self, server_ip, port_id):
        self.server_ip=server_ip
        # self.server_port=server_port
        self.channel = grpc.insecure_channel(server_ip)
        self.stub = market_pb2_grpc.MarketServiceStub(self.channel)
        print("Connected to Market server")

    def register_seller(self, seller_address, seller_uuid):
        request = market_pb2.RegisterSellerRequest(seller_address=seller_address,uuid=seller_uuid)
        response = self.stub.RegisterSeller(request)
        # print("Market prints:", response)
        print("Seller prints: SUCCESS" if response.status == market_pb2.RegisterSellerResponse.Status.SUCCESS else "Seller prints: FAIL")

    def sell_item(self, product, seller_uuid):
        request = market_pb2.SellItemRequest(
            product=product,
            seller_uuid=seller_uuid
        )
        response = self.stub.SellItem(request)
        # print("Market prints:")
        if response.status == market_pb2.SellItemResponse.Status.SUCCESS:
            print("Seller prints: SUCCESS. Item ID:", response.item_id)
        else:
            print("Seller prints: FAIL")

    def update_item(self, item_id, new_price, new_quantity, seller_address, seller_uuid):
        request = market_pb2.UpdateItemRequest(
            item_id=item_id,
            new_price=new_price,
            new_quantity=new_quantity,
            seller_address=seller_address,
            seller_uuid=seller_uuid
        )
        response = self.stub.UpdateItem(request)
        # print("Market prints:", response)
        print("Seller prints: SUCCESS" if response.status == market_pb2.UpdateItemResponse.Status.SUCCESS else "Seller prints: FAIL")

    def delete_item(self, item_id, seller_address, seller_uuid):
        request = market_pb2.DeleteItemRequest(
            item_id=item_id,
            seller_address=seller_address,
            seller_uuid=seller_uuid
        )
        response = self.stub.DeleteItem(request)
        # print("Market prints:", response)
        print("Seller prints: SUCCESS" if response.status == market_pb2.DeleteItemResponse.Status.SUCCESS else "Seller prints: FAIL")
    
    def display_seller_items(self, seller_address, seller_uuid):
        request = market_pb2.DisplaySellerItemsRequest(
            seller_address=seller_address,
            seller_uuid=seller_uuid
        )
        response = self.stub.DisplaySellerItems(request)
        # print("Market prints:", response)
        # print("Seller prints:")
        for product in response.products:
            print("Item ID:", product.id)
            print("Name:", product.name)
            print("Price:", product.price)
            print("Category:", market_pb2.Product.ItemCategory.Name(product.category))
            print("Description:", product.description)
            print("Quantity Remaining:", product.quantity)


class SellerNotify(market_pb2_grpc.SellerNotificationServiceServicer):
    def NotifySeller(self, request, context):
        print("Notification received:", request.message)
        return market_pb2.Notification(message="Notification received")
        # return market_pb2.NotifySellerResponse(status=market_pb2.NotifySellerResponse.Status.SUCCESS)
    
    # server.wait_for_termination()

def run(port_id,server_ip,seller_ip):
    username = input("Enter Username: ")
    seller_uuid = uuid5(NAMESPACE_DNS, username).hex
    seller = SellerClient(server_ip,port_id)

    # seller.register_seller(market_pb2.Address(ip="localhost",port=50051), seller_uuid)
    while(True):
        menu=["Register Seller","Sell items","Update item","Delete item","Display Seller items","Exit"]
        for i in range(len(menu)):
            print(f"{i+1}. {menu[i]}")
        c=int(input(""))
        try:
            if(c==1):
                seller.register_seller(market_pb2.Address(ip=seller_ip,port=port_id), seller_uuid)
            elif(c==2):
                name=input("Enter name of product: ")
                category=input("Enter category of product: ")
                category=market_pb2.Product.ItemCategory.Value(category.upper())
                description=input("Enter description of product: ")
                quantity=int(input("Enter quantity of product: "))
                price=float(input("Enter price of product: "))
                seller.sell_item(product=market_pb2.Product(id=0, name=name, category=category, description=description, quantity=quantity, price=price, rating=0), seller_uuid=seller_uuid)
            elif(c==3): 
                item_id=int(input("Enter item id: "))
                new_price=float(input("Enter new price of product: "))
                new_quantity=int(input("Enter new quantity of product: "))
                seller.update_item(item_id=item_id, new_price=new_price, new_quantity=new_quantity, seller_address=market_pb2.Address(ip=seller_ip, port=port_id), seller_uuid=seller_uuid)
            elif(c==4):
                item_id=int(input("Enter item id: "))
                seller.delete_item(item_id=item_id, seller_address=market_pb2.Address(ip=seller_ip, port=port_id), seller_uuid=seller_uuid)
            elif(c==5):
                seller.display_seller_items(seller_address=market_pb2.Address(ip=seller_ip, port=port_id), seller_uuid=seller_uuid)
            elif(c==6):
                break
            else:
                print("Invalid input")
        except Exception as e:
            print("That didn't work. Try again. Error:", e)

def serve(port,server_ip,seller_ip):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_SellerNotificationServiceServicer_to_server(SellerNotify(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Notification server started, listening on " + port)
    run(port,server_ip,seller_ip)

if __name__ == "__main__":
    # server_ip="localhost:50050"
    server_ip = input("Enter server IP(ip:port): ")
    # port_id="50051"
    seller_ip = input("Enter seller IP(ip): ")
    port_id = input("Enter port number(port): ")
    serve(port_id,server_ip,seller_ip)
