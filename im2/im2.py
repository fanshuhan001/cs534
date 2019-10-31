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
    '''
    data = pd.read_csv(filename, header=None)
    if label:
        y = data[[0]]        
        #change label from 3/5 to 1/-1
        y = y.applymap(relabel)
        x = data.drop([0], axis = 1)

        #chage data type to np.array 
        x = np.array(x)
        y = np.array(y)

    #insert bias to x
        x = np.insert(x, 0, values=1.0, axis=1)

        y = y.T[0]
    else:
        y = None
        x = np.array(data)
        x = np.insert(x, 0, values=1.0, axis=1)
    
    return x, y 

if __name__ == "__main__":
    load_data("pa2_train.csv")
    #print(features)
