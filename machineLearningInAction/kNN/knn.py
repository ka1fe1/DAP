# -*- coding: utf-8 -*-

from numpy import *
import operator
"""
KNN：k-近邻算法
"""


def create_data_set():
    group = [
        [1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]
    ]
    labels = ['A', 'A', 'B', 'B']
    return mat(group), labels

if __name__ == '__main__':
    group, labels = create_data_set()
    print(group)
    print(mat(group))
