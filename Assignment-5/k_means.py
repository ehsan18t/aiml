import sys
from numpy import genfromtxt
import random
import math
import matplotlib.pyplot as plt

random.seed(11201122)

def csv_to_list(path):
    my_data = genfromtxt(path, delimiter=',')
    return my_data.tolist()

def find_random_centers(data, k):
    temp_centers = set()
    total_data = len(data)
    centers = []

    # finding random center
    for i in data:
        d = random.randint(0,total_data-1)
        temp_centers.add((data[d][0], data[d][1]))
        if(len(temp_centers)==k):
            break

    # adding center to center list
    for i in range(k):
        centers.append(temp_centers.pop())

    return centers

def init_clusters(k):
    clusters = []
    for i in range(k):
        clusters.append([])
    return clusters

def euclidean_distance(p1, p2):
    # p2 given values, p1 calculated centers
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

def assign_cluster(data, center):
    clusters = init_clusters(len(center))
    for i in range(len(data)):
        min_dist = sys.maxsize
        min_index = 0
        for j in range(len(center)):
            dist = euclidean_distance(center[j], data[i])
            if dist < min_dist:
                min_dist = dist
                min_index = j
        clusters[min_index].append(i)
    return clusters

# for each cluster
def find_mean_center(data, cluster):
    sum_x = 0
    sum_y = 0
    for i in cluster:
        sum_x += data[i][0]
        sum_y += data[i][1]
    return [sum_x/len(cluster), sum_y/len(cluster)]

# for all clusters
def find_new_centers(data, clusters):
    new_centers = []
    for cluster in clusters:
        new_centers.append(find_mean_center(data, cluster))
    return new_centers

def is_centers_changed(old_centers, new_centers):
    for i in range(len(old_centers)):
        if old_centers[i] != new_centers[i]:
            return True
    return False

def k_means_clustering(data, k):
    centers = find_random_centers(data, k)
    clusters = assign_cluster(data, centers)
    new_centers = find_new_centers(data, clusters)
    while is_centers_changed(centers, new_centers):
        centers = new_centers
        clusters = assign_cluster(data, centers)
        new_centers = find_new_centers(data, clusters)
    return clusters

def plot_clusters(data, clusters):
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
    for i in range(len(clusters)):
        cluster = clusters[i]
        color = colors[i % len(colors)]
        for j in cluster:
            plt.scatter(data[j][0], data[j][1], c=color)
    plt.show()

def main():
    data_path = 'g_data.csv'
    data = csv_to_list(data_path)
    k = 4
    clusters = k_means_clustering(data, k)
    plot_clusters(data, clusters)
main()