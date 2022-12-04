from numpy import genfromtxt
import random
import math

random.seed(23)

def csv_to_list(path):
    my_data = genfromtxt(path, delimiter=',')
    return my_data.tolist()

def split_datasets(data):
    Train_set = []
    Val_set = []
    Test_set = []
    for i in range(len(data)):
        R = random.uniform(0.0,1.0)
        if(R>=0 and R<=0.7):
            Train_set.append(data[i])
        elif(R>0.7 and R<=0.85):
            Val_set.append(data[i])
        else:
            Test_set.append(data[i])
    return Train_set, Val_set, Test_set

def euclidean(V, T):
    total = 0
    size = len(V) - 2   # major won't be get included
    for i in range(size):
        total += ((V[i] - T[i])**2)
    return math.sqrt(total)

def knn_classification(K, train, val):
    validated_sample = 0

    # find distance
    for V in val:
        L = []
        for T in train:
            d = euclidean(V, T)
            L.append([T,d])

        # sort asc distance
        L.sort(key=lambda x: x[1])

        # Separating first K sample data
        A = []  # only contains major
        for i in range(K):
            A.append(int(L[i][0][-1]))  # L[i][0] == T &  L[i][1] == distance

        # finding major
        major = max(A, key=A.count)

        # Checking
        if(V[-1]==major):
            validated_sample+=1
    cvAccuracy = (validated_sample/len(val))*100;

    # output
    return cvAccuracy

def main():
    # KNN Classification
    # load data
    K = [1, 3, 5, 10, 15]
    accuracy = []
    data = csv_to_list('iris.csv')
    train, test, val = split_datasets(data)

    # validations
    for k in K:
        accuracy.append((k, knn_classification(k, train, val)))

    # print all accuracy
    for a in accuracy:
        print('K =', a[0], '\tAccuracy =', a[1])

    # sort accuracy desc with value
    accuracy.sort(key=lambda x: x[1], reverse=True)

    # best K
    bestK = accuracy[0][0]
    test_accuracy = knn_classification(bestK, train, test)

    print("\nBest K: ", bestK, "\tTest Accuracy: ", test_accuracy)

main()