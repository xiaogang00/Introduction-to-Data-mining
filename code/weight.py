# -*-coding: utf-8 -*-
import numpy as np


def Default_Vote(user, item, score, a, i):
    # 这个weight的计算，使用了default的一些假设数据，这样就可以在计算两个user的weight的时候使用所有的item的信息
    d = 3
    # d在这里就是default的值，所有的确实的user， item对的信息都是取这个值
    user_unique = np.unique(user)
    item_index_a = np.where(user == user_unique[a])
    item_index_a = item_index_a[0]
    item_index_i = np.where(user == user_unique[i])
    item_index_i = item_index_i[0]
    n = len(item_index_a) + len(item_index_i)
    item_a = []
    for i in range(len(item_index_a)):
        item_a.append(item[item_index_a[i]])
    item_i = []
    for i in range(len(item_index_i)):
        item_i.append(item[item_index_i[i]])
    used = []
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0
    count = 0
    for i in range(len(item_index_a)):
        used.append(item[item_index_a[i]])
        if item[item_index_a[i]] in item_i:
            for j in range(len(item_index_i)):
                if item[item_index_a[i]] == item[item_index_i[j]]:
                    sum1 += score[item_index_a[i]] * score[item_index_i[j]]
                    sum2 += score[item_index_a[i]]
                    sum3 += score[item_index_i[j]]
                    sum4 += pow(score[item_index_a[i]], 2)
                    sum5 += pow(score[item_index_i[j]], 2)
        else:
            sum1 += score[item_index_a[i]] * d
            sum2 += score[item_index_a[i]]
            sum3 += d
            sum4 += pow(score[item_index_a[i]], 2)
            sum5 += pow(d, 2)
            count = count + 1

    for i in range(len(item_index_i)):
        if item[item_index_i[i]] in used:
            continue
        else:
            used.append(item[item_index_i[i]])
        if item[item_index_i[i]] in item_a:
            for j in range(len(item_index_a)):
                if item[item_index_a[j]] == item[item_index_i[i]]:
                    sum1 += score[item_index_a[j]] * score[item_index_i[i]]
                    sum2 += score[item_index_a[j]]
                    sum3 += score[item_index_i[i]]
                    sum4 += pow(score[item_index_a[j]], 2)
                    sum5 += pow(score[item_index_i[i]], 2)
        else:
            sum1 += score[item_index_i[i]] * d
            sum2 += d
            sum3 += score[item_index_i[i]]
            sum4 += pow(d, 2)
            sum5 += pow(score[item_index_i[i]], 2)
            count = count + 1
    molecular = (n+count) * (sum1+count*d*d) - (sum2+count*d)*(sum3+count*d)
    denominator1 = ((n+count)*(sum4+count*d*d) - pow((sum2+count*d), 2))
    denominator2 = ((n + count) * (sum5 + count * d * d) - pow((sum3 + count * d), 2))
    denominator = np.sqrt(denominator1*denominator2)
    weight = molecular / denominator
    # 如果计算出来的weight不是一个数，说明两个user之间没有关系，所有为0
    if np.isnan(weight):
        weight = 0
    return weight


def compute_Correlation_weight(user, item, score, a, i, mean_v):
    # 这个函数是根据关联系数来计算weight
    user_unique = np.unique(user)
    item_index_a = np.where(user == user_unique[a])
    item_index_a = item_index_a[0]
    item_index_i = np.where(user == user_unique[i])
    item_index_i = item_index_i[0]
    v_a = mean_v[a]
    v_i = mean_v[i]
    molecular = 0
    denominator1 = 0
    denominator2 = 0
    # ssignificant weighting
    count = 0
    for i in range(len(item_index_a)):
        for j in range(len(item_index_i)):
            if item[item_index_a[i]] == item[item_index_i[j]]:
                count = count + 1
                molecular += (score[item_index_a[i]] - v_a) * (score[item_index_i[j]]-v_i)
                denominator1 += pow((score[item_index_a[i]] - v_a), 2)
                denominator2 += pow((score[item_index_i[j]] - v_i), 2)
    weight = molecular / np.sqrt(denominator1*denominator2)
    # 如果两者之间的重叠的item很少，说明两者之间的weight也应该小，所有进行significant weight
    if count < 50:
        weight = weight * count / 50
    #print weight
    # 如果计算出来的weight不是一个数，说明两个user之间没有关系，所有为0
    if np.isnan(weight):
        weight = 0
    return weight


def compute_vector_weight(user, item, score, a, i):
    # 在这里使用向量的相似性来作为weight
    user_unique = np.unique(user)
    item_index_a = np.where(user == user_unique[a])
    item_index_a = item_index_a[0]
    item_index_i = np.where(user == user_unique[i])
    item_index_i = item_index_i[0]
    molecular1 = 0
    molecular2 = 0
    denominator1 = 0
    denominator2 = 0
    for number1 in range(len(item_index_a)):
        denominator1 = denominator1 + pow(score[item_index_a[number1]], 2)
    denominator1 = np.sqrt(denominator1)

    for number2 in range(len(item_index_i)):
        denominator2 = denominator2 + pow(score[item_index_i[number2]], 2)
    denominator2 = np.sqrt(denominator2)
    weight = 0
    count = 0
    for i in range(len(item_index_a)):
        for j in range(len(item_index_i)):
            if item[item_index_a[i]] == item[item_index_i[j]]:
                count += 1
                molecular1 = score[item_index_a[i]]
                molecular2 = score[item_index_i[j]]
                weight = weight + (molecular1 /denominator1)*(molecular2 /denominator2)
    # 如果两者之间的重叠的item很少，说明两者之间的weight也应该小，所有进行significant weight
    if count < 50:
        weight = weight * count / 50
    # 如果计算出来的weight不是一个数，说明两个user之间没有关系，所有为0
    if np.isnan(weight):
        weight = 0
    return weight




