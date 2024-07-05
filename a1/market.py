from concurrent import futures
import grpc
import time
import market_pb2
import market_pb2_grpc

# _ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MarketService(market_pb2_grpc.MarketServiceServicer):
    def __init__(self):
        # Placeholder for seller data
        self.sellers = {}
        # Placeholder for buyer data
        self.buyer= {}
        # Placeholder for item data
        self.items = {}
        self.items_rating = {}
        self.items_wishlist = {}

    def RegisterSeller(self, request, context): 
        seller_uuid = request.uuid
        if seller_uuid in self.sellers:
            return market_pb2.RegisterSellerResponse(status=market_pb2.RegisterSellerResponse.Status.FAILED)
        else:
            self.sellers[seller_uuid] = request.seller_address
            print("Market prints: Seller join request from", request.seller_address.ip + ":" + request.seller_address.port, "[ip:port], uuid =", seller_uuid)
            return market_pb2.RegisterSellerResponse(status=market_pb2.RegisterSellerResponse.Status.SUCCESS)
        
    def RegisterBuyer(self, request, context): 
        buyer_uuid = request.uuid
        self.buyer[buyer_uuid] = request.buyer_address
        # print("Market prints: Buyer join request from", request.buyer_address.ip + ":" + request.buyer_address.port, "[ip:port], uuid =", buyer_uuid)
        return market_pb2.RegisterBuyerResponse(status=market_pb2.RegisterSellerResponse.Status.SUCCESS)
    
    def SellItem(self, request, context):
        seller_uuid = request.seller_uuid
        if seller_uuid not in self.sellers:
            return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.Status.FAILED)
        product = request.product
        product.seller_address.ip = self.sellers[seller_uuid].ip
        product.seller_address.port = self.sellers[seller_uuid].port
        item_id = len(self.items) + 1  # Generate unique item ID
        product.id = item_id
        self.items[item_id] = product
        self.items_rating[item_id] = {}
        print("Market prints: Sell Item request from", self.sellers[seller_uuid].ip + ":" + self.sellers[seller_uuid].port, "[seller address]")
        return market_pb2.SellItemResponse(status=market_pb2.SellItemResponse.Status.SUCCESS, item_id=item_id)

    def UpdateItem(self, request, context):
        seller_uuid = request.seller_uuid
        if seller_uuid not in self.sellers:
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.Status.FAILED)

        item_id = request.item_id
        if item_id not in self.items:
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.Status.FAILED)
        
        if self.items[item_id].seller_address.ip != self.sellers[seller_uuid].ip or self.items[item_id].seller_address.port != self.sellers[seller_uuid].port:
            return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.Status.FAILED)
        self.items[item_id].price = request.new_price
        self.items[item_id].quantity = request.new_quantity
        
        print("Market prints: Update Item", item_id, "request from", self.sellers[seller_uuid].ip + ":" + self.sellers[seller_uuid].port, "[seller address]")
        # print(self.items_wishlist[item_id])
        # print(self.items[item_id])
        for i in range(len(self.items_wishlist[item_id])):
            channel = grpc.insecure_channel(self.items_wishlist[item_id][i])
            stub = market_pb2_grpc.BuyerNotificationServiceStub(channel)
            request = market_pb2.ItemUpdateNotification(product=self.items[item_id],message="Item " + str(item_id) + " updated.")
            response = stub.NotifyClient(request)
        return market_pb2.UpdateItemResponse(status=market_pb2.UpdateItemResponse.Status.SUCCESS)

    def DeleteItem(self, request, context):
        seller_uuid = request.seller_uuid
        if seller_uuid not in self.sellers:
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.Status.FAILED)
        
        if request.item_id not in self.items:
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.Status.FAILED)
        
        if self.items[request.item_id].seller_address.ip != self.sellers[seller_uuid].ip or self.items[request.item_id].seller_address.port != self.sellers[seller_uuid].port:
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.Status.FAILED)
        
        item_id = request.item_id
        if item_id in self.items:
            del self.items[item_id]
            print("Market prints: Delete Item", item_id, "request from", self.sellers[seller_uuid].ip + ":" + self.sellers[seller_uuid].port, "[seller address]")
            if item_id in self.items_wishlist:
                del self.items_wishlist[item_id]
            if item_id in self.items_rating:
                del self.items_rating[item_id]
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.Status.SUCCESS)
        else:
            return market_pb2.DeleteItemResponse(status=market_pb2.DeleteItemResponse.Status.FAILED)

    def DisplaySellerItems(self, request, context):
        seller_uuid = request.seller_uuid
        products = []
        for item_id, product in self.items.items():
            if product.seller_address.ip == request.seller_address.ip and product.seller_address.port == request.seller_address.port:
                products.append(product)
        print("Market prints: Display Items request from", self.sellers[seller_uuid].ip + ":" + self.sellers[seller_uuid].port, "[seller address]")
        return market_pb2.DisplaySellerItemsResponse(products=products)

    def SearchItem(self, request, context):
        products = []
        for item_id, product in self.items.items():
            if request.item_name == "" or request.item_name.lower() in product.name.lower():
                if request.category == market_pb2.SearchItemRequest.ItemCategory.ANY or request.category == product.category:
                    products.append(product)
        print("Market prints: Search request for Item name:", request.item_name, ", Category:", request.category)
        return market_pb2.SearchItemResponse(products=products)

    def BuyItem(self, request, context):
        item_id = request.item_id
        if item_id not in self.items:
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.Status.FAILED)

        product = self.items[item_id]
        if product.quantity < request.quantity:
            return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.Status.FAILED)

        product.quantity -= request.quantity
        print("Market prints: Buy request", request.quantity, "of item", item_id, "from", request.buyer_address.ip + ":" + request.buyer_address.port, "[buyer address]")
        channel = grpc.insecure_channel(self.items[item_id].seller_address.ip + ":" + self.items[item_id].seller_address.port)
        stub = market_pb2_grpc.SellerNotificationServiceStub(channel)
        req = market_pb2.Notification(message="Item " + str(item_id) + " sold " + str(request.quantity) + " times.")
        response = stub.NotifySeller(req)
        return market_pb2.BuyItemResponse(status=market_pb2.BuyItemResponse.Status.SUCCESS)

    def AddToWishlist(self, request, context):
        item_id = request.item_id
        if item_id not in self.items:
            return market_pb2.AddToWishlistResponse(status=market_pb2.AddToWishlistResponse.Status.FAILED)
        if item_id not in self.items_wishlist:
            self.items_wishlist[item_id] = []
        self.items_wishlist[item_id].append(request.buyer_address.ip + ":" + request.buyer_address.port)
        print("Market prints: Wishlist request of item", item_id, "from", request.buyer_address.ip + ":" + request.buyer_address.port, "[buyer address]")
        return market_pb2.AddToWishlistResponse(status=market_pb2.AddToWishlistResponse.Status.SUCCESS)
    
    def RateItem(self, request, context):
        item_id = request.item_id
        buyer_address=request.buyer_address.ip + ":" + request.buyer_address.port
        if item_id not in self.items:
            return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.Status.FAILED)
        elif buyer_address in self.items_rating[item_id]:
            return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.Status.FAILED)
        rating= request.rating
        print(request.buyer_address.ip + ":" + request.buyer_address.port, "rated item", item_id, "with", rating, "stars.")
        self.items_rating[item_id][buyer_address]=rating
        self.items[item_id].rating= sum(self.items_rating[item_id].values())/len(self.items_rating[item_id])
        return market_pb2.RateItemResponse(status=market_pb2.RateItemResponse.Status.SUCCESS)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServiceServicer_to_server(MarketService(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("Market server started...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
