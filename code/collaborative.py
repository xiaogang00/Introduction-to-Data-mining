# -*-coding: utf-8 -*-
import numpy as np
import os
from weight import *
from train_and_predict import *


def overall_predict(data):
    # 这个函数把所有的训练数据输入，并且输出所有的，我们将要进行的user, item对的预测
    # 进行结果保存
    if not os.path.exists('./result'):
        os.makedirs('./result')
    file_object = open('./result/output.txt', 'w')
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
            v_a = mean_v[a, 0]
            sum = 0
            sumk = 0
            # 对于缺失的item，即没有人曾经关联过的item，用平均值
            for k in range(int(max(user_unique))):
                if not (j + 1 in item_unique):
                    continue

                if user_unique[k] == user_unique[a]:
                    continue
                #temp_weight = compute_Correlation_weight(user, item, score, a, k, mean_v)
                #temp_weight = compute_vector_weight(user, item, score, a, k)
                temp_weight = Default_Vote(user, item, score, a, k)
                temp_index = np.where(user == user_unique[k])
                temp_index = temp_index[0]
                temp_data = 0
                if abs(temp_weight) < 0.3:
                    continue
                for number in range(len(temp_index)):
                    if item[temp_index[number]] == j + 1:
                        temp_data = (score[temp_index[number]] - mean_v[k, 0]) / np.sqrt(var_v[k, 0])
                sum = sum + temp_weight * temp_data
                sumk = sumk + abs(temp_weight)
            if sumk == 0:
                data_k = 0
            else:
                data_k = 1.0 / sumk
            print (v_a + np.sqrt(var_v[a, 0]) * data_k * sum)
            predict[a, j] = round((v_a + np.sqrt(var_v[a, 0]) * data_k * sum))
            # 预测出的结果的值
            out = "%d  %d  %d  \n" % (a+1, j+1, predict[a, j])
            file_object.write(out)
    return predict


def evaluate(result):
    # 这个返回的result的形式为[score, label]，score是我们预测出来的，label是ground truth
    correct = 0
    wrong = 0
    # 正确率与错误率
    for number in range(len(result)):
        if result[number][0] == result[number][1]:
            correct = correct + 1
        else:
            wrong = wrong + 1
    acc = correct / (correct + wrong)
    return acc


if __name__ == '__main__':
    file = open('train_sub_txt.txt')
    lines = file.readlines()
    data = np.zeros((len(lines), 3))
    #test_data = np.zeros((len(lines)/2, 3))
    row = 0
    #row2 = 0
    count = 0
    # 在这里设置训练集合和测试集
    for line in lines:
        line = line.strip().split(' ')
        if True:
            for k in range(3):
                # data这里是我们需要的训练集合，最好是整个数据集
                data[row, k] = int(line[k])
            row += 1
        #if count % 2 == 0:
        #    for k in range(3):
        #        test_data[row2, k] = int(line[k])
                # test_data在这里是测试的集合
        #    row2 += 1
        count += 1
    predict = overall_predict(data)
    # print predict
    # 进行训练和预测
    #result = experiment(data, test_data)
    # 计算准确率
    #acc = evaluate(result)
    #print acc
