import numpy as np
import os

from sklearn.cross_validation import (cross_val_score, StratifiedKFold)
from sklearn.pipeline import make_pipeline
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler

from my_settings import *


def ITC_over_trials(data, faverage=True):
    """Calculate the ITC over time.

    Parameters
    ----------
    data : numpy array
        It should be trials x channels x frequencies x times.
    faverage : bool
        If true the average is returned, If false each frequency is returned.

    Returns
    -------
    result : numpy array
        The result is a numpy array with the length equal to the number of
        trials.
    """
    result = np.empty([data.shape[1], data.shape[-1]])

    for freq in range(result.shape[0]):
        for i in range(result.shape[1]):
            result[freq, i] =\
                np.abs(np.mean(np.exp(1j * (np.angle(data[:, freq, i])))))

    if faverage:
        result = result.mean(axis=0).squeeze()

    return result


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

itc_ent_left_lh = np.array([ITC_over_trials(ts) for ts in ent_left_lh])
itc_ent_left_rh = np.array([ITC_over_trials(ts) for ts in ent_left_rh])
itc_ent_right_lh = np.array([ITC_over_trials(ts) for ts in ent_right_lh])
itc_ent_right_rh = np.array([ITC_over_trials(ts) for ts in ent_right_rh])

itc_ctl_left_lh = np.array([ITC_over_trials(ts) for ts in ctl_left_lh])
itc_ctl_left_rh = np.array([ITC_over_trials(ts) for ts in ctl_left_rh])
itc_ctl_right_lh = np.array([ITC_over_trials(ts) for ts in ctl_right_lh])
itc_ctl_right_rh = np.array([ITC_over_trials(ts) for ts in ctl_right_rh])


X = np.vstack([itc_ent_left_lh, itc_ent_left_rh,
               itc_ent_right_lh, itc_ent_right_rh,
               itc_ctl_left_lh, itc_ctl_left_rh,
               itc_ctl_right_lh, itc_ctl_right_rh])

y = np.concatenate([[0]*20, [0]*20, [0]*20, [0]*20,
                    [1]*20, [1]*20, [1]*20, [1]*20])
cv = StratifiedKFold(y, n_folds=10)

ada_params = {"n_estimators": np.arange(10, 350, 50)}

scaler_pipe = make_pipeline(StandardScaler(), AdaBoostClassifier())
ada_grid = GridSearchCV(scaler_pipe, param_grid=ada_params, cv=cv)

ada_grid.fit(X, y)
