import grpc
from concurrent import futures
import mapreduce_pb2 as pb2
import mapreduce_pb2_grpc as pb2_grpc
import threading
import os
import random
import sys

class Map(pb2_grpc.KMeansMapReduceServicer):
    def __init__(self):
        self.mapper_id = 0
        self.input_file_path = None
        self.start_index = 0
        self.end_index = 0
        self.centroids = None
        self.R = 0
        self.mapper_points = None
        self.partitions = []

    def MapTask(self, request, context):
        self.mapper_id = request.mapper_id
        self.input_file_path = request.input_file_path
        self.start_index = request.start_index
        self.end_index = request.end_index
        self.centroids = [list(centroid.coordinates)
                          for centroid in request.centroids]
        self.R = request.num_reducers
        self.mapper_points = []
        self.partitions = [[] for _ in range(self.R)]
        with open(self.input_file_path, 'r') as file:
            for i, line in enumerate(file):
                if i >= self.start_index and i < self.end_index:
                    point = list(map(float, line.strip().split(',')))
                    nearest_centroid = self.find_nearest_centroid(
                        point, self.centroids)
                    self.mapper_points.append((nearest_centroid, point))

        print(
            f"Mapper {self.mapper_id} mapped {len(self.mapper_points)} points")
        self.Partition()
        return pb2.MapResponse(status="SUCCESS", message="Map function completed successfully")

    def ReceiveKeyValues(self, request, context):
        print("Mapper received request")
        reducer_id = request.reducer_id
        arr = []
        print(
            f"Reducer {reducer_id} received {len(self.partitions)} partitions")
        for i, partition in enumerate(self.partitions):
            if i % self.R == reducer_id:
                # arr.extend(partition)
                # []
                for j in range(len(partition)):
                    arr.append(pb2.DataPoint(
                        centroid_id=partition[j][0], points=partition[j][1]))
        print(f"Mapper {self.mapper_id} sending {len(arr)} points")
        return pb2.ReceiveKeyValuesResponse(success=True, data_points=arr)

    def sendKeyValues(self, reducer_id):
        for i, partition in enumerate(self.partitions):
            if i % self.R == reducer_id:
                for point in partition:
                    yield pb2.KeyValue(key=point[0], value=point[1])

    def find_nearest_centroid(self, point, centroids):
        distances = [self.euclidean_distance(
            point, centroid) for centroid in centroids]
        nearest_centroid_index = distances.index(min(distances))
        return nearest_centroid_index

    def euclidean_distance(self, point1, point2):
        return sum([(a - b) ** 2 for a, b in zip(point1, point2)]) ** 0.5

    def write_output(self, mapped_points, output_file):
        # create directory if not exists
        if not os.path.exists(f'Mappers/M{self.mapper_id}'):
            os.makedirs(f'Mappers/M{self.mapper_id}')

        with open(output_file, 'w') as file:
            for point in mapped_points:
                file.write(f'{point[0]}\t{point[1]}\n')

    def Partition(self):
        for entry in self.mapper_points:
            self.partitions[entry[0] % self.R].append(entry)
        for i, partition in enumerate(self.partitions):

            self.write_output(
                partition, f'Mappers/M{self.mapper_id}/partition_{i%self.R}.txt')
        print(
            f"Mapper {self.mapper_id} partitioned {len(self.mapper_points)} points")


def serve(i,r):
    flag = random.randint(1,10)
    if flag <= r:
        sys.exit()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    pb2_grpc.add_KMeansMapReduceServicer_to_server(Map(), server)
    # Get all system args used when program is run
    # If there are more than 1 system args, then it means that the user has provided a port number
    port = f'[::]:400{i}'
    server.add_insecure_port(f'{port}')
    print(f"Mapper server started, listening on port {port}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
