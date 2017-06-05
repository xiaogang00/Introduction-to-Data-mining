import numpy as np

def acc(data, test):
    count = 0
    correct = 0
    wrong = 0
    number = 0
    for i in range(len(data)):
        for j in range(count, len(test), 1):
            count += 1
            if (test[j, 0] == data[i, 0]) and (test[j, 1] == data[i, 1]):
                number += 1
                if test[j, 2] == data[i, 2]:
                    correct += 1
                else:
                    wrong += 1
                break
    print correct, wrong, len(data), number
    acc = correct * 1.0 / (correct + wrong)
    print acc


if __name__ == '__main__':
    file = open('train_sub_txt.txt')
    lines = file.readlines()
    data = np.zeros((len(lines), 3))
    row = 0
    for line in lines:
        line = line.strip().split(' ')
        if True:
            for k in range(3):
                data[row, k] = int(line[k])
            row += 1

    file = open('output2.txt')
    lines = file.readlines()
    test = np.zeros((len(lines), 3))
    row = 0
    count = 0
    for line in lines:
        line = line.strip().split('  ')
        if True:
            for k in range(3):
                test[row, k] = int(line[k])
            row += 1
            count += 1

    acc(data, test)
