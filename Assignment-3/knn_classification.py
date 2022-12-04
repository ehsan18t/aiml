from numpy import genfromtxt
import random
import math

def csv_to_list(path):
    my_data = genfromtxt(path, delimiter=',')
    return my_data.tolist()

def split_datasets(data):
    Train_set = []
    Val_set = []
    Test_set = []
    # random.seed(0)
    for i in range(len(data)):
        R = random.uniform(0.0,1.0)
        if(R>=0 and R<=0.7):
            Train_set.append(data[i])
        elif(R>0.7 and R<=0.85):
            Val_set.append(data[i])
        else:
            Test_set.append(data[i])
    return Train_set, Val_set, Test_set

def knn_classification(K, train, val):
    L = []

    # find distance
    for V in val :
        for T in train:
            d = math.sqrt(((V[0]-T[0])**2)+((V[1]-T[1])**2)+((V[2]-T[2])**2)+((V[3]-T[3])**2));
            L.append([T,d])

    # sort asc distance
    L.sort(key=lambda x: x[1])

    # Separating first K sample data
    A = []
    for i in range(K):
        A.append(int(L[i][0][4]))
    
    # majority class from the K samples
    E0 = E1 = E2 = 0
    major = 0

    for i in range(K):
        if(A[i]== 0):
            E0+=1
        elif A[i]== 1:
            E1+=1
        else:
            E2+=1

    if E0>=E1 and E0>=E2:
        major = 0
    elif E1>=E0 and E1>=E2:
        major = 1
    else:
        major = 2

    # Checking
    currentCount = 0

    for V in val:
        if(V[4]==major):
            currentCount+=1
    totalCount = len(val)
    cvAccuracy = (currentCount/totalCount) *100;

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