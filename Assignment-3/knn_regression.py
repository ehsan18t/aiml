from numpy import genfromtxt
import random
import math

random.seed(34)

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
    size = len(V) - 2   # last won't be get included
    for i in range(size):
        total += ((V[i] - T[i])**2)
    return math.sqrt(total)

def knn_regression(K, train, val):
    Error = 0

    for V in val:
        L = []
        for T in train:
            d = euclidean(V, T)
            L.append([T,d])

        # sort asc distance
        L.sort(key=lambda x: x[1])

        # Separating first K sample data
        A = []
        for i in range(K):
            A.append(L[i])

        # avg calculation
        Avg = 0
        for i in range(K):
            Avg+=A[i][0][-1]
        Avg/=K

        # calculate sum of error
        Error+=(V[-1] - Avg)**2

    return Error / len(val)

def main():
    # KNN Regression
    # load data
    K = [1, 3, 5, 10, 15]
    error = []
    data = csv_to_list('diabetes.csv')
    train, test, val = split_datasets(data)

    # validations
    for k in K:
        error.append((k, knn_regression(k, train, val)))

    # print all accuracy
    for e in error:
        print('K =', e[0], '\tMean Squared Error =', e[1])

    # sort accuracy asc with value
    error.sort(key=lambda x: x[1])

    # best K (lowest error)
    bestK = error[0][0]
    mean_squared_error = knn_regression(bestK, train, test)

    print("\nBest K: ", bestK, "\tMean Squared Error: ", mean_squared_error)

main()