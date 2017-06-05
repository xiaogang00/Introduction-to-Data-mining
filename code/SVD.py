# -*-coding: utf-8 -*-
import numpy as np
import os

def svd(mat, feature, steps=1500, gama=0.02, lamda=0.1):
    slowRate = 0.99
    preRmse = 1000000000.0
    nowRmse = 0.0

    user_feature = np.matrix(np.random.rand(mat.shape[0], feature))
    item_feature = np.matrix(np.random.rand(mat.shape[1], feature))

    for step in range(steps):
        rmse = 0.0
        n = 0
        for u in range(mat.shape[0]):
            for i in range(mat.shape[1]):
                if mat[u, i] != 0:
                    pui = float(np.dot(user_feature[u, :], item_feature[i, :].T))
                    eui = mat[u, i] - pui
                    rmse += pow(eui, 2)
                    n += 1
                    for k in range(feature):
                        user_feature[u, k] += gama * (eui * item_feature[i, k] - lamda * user_feature[u, k])
                        item_feature[i, k] += gama * (eui * user_feature[u, k] - lamda * item_feature[i, k])

        nowRmse = np.sqrt(rmse * 1.0 / n)
        print 'step: %d      Rmse: %s' % ((step + 1), nowRmse)
        if (nowRmse < preRmse):
            preRmse = nowRmse
        else:
            break
        gama *= slowRate
        step += 1

    return user_feature, item_feature


def evaluate(user_feature, item_feature, test):
    test_user = []
    test_item = []
    for i in range(len(data)):
        test_user.append(data[i, 0])
        test_item.append(data[i, 1])
    user_unique = np.unique(user)
    item_unique = np.unique(item)
    result = np.zeros((len(test), 2))
    correct = 0
    wrong = 0
    for i in range(len(test)):
        pui = round(np.dot(user_feature[int(test[i, 0]-1), :], item_feature[int(test[i, 1]-1), :].T))
        result[i, 0] = pui
        result[i, 1] = int(test[i, 2])
        print pui, int(test[i, 2])
        if pui == int(test[i, 2]):
            correct += 1
        else:
            wrong += 1
    acc = correct / (correct + wrong)
    return acc


def over_all(user, item, user_feature, item_feature):
    if not os.path.exists('./result'):
        os.makedirs('./result')
    file_object = open('./result/output2.txt', 'w')
    user_unique = np.unique(user)
    item_unique = np.unique(item)
    result = []
    for i in range(int(max(user_unique))):
        for j in range(int(max(item_unique))):
            pui = round(np.dot(user_feature[i, :], item_feature[j, :].T))
            if pui >= 5:
                pui = 5
            out = "%d  %d  %d  \n" % (i+1, j+1, pui)
            result.append(pui)
            file_object.write(out)
    return result


if __name__ == '__main__':
    file = open('train_sub_txt.txt')
    lines = file.readlines()
    data = np.zeros((len(lines), 3))
    test = np.zeros((int(len(lines)/2), 3))
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

    user = []
    item = []
    for i in range(len(data)):
        user.append(data[i, 0])
        item.append(data[i, 1])
    user_unique = np.unique(user)
    item_unique = np.unique(item)
    data_matrix = np.zeros((int(max(user_unique)), int(max(item_unique))))
    for i in range(len(data)):
        data_matrix[int(data[i, 0]-1), int(data[i, 1]-1)] = data[i, 2]
    print data_matrix
    user_feature, item_feature = svd(data_matrix, 100, steps=1500, gama=0.02, lamda=0.1)
    print user_feature
    print item_feature
    #acc = evaluate(user_feature, item_feature, test)
    over_all(user, item, user_feature, item_feature)
