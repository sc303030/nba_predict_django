
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
import datetime

import matplotlib

matplotlib.rcParams['axes.unicode_minus'] = False

import platform
import seaborn as sns

import warnings

warnings.filterwarnings('ignore')

from matplotlib import font_manager, rc
from matplotlib import style
import math
import re

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import layers

import pandas as pd
import numpy as np
import seaborn as sns

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print(',', end='')

class Tensorflow_df:
    def __init__(self, train, test, dense_cnt, name):
        self.train_set = train
        self.test_set = test
        self.dense_cnt = dense_cnt
        self.name = name
        self._sample_result = ''
        self.train_df()
        self.y_df()
        self.norm_df()
        self.model_learn()
        self.mse_print()

    def train_df(self):
        self.train_state = self.train_set.describe()
        self.train_state.pop('age')
        self.train_state = self.train_state.T

    def y_df(self):
        self.y_train = self.train_set.pop('age')
        self.y_test = self.test_set.pop('age')

    @staticmethod
    def norm(x, train_state):
        return (x - train_state['mean']) / train_state['std']

    def norm_df(self):
        self.norm_train_set = self.norm(self.train_set, self.train_state)
        self.norm_test_set = self.norm(self.test_set, self.train_state)

    def model_learn(self):
        self.model = keras.Sequential([
            layers.Dense(self.dense_cnt, activation=self.name, input_shape=[1]),
            layers.Dense(self.dense_cnt, activation=self.name),
            layers.Dense(1)
        ])

        optimizer = tf.keras.optimizers.RMSprop()
        self.model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
        self.model.build( input_shape=[1])
        self.model.summary()

        self._sample_result = self.model.predict(self.norm_train_set)

        self.history = self.model.fit(self.norm_train_set, self.y_train, epochs=1000, validation_split=.2, verbose=0,
                                      callbacks=[PrintDot()])

    def mse_print(self):
        loss, mae, mse = self.model.evaluate(self.norm_test_set, self.y_test, verbose=1)
        print('평균 절대 오차 : ', mae)

    def plt_show(self):
        # 시각화
        self.y_pred = self.model.predict(self.norm_test_set).flatten()
        plt.scatter(self.y_test, self.y_pred)
        plt.xlim([0, plt.xlim()[1]])
        plt.ylim([0, plt.ylim()[1]])
        plt.scatter(self.y_test, self.y_pred)
        _ = plt.plot([-100, 100], [-100, 100])
        plt.show()

    def history_df(self):
        self.hist = pd.DataFrame(self.history.history)
        return self.hist

    @property
    def get_result(self):
        return self._sample_result
