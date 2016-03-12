import numpy as np
import os

from sklearn.cross_validation import (cross_val_score, StratifiedKFold)
from sklearn.pipeline import make_pipeline
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegressionCV

from my_settings import *

os.chdir(tf_folder)


ent_left_lh = []
ent_left_rh = []
ctl_left_lh = []
ctl_left_rh = []

ent_right_lh = []
ent_right_rh = []
ctl_right_lh = []
ctl_right_rh = []

data_name = glob("00*MNE-tfr.npy")
data_name.sort()

for d in data_name:
    if d[5:10] == "ent_l":
        if d[26:28] == "lh":
            tmp = np.load(d)
            ent_left_lh.append(tmp)
        else: # d[27:29] == "rh":
            tmp = np.load(d)
            ent_left_rh.append(tmp)
    elif d[5:10] == "ent_r":
        if d[27:29] == "lh":
            tmp = np.load(d)
            ent_right_lh.append(tmp)
        else:  # elif d[27:29] == "rh":
            tmp = np.load(d)
            ent_right_rh.append(tmp)
    elif d[5:10] == "ctl_l":
        if d[26:28] == "lh":
            tmp = np.load(d)
            ctl_left_lh.append(tmp)
        else:  # elif d[27:29] == "rh":
            tmp = np.load(d)
            ctl_left_rh.append(tmp)
    elif d[5:10] == "ctl_r":
        if d[27:29] == "lh":
            tmp = np.load(d)
            ctl_right_lh.append(tmp)
        else:  # elif d[27:29] == "rh":
            tmp = np.load(d)
            ctl_right_rh.append(tmp)