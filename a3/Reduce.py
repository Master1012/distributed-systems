# syntax = "proto3"

# message Centroid {
#     repeated double coordinates = 1
# }

# message DataPoint {
#     repeated double points = 1
# }

# message MapTaskRequest {
#     int32 mapper_id = 1
#     int32 num_mappers = 2
#     int32 num_reducers = 3
#     int32 num_iterations = 4
#     string input_file_path = 5
#     int32 start_index = 6
#     int32 end_index = 7
#     repeated Centroid centroids = 8
# }

# message MapResponse {
#     string status = 1
#     string message = 2
# }

# message ReduceTaskRequest {
#     int32 reducer_id = 1
#     int32 num_mappers = 2
#     int32 num_reducers = 3
#     repeated Centroid centroids = 4
# }

# message ReduceTaskResponse {
#     bool success = 1
#     string message = 2
#     repeated Centroid centroids = 3
# }

# message ReceiveKeyValuesRequest {
#     int32 reducer_id = 1
# }

# message ReceiveKeyValuesResponse {
#     bool success = 1
#     repeated DataPoint data_points = 2
# }

# service KMeansMapReduce {
#     rpc MapTask(MapTaskRequest) returns(MapResponse)
#     rpc ReduceTask(ReduceTaskRequest) returns(ReduceTaskResponse)
#     rpc ReceiveKeyValues(ReceiveKeyValuesRequest) returns(ReceiveKeyValuesResponse)
# }
import grpc
import multiprocessing
from concurrent import futures
import mapreduce_pb2 as pb2
import mapreduce_pb2_grpc as pb2_grpc
import sys
import os
import random


class Reducer(pb2_grpc.KMeansMapReduceServicer):
    def __init__(self):
        self.reducer_id = 0
        self.centroids = []
        self.allocated_data = []
        self.num_mappers = 0
        self.num_reducers = 0
        # stores the mapping of centroid_id to updated centroid coordinates.
        self.updated_centroids = {}

    def ReduceTask(self, request, context):
        print(f"Reducer {request.reducer_id} received request")
        self.reducer_id = request.reducer_id
        self.num_mappers = request.num_mappers
        self.num_reducers = request.num_reducers
        self.centroids = [list(centroid.coordinates)
                          for centroid in request.centroids]
        self.allocated_data = []
        updated_centroids = self.receiveKeyValues()
        print(f"Reducer {self.reducer_id} completed")
        self.Save_centroids()
        return pb2.ReduceTaskResponse(success=True, message=f"Reducer {self.reducer_id} completed", centroids=[pb2.Centroid(coordinates=centroid) for centroid in updated_centroids])

    def Shuffle_and_sort(self):
        sorted_dict = {}
        for entry in self.allocated_data:
            if entry[0] in sorted_dict:
                sorted_dict[entry[0]].append(entry[1])
            else:
                sorted_dict[entry[0]] = [entry[1]]
        return sorted_dict

    def receiveKeyValues(self):
        print(f"Reducer {self.reducer_id} is receiving data points...")
        request = pb2.ReceiveKeyValuesRequest(reducer_id=self.reducer_id)
        for i in range(self.num_mappers):
            with grpc.insecure_channel(f'localhost:400{i}') as channel:
                stub = pb2_grpc.KMeansMapReduceStub(channel)
                response = stub.ReceiveKeyValues(request)
                data = response.data_points
                # self.allocated_data = [{data_point.centroid: data_point.points} for data_point in response.data_points]
                for d in data:
                    # if d.centroid_id not in self.allocated_data:
                    #     self.allocated_data[d.centroid_id] = []
                    # self.allocated_data[d.centroid_id].append(d.points)
                    self.allocated_data.append((d.centroid_id, d.points))
        print(
            f"Reducer {self.reducer_id} received {len(self.allocated_data)} data points")
        updated_centroids = self.Reduce()
        # return [pb2.Centroid(coordinates=centroid) for centroid in updated_centroids]
        return updated_centroids

    def Reduce(self):
        sorted_dict = self.Shuffle_and_sort()
        self.updated_centroids = {}
        for key in sorted_dict:
            points = sorted_dict[key]
            if (len(points) == 0):
                self.updated_centroids[key] = self.centroids[key]
            else:
                self.updated_centroids[key] = self.update_centroid(points)
        print(self.updated_centroids)
        return list(self.updated_centroids.values())

    def update_centroid(self, points):
        centroid = [0] * len(points[0])
        for point in points:
            for i in range(len(point)):
                centroid[i] += point[i]
        for i in range(len(centroid)):
            centroid[i] /= len(points)
        return centroid

    def Save_centroids(self):
        path = f"Reducers/Reducer{self.reducer_id}.txt"
        # check if the file exists
        if not (os.path.exists(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            for entry in self.updated_centroids:  # self.updated_centroids is a dictionary
                file.write(f"{entry} {self.updated_centroids[entry]}\n")


def run(i,r):
    flag = random.randint(1,10)
    if flag <= r:
        # os.kill(os.getpid(), 9)
        sys.exit()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_KMeansMapReduceServicer_to_server(Reducer(), server)
    port = f'[::]:500{i}'
    server.add_insecure_port(f'{port}')
    print(f"Reducer server started, listening on port {port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run()
