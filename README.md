# Distributed Shopping Platform

This project implements a distributed shopping platform with a central market server and client applications for buyers and sellers, deployed on Google Cloud. The platform allows sellers to manage their products and buyers to search for and purchase items, all while maintaining secure and reliable communication between the different components.

## Components

1. **Market Server (Central Platform)**
2. **Seller Client**
3. **Buyer Client**

### 1. Market Server

The Market Server handles all communications and transactions. It listens for requests from sellers and buyers and processes them accordingly.

### 2. Seller Client

The Seller Client interacts with the Market Server to:

- Register as a seller
- Add new items for sale
- Update existing items
- Delete items
- View all items listed by the seller

### 3. Buyer Client

The Buyer Client interacts with the Market Server to:

- Search for items
- Buy items
- Add items to a wishlist
- Rate items

## Setup

### Prerequisites

- Python 3.6+
- `grpcio` and `grpcio-tools` packages
- Google Cloud account for deploying virtual machines

# A2. Raft Consensus Algorithm with Leader Lease

## Overview
This project implements a distributed key-value store using the Raft consensus algorithm with leader lease modification. The system ensures data consistency, fault tolerance, and leader election in a cluster of nodes hosted on Google Cloud VMs, communicating via gRPC.

## Features
- **Leader Election:** Nodes participate in elections to choose a leader.
- **Log Replication:** Leader replicates log entries to follower nodes.
- **Fault Tolerance:** System continues to operate correctly even if some nodes fail.
- **Leader Lease:** If leader fails or gets network partitioned, the remaining nodes wait for the original leader to step down to avoid having multiple leaders.
- **Data Persistence:** Logs and metadata are stored in human-readable formats for persistence and recovery.
- **Client Interaction:** Supports SET and GET operations, handling leader identification and failure.

## Technologies Used
- **Python**
- **gRPC** for inter-node and client-node communication
- **Google Cloud Platform (GCP)** for hosting virtual machines

## Setup and Installation

### Prerequisites
- Python 3.6 or later
- gRPC and Protocol Buffers
- Google Cloud Platform account
- 
### Running the Nodes
1. Start the Raft nodes on separate Google Cloud VMs.
2. Each node should be started with a unique node ID and a list of all node IDs in the cluster.


# A3. Distributed K-Means Clustering Using MapReduce Framework

## Project Description

This project implements a distributed K-Means clustering algorithm using a custom MapReduce framework. The framework is deployed on a single machine, with each component (master, mappers, reducers) running as separate processes. Communication between the processes is handled using gRPC.

## Components

### Master Node

The master node is responsible for:
- Managing the execution of mappers and reducers.
- Splitting the input data into chunks for mappers.
- Sending necessary parameters to mappers and reducers.
- Compiling the final list of centroids after each iteration.

### Mapper

Each mapper:
- Reads an input data chunk.
- Assigns each data point to the nearest centroid.
- Outputs intermediate key-value pairs (centroid index, data point).

### Reducer

Each reducer:
- Receives intermediate key-value pairs from mappers.
- Shuffles and sorts the key-value pairs.
- Updates centroids based on grouped key-value pairs.
- Outputs the updated centroids.
