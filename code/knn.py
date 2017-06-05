# -*-coding: utf-8 -*-
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os

def knn_method(data):
    X = []
    for i in range(len(data)):
        tempX = [data[i, 0], data[i, 1]]
        X.append(tempX)
    # neigh = KNeighborsClassifier(n_neighbors=100)
    neigh = NearestNeighbors(n_neighbors=80)
    neigh.fit(X)
    return neigh, X


def over_all(data, neigh, X):
    if not os.path.exists('./result'):
        os.makedirs('./result')
    file_object = open('./result/output3.txt', 'w')
    user = []
    for i in range(len(data)):
        user.append(data[i, 0])
    item = []
    for i in range(len(data)):
        item.append(data[i, 1])
    score = []
    for i in range(len(data)):
        score.append(data[i, 2])

    user_unique = np.unique(user)
    item_unique = np.unique(item)
    mean_v = np.zeros((len(user_unique), 1))
    var_v = np.zeros((len(user_unique), 1))
    for i in range(len(user_unique)):
        itemindex = np.where(user == user_unique[i])
        itemindex = itemindex[0]
        sum_vote = 0
        sum_vote2 = 0
        for k in range(len(itemindex)):
            sum_vote = sum_vote + score[itemindex[k]]
            sum_vote2 = sum_vote2 + pow(score[itemindex[k]], 2)
        mean_vote = sum_vote / len(itemindex)
        var_vote = sum_vote2 / len(itemindex) - mean_vote * mean_vote
        mean_v[i, 0] = mean_vote
        var_v[i, 0] = var_vote

    predict = np.zeros((int(max((user_unique))), int(max((item_unique)))))

    for a in range(int(max(user_unique))):
        for j in range(int(max(item_unique))):
            print a, j
            sum = 0
            count = 0
            v_a = mean_v[a, 0]
            temp = [[a+1, j+1]]
            temp_array = neigh.kneighbors(temp, return_distance=False)
            user_number = []
            for number in range(len(temp_array[0])):
                temp_index = temp_array[0][number]
                temp_neigh = X[temp_index]
                user_number.append(temp_neigh[0])
            user_number_unique = np.unique(user_number)

            for my_number in range(len(user_number_unique)):
                temp_index = np.where(user == user_number_unique[my_number])
                temp_index = temp_index[0]
                temp_data = 0
                for mm in range(len(temp_index)):
                    if item[temp_index[mm]] == j + 1:
                        temp_data = (score[temp_index[mm]] -
                                     mean_v[int(user_number_unique[my_number]-1), 0])\
                                    / np.sqrt(var_v[int(user_number_unique[my_number]-1), 0])
                sum = sum + temp_data
                count += 1
            if count == 0:
                data_k = 0
            else:
                data_k = 1.0 / count
            print (v_a + np.sqrt(var_v[a, 0]) * data_k * sum)
            predict[a, j] = round((v_a + np.sqrt(var_v[a, 0]) * data_k * sum))
            out = "%d  %d  %d  \n" % (a + 1, j + 1, round((v_a + np.sqrt(var_v[a, 0]) * data_k * sum)))
            file_object.write(out)
    return predict


if __name__ == '__main__':
    file = open('train_sub_txt.txt')
    lines = file.readlines()
    data = np.zeros((len(lines), 3))
    test = np.zeros((int(len(lines) / 2), 3))
    # 在这里设置训练集合和测试集
    row = 0
    row2 = 0
    count = 0
    for line in lines:
        line = line.strip().split(' ')
        for k in range(3):
            # data这里是我们需要的训练集合，最好是整个数据集
            data[row, k] = int(line[k])
        row += 1
        if count % 2 == 0:
            for k in range(3):
                test[row2, k] = int(line[k])
            row2 += 1
        count += 1
    neigh, X = knn_method(data)
    predict = over_all(data, neigh, X)

