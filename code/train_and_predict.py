# -*-coding: utf-8 -*-
import numpy as np
import os
from collaborative import *

def experiment(train_data, test_data):
    if not os.path.exists('./result'):
        os.makedirs('./result')
    file_object = open('./result/output.txt', 'w')
    # 在这里载入训练的数据
    user = []
    for i in range(len(train_data)):
        user.append(train_data[i, 0])
    item = []
    for i in range(len(train_data)):
        item.append(train_data[i, 1])

    score = []
    for i in range(len(train_data)):
        score.append(train_data[i, 2])

    # 统计不同的user的数字label
    user_unique = np.unique(user)
    mean_v = np.zeros((len(user_unique), 1))
    var_v = np.zeros((len(user_unique), 1))
    # 在这里计算平均值和方差，注意需要有所有的user，不能有被遗漏的user在矩阵中
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

    # 在这里读取测试数据，统计user,item,score
    test_user = []
    for i in range(len(test_data)):
        test_user.append(test_data[i, 0])
    test_item = []
    for i in range(len(test_data)):
        test_item.append(test_data[i, 1])
    test_score = []
    for i in range(len(test_data)):
        test_score.append(test_data[i, 2])
    result = np.zeros((len(test_user), 2))

    # 对于每一个test中的对，user和item来预测他们的值，并且将真正的label也保存下来
    for i in range(len(test_user)):
        result[i] = [predict(int(test_user[i]-1), int(test_item[i]-1),
                             user, item, score, mean_v, var_v), test_score[i]]
        print result[i]
    return result


def predict(user_no, item_no, user, item, score, mean_v, var_v):
    v_a = mean_v[user_no, 0]
    sum = 0
    sumk = 0
    user_unique = np.unique(user)
    item_unique = np.unique(item)
    for k in range(len(user_unique)):
        # 计算和其他的user之间的weight
        if user_unique[k] == user_unique[user_no]:
            continue
        temp_weight = compute_Correlation_weight(user, item, score, user_no, k, mean_v)
        # temp_weight = compute_vector_weight(user, item, score, a, k)
        # temp_weight = Default_Vote(user, item, score, a, k)
        print temp_weight
        temp_index = np.where(user == user_unique[k])
        temp_index = temp_index[0]
        temp_data = 0
        # 在这里如果weight太低，说明两者之间的相关性太低，所以忽略
        if abs(temp_weight) < 0.3:
            continue
        # 在这里计算最后的weight，要进行归一化，用其均值和标准差进行归一化
        for number in range(len(temp_index)):
            if item[temp_index[number]] == item_unique[item_no]:
                temp_data = (score[temp_index[number]] - mean_v[k, 0]) / np.sqrt(var_v[k, 0])
        sum = sum + temp_weight * temp_data
        # sumk是用来归一化weight使得其符合我们最后的分数的范围
        sumk = sumk + abs(temp_weight)
    if sumk == 0:
        data_k = 0
    else:
        data_k = 1.0 / sumk
    print (v_a + np.sqrt(var_v[user_no, 0]) * data_k * sum)
    # 在这里按照公式进行四舍五入，作为最后预测的分数
    predict = round((v_a + np.sqrt(var_v[user_no, 0]) * data_k * sum))
    return predict