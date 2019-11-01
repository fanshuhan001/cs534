import numpy as np 
import pandas as pd 
import csv
import argparse

def relabel(tag):
    '''
    if an example labelled "3", then change it to be  "1"
    if it labelled "5", then change it to be "-1"
    '''
    return 1.0 if tag == 3 else -1.0

def load_data(filename, label=True):
    '''
    预处理数据，将标签（分类值）从训练集中分离，方便单独处理特征;
    将添加一组值为1.0的bias到特征中去;
    para.:
        x: features
        y: label
    return:
        x,y
    '''
    data = pd.read_csv(filename, header=None)
    if label:
        y = data[[0]]        
        #change label from 3/5 to 1/-1
        y = y.applymap(relabel)

        y = np.array(y)
        y = y.T[0]

        x = data.drop([0], axis = 1)
        #chage data type to np.array 
        x = np.array(x)
    else:
        y = None
        x = np.array(data)
    #insert bias to x
    x = np.insert(x, 0, values=1.0, axis=1)
    return x, y 

def predict(w, v_xs, v_y):
    correct = 0
    y_hat = []
    cases = len(v_xs)
    for i in range(cases):
        y_hat.append(np.sign(np.dot(w, v_xs[i])))
        if y_hat[i] == v_y[i]:
            correct += 1
    return correct/cases, y_hat

def online_perceptron(learn_x, learn_y, valid_x, valid_y, iters=15):
    '''
    使用online perceptron来预测，将每一次迭代后W的结果用于对valid数据集的
    预测，将结果与实际值进行比较，计算每次迭代的预测正确率
    para:
        learn_x:learning data:用于学习的features
        learn_y:用于学习的label
        valid_x:用于测试的数据集（特征集）
        valid_y:用于比较的实际结果
        inters:算法迭代次数
    return:
    w：最后得到的权重
    accuracies:一个list,代表地accuracies[i]表示第i次迭代后预测的准确率
    prediction:最后一次迭代预测出的结果
    '''
    accuracies = []
    prediction = []
    w = np.zeros(len(learn_x[0]))
    
    for iter in range(iters):
        for i in range(len(learn_x)):
            #w_t = w.reshape(w.shape[0], 1)
            y_hat = np.sign(np.dot(w, learn_x[i]))
            if y_hat * learn_y[i] <= 0:
                w += learn_y[i] * learn_x[i] 
        acc, prediction = predict(w, valid_x, valid_y)
        accuracies.append(acc)
        #predictions.append(pred)
    return w, accuracies, prediction



if __name__ == "__main__":
    t_features, t_label = load_data("pa2_train.csv")
    v_features, v_label = load_data("pa2_valid.csv")
    w, acc, pred = online_perceptron(t_features, t_label, v_features, v_label, 50)
    print(acc)
    
   # print(features[[1]], "\n------------------------------\n\n")
