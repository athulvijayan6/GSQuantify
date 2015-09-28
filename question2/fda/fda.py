#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-28 13:25:18
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 13:26:32
from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.lda import LDA
import scipy.stats
plt.style.use('ggplot')

trainData = np.load('../data/Initial_Training_Data.npy')
np.random.shuffle(trainData)
testData = np.load('../data/Initial_Test_Data.npy')
truth = trainData[:, 19].astype(int)
numClasses = max(truth) - min(truth) + 1

# Remove NaNs
for cls in xrange(numClasses):
    classData = trainData[truth==cls, :]
    col_mean = scipy.stats.mode(classData, axis=0)
    ids = np.where(np.isnan(classData))
    classData[ids] = np.take(col_mean, ids[1])
    trainData[truth==cls, :] = classData

col_mean = scipy.stats.mode(trainData, axis=0)
ids = np.where(np.isnan(testData))
testData[ids] = np.take(col_mean, ids[1])

trainFeatures = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
testFeatures = testData[:, 1:]

# =========================== FDA model =======================
model = LDA()
model.fit(trainFeatures, truth)

scores = model.predict_proba(testFeatures)
targetScores = np.amax(scores, axis = 1)
targetClass = np.argmax(scores, axis = 1)

outFile = 'output.csv'
with open(outFile, 'w') as f:
    f.write('ISIN, Risk_Stripe\n')
    for i in xrange(testData.shape[0]):
        line = 'ISIN{0},Stripe {1}\n'
        line = line.format(int(testData[i, 0]), int(targetClass[i]))
        f.write(line)
f.close()
