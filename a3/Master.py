import os
import sys
import multiprocessing
import Map
import Reduce
import mapreduce_pb2 as pb2
import mapreduce_pb2_grpc as pb2_grpc
import grpc
import random
import time

Mappers_dict = {}
Reducers_dict = {}
num_mappers = 0
num_reducers = 0
num_iterations = 0


def start_processes(file):
    # Start all mapper processes
    for i in range(num_mappers):
        r = 2
        p = multiprocessing.Process(target=Map.serve, args=(i, r))
        p.start()
        time.sleep(0.5)
        if p.exitcode is None:
            print("Process is still running")
        else:
            print(f"Process{i} has terminated")
            file.write(f"Process{i} has terminated\n")
            p = multiprocessing.Process(target=Map.serve, args=(i, -1))
            p.start()
        Mappers_dict[i] = p

    # Start all reducer processes
    for i in range(num_reducers):
        r = 2
        p = multiprocessing.Process(target=Reduce.run, args=(i, r))
        p.start()
        time.sleep(0.5)
        if p.exitcode is None:
            print("Process is still running")
        else:
            print(f"Process{i} has terminated")
            p = multiprocessing.Process(target=Reduce.run, args=(i, -1))
            p.start()
        Reducers_dict[i] = p


def run_iterations():
    global CENTROIDS
    with open("dump.txt", "a") as file:
        for iteration in range(num_iterations):
            start_processes(file)
            print(f"Starting Iteration {iteration + 1}")
            file.write(f"Iteration {iteration + 1}:\n")

            print("Starting map tasks...")
            file.write("Starting map tasks...\n")
            call_mappers(CENTROIDS, file)

            print("Starting reduce tasks...")
            file.write("Starting reduce tasks...\n")
            UPDATED_CENTROIDS = call_reducers(CENTROIDS, file)
            # Converting the updated centroids to a list of tuples
            UPDATED_CENTROIDS = [tuple(centroid.coordinates)
                                 for centroid in UPDATED_CENTROIDS]

            print(f"Updated_centroids: {UPDATED_CENTROIDS}")
            file.write(f"Updated centroids: {UPDATED_CENTROIDS}\n")

            # Save the latest centroids to a file
            save_centroids(UPDATED_CENTROIDS)

            if check_convergence(CENTROIDS, UPDATED_CENTROIDS):
                # Should be the iteration before this one
                print("Convergence reached in iteration", iteration,
                      " As the centroids are the same in this iteration", iteration)
                file.write(f"Convergence reached in iteration {iteration}\n")
                for i in range(num_mappers):
                    Mappers_dict[i].terminate()
                for i in range(num_reducers):
                    Reducers_dict[i].terminate()
                break
            else:
                CENTROIDS = UPDATED_CENTROIDS

            # Terminate all the processes
            for i in range(num_mappers):
                Mappers_dict[i].terminate()
            for i in range(num_reducers):
                Reducers_dict[i].terminate()


def call_mappers(centroids, file):
    indices_per_mapper = len(data_points) // num_mappers
    remainder = len(data_points) % num_mappers
    for i in range(num_mappers):
        start_index = i * indices_per_mapper
        end_index = start_index + indices_per_mapper
        if i == num_mappers - 1:
            end_index += remainder
        centroid_objects = [pb2.Centroid(
            coordinates=centroid) for centroid in centroids]
        request = pb2.MapTaskRequest(
            mapper_id=i,
            num_mappers=num_mappers,
            num_reducers=num_reducers,
            num_iterations=num_iterations,
            input_file_path=input_file_path,
            start_index=start_index,
            end_index=end_index,
            centroids=centroid_objects
        )
        call_mapper(request, file)


def call_mapper(request, file):
    map_id = request.mapper_id

    with grpc.insecure_channel(f'localhost:400{map_id}') as channel:
        stub = pb2_grpc.KMeansMapReduceStub(channel)
        response = stub.MapTask(request)
        print(response.message)

        file.write(f"Mapper {map_id} response: {response.message}\n")


def call_reducers(centroids, file):
    final_reduce_output = []
    for i in range(num_reducers):
        centroid_objects = [pb2.Centroid(
            coordinates=centroid) for centroid in centroids]
        request = pb2.ReduceTaskRequest(
            reducer_id=i,
            num_mappers=num_mappers,
            num_reducers=num_reducers,
            centroids=centroid_objects
        )
        final_reduce_output.extend(call_reducer(request, file))
    return final_reduce_output


def call_reducer(request, file):
    reduce_id = request.reducer_id
    with grpc.insecure_channel(f'localhost:500{reduce_id}') as channel:
        stub = pb2_grpc.KMeansMapReduceStub(channel)
        response = stub.ReduceTask(request)
        print(response.message)
        file.write(f"Reducer {reduce_id} response: {response.message}\n")
        final_centroids = response.centroids
    return final_centroids


def save_centroids(centroids):
    with open("centroids.txt", 'w') as file:
        for centroid in centroids:
            file.write(','.join(map(str, centroid)) + '\n')


def check_convergence(centroids, final_centroids):
    # We have to compare whether all points in the two lists are equal, irrespective of their order
    return sorted(centroids) == sorted(final_centroids)


def load_centroids(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                centroids = [tuple(map(float, line.strip().split()))
                             for line in file.readlines()]
            except ValueError:
                try:
                    centroids = [tuple(map(float, line.strip().split(',')))
                                 for line in file.readlines()]
                except ValueError:
                    print("Invalid file format")
                    return None
        return centroids
    return None


if __name__ == "__main__":
    # Set up the necessary variables and parameters
    # num_mappers = 2
    # num_reducers = 2
    # num_iterations = 10
    # num_centroids = 3
    num_mappers = int(input("Enter the number of mappers: "))
    num_reducers = int(input("Enter the number of reducers: "))
    num_iterations = int(input("Enter the number of iterations: "))
    num_centroids = int(input("Enter the number of centroids: "))

    input_file_path = "E:\dscd\Assignment-3 FINAL\Assignment-3\points.txt"

    # Start all the required processes
    # start_processes()
    # sleep for a while to allow all the servers to start
    time.sleep(2)
    data_points = []
    with open(input_file_path, 'r') as file:
        data_points = [tuple(map(float, line.strip().split(',')))
                       for line in file.readlines()]
    # Load the initial centroids or generate them randomly
    # CENTROIDS = load_centroids("centroids.txt")
    # if not CENTROIDS:
    CENTROIDS = random.sample(data_points, num_centroids)
    CENTROIDS = sorted(CENTROIDS, key=lambda x: x[0])
    with open("dump.txt", "a") as file:
        file.write(f"Initial centroids: {CENTROIDS}\n")

    # Run the iterations
    run_iterations()
