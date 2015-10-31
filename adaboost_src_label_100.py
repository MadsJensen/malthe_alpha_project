"""Doc string Here."""

import mne
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator)

import socket
import numpy as np
# import matplotlib.pyplot as plt

from sklearn.ensemble import AdaBoostClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import StratifiedKFold, cross_val_score
# from sklearn.preprocessing import scale
# import seaborn as sns

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    # data_path = "/home/mje/mnt/caa/scratch/"
    data_path = "/home/mje/Projects/malthe_alpha_project/data/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    n_jobs = 1

subjects_dir = data_path + "fs_subjects_dir/"

fname_inv = data_path + '0001-meg-oct-6-inv.fif'
fname_epochs = data_path + '0001_p_03_filter_ds_ica-mc_tsss-epo.fif'
fname_evoked = data_path + "0001_p_03_filter_ds_ica-mc_raw_tsss-ave.fif"


snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

# load labels
labels = mne.read_labels_from_annot('0001', parc='PALS_B12_Lobes',
                                    # regexp="Bro",
                                    subjects_dir=subjects_dir)

labels_occ = [labels[9], labels[10]]

# Load data
inverse_operator = read_inverse_operator(fname_inv)
epochs = mne.read_epochs(fname_epochs)

epochs.crop(0, 1.1)
epochs.resample(200)

stcs_ent_left = apply_inverse_epochs(epochs["ent_left"], inverse_operator,
                                     lambda2, method, pick_ori="normal")

stcs_ctl_left = apply_inverse_epochs(epochs["ctl_left"], inverse_operator,
                                     lambda2, method, pick_ori="normal")

# src_ctl_l = np.asarray([stc.data.reshape(-1) for stc in stcs_ctl_left])
# src_ent_l = np.asarray([stc.data.reshape(-1) for stc in stcs_ent_left])

# data_ctl_l = np.squeeze(np.asarray(
#    mne.extract_label_time_course(stcs_ctl_left,
#                                  labels_occ[1],
#                                  inverse_operator["src"],
#                                  mode="pca_flip")))
#
# data_ent_l = np.squeeze(np.asarray(
#    mne.extract_label_time_course(stcs_ent_left,
#                                  labels_occ[1],
#                                  inverse_operator["src"],
#                                  mode="pca_flip")))

data_ent_l = np.asarray([stc.in_label(labels_occ[1]).data.reshape(-1)
                        for stc in stcs_ent_left])
data_ctl_l = [stc.in_label(labels_occ[1]).data.reshape(-1)
              for stc in stcs_ctl_left]

X = np.vstack([data_ctl_l, data_ent_l])  # data for classiication
y = np.concatenate([np.zeros(64), np.ones(64)])  # Classes for X

n_estimators = np.arange(100, 1000, 100)
meta_score = np.empty_like(n_estimators)
for j in range(len(meta_score)):
    # Setup classificer
    bdt = AdaBoostClassifier(algorithm="SAMME.R",
                             n_estimators=n_estimators[j])

    n_folds = 10  # number of folds used in cv
    cv = StratifiedKFold(y, n_folds=n_folds)
    scores = cross_val_score(X, y, cv=cv)
    meta_score[j] = scores.mean()

    # scores = np.zeros(n_folds)  # aaray to save scores
    # feature_importance = np.zeros(X.shape[1])  # array to save features
    #
    # for ii, (train, test) in enumerate(cv):
    #     bdt.fit(X[train], y[train])
    #     y_pred = bdt.predict(X[test])
    #     y_test = y[test]
    #     scores[ii] = np.sum(y_pred == y_test) / float(len(y_test))
    #     feature_importance += bdt.feature_importances_
    #
    # feature_importance_std = scale(feature_importance)
    # feature_importance /= (ii + 1)  # create average importance

    # # create mask to avoid division error
    # feature_importance = np.ma.masked_array(feature_importance,
    #                                         feature_importance == 0)
    # # normalize scores for visualization purposes
    # feature_importance /= feature_importance.std(axis=1)[:, None]
    # feature_importance -= feature_importance.mean(axis=1)[:, None]

    # vertices = [np.array([], int), stc.in_label(labels_occ[1]).rh_vertno]
    # shape = stcs_ent_left[0].in_label(labels_occ[1]).shape

    # stc_feat = mne.SourceEstimate(feature_importance.reshape(shape),
    #                               vertices=vertices,
    #                               tmin=0, tstep=stc.tstep,
    #                               subject='0001')
    #
    # # stc_feat.save(data_path + "stc_adaboost_feature_label")
    #
    # stc_feat_std = mne.SourceEstimate(feature_importance_std.reshape(shape),
    #                                   vertices=vertices,
    #                                   tmin=0, tstep=stc.tstep,
    #                                   subject='0001')

# stc_feat_std.save(data_path + "stc_adaboost_feature_label_std")

# np.savetxt(data_path + "adaboost_label_scores.csv", scores, delimiter=",")

# scores_10 = cross_val_score(bdt, X, y, cv=10, n_jobs=1, verbose=False)
