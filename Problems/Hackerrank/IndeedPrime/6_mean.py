#!/usr/bin/python

#######################################################################
# Author: Andrés Herrera Poyatos
# Universidad de Granada, June, 2015
# Indeed Prime Challengue
# Problem 6
########################################################################

import numpy
import math
from sklearn import ensemble

#-------------------------------- FUNCTIONS --------------------------------#

def preprocessing(new_line):
    instance = [None] * 6
    first_split = new_line.split()
    first_part_split = first_split[0].split("-")
    second_part_split = first_split[2].split("-")
    instance[0] = int(first_part_split[0])
    instance[1] = int(first_part_split[1])
    instance[2] = int(first_part_split[2])
    instance[3] = int(second_part_split[0])
    instance[4] = int(second_part_split[1])
    instance[5] = int(second_part_split[2])
    return instance, int(first_split[3]) if len(first_split[3].split("_")) == 1 else None

ROWS = 595
TEST_ROWS = 50
TRAIN_ROWS = ROWS - TEST_ROWS

###############################################################################

# Load data
x = []; y = []
for i in range(0, ROWS):
    instance, value = preprocessing(input())
    x.append(instance)
    y.append(value)


x_train, y_train = x[:TRAIN_ROWS], y[:TRAIN_ROWS]
x_test, y_test = x[TRAIN_ROWS:], y[TRAIN_ROWS:]

###############################################################################

y = []
for i in range(0, len(x_test)):
    count = 0
    value = 0
    for j in range(300, TRAIN_ROWS):
        if x_train[1] == x_test[1]:
            count += 1
            value += y_train[i]
    y.append(value / count)

for p in y:
    print(math.trunc(p))