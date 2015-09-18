# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 08:41:17 2015.

@author: mje
"""
import numpy as np
import numpy.random as npr
import os
import socket
import mne
# import pandas as pd

from mne.connectivity import spectral_connectivity
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator)


#  Permutation test.
def permutation_resampling(case, control, num_samples, statistic):
    """
    Permutation test.

    Return p-value that statistic for case is different
    from statistc for control.
    """
    observed_diff = abs(statistic(case) - statistic(control))
    num_case = len(case)

    combined = np.concatenate([case, control])
    diffs = []
    for i in range(num_samples):
        xs = npr.permutation(combined)
        diff = np.mean(xs[:num_case]) - np.mean(xs[num_case:])
        diffs.append(diff)

    pval = (np.sum(diffs > observed_diff) +
            np.sum(diffs < -observed_diff))/float(num_samples)
    return pval, observed_diff, diffs


def permutation_test(a, b, num_samples, statistic):
    """
    Permutation test.

    Return p-value that statistic for a is different
    from statistc for b.
    """
    observed_diff = abs(statistic(b) - statistic(a))
    num_a = len(a)

    combined = np.concatenate([a, b])
    diffs = []
    for i in range(num_samples):
        xs = npr.permutation(combined)
        diff = np.mean(xs[:num_a]) - np.mean(xs[num_a:])
        diffs.append(diff)

    pval = np.sum(np.abs(diffs) >= np.abs(observed_diff)) / float(num_samples)
    return pval, observed_diff, diffs


# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    n_jobs = 1

subjects_dir = data_path + "fs_subjects_dir/"

# change dir to save files the rigth place
os.chdir(data_path)


fname_inv = data_path + '0001-meg-oct-6-inv.fif'
fname_epochs = data_path + '0001_p_03_filter_ds_ica-mc_tsss-epo.fif'
fname_evoked = data_path + "0001_p_03_filter_ds_ica-mc_raw_tsss-ave.fif"

# Parameters
snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2

method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

# Load data
inverse_operator = read_inverse_operator(fname_inv)
epochs = mne.read_epochs(fname_epochs)

# Get labels for FreeSurfer 'aparc' cortical parcellation with 34 labels/hemi
#labels = mne.read_labels_from_annot('0001', parc='PALS_B12_Lobes',
labels = mne.read_labels_from_annot('0001', parc='PALS_B12_Brodmann',
                                    regexp="Brodmann",
                                    subjects_dir=subjects_dir)

labels_occ = labels[6:12]

# labels = mne.read_labels_from_annot('subject_1', parc='aparc.DKTatlas40',
#                                     subjects_dir=subjects_dir)

for cond in epochs.event_id.keys():
    stcs = apply_inverse_epochs(epochs[cond], inverse_operator, lambda2,
                                method, pick_ori="normal")
    exec("stcs_%s = stcs" % cond)

labels_name = [label.name for label in labels_occ]

for label in labels_occ:
    labels_name += [label.name]

# Extract  time series
ts_ctl_left = mne.extract_label_time_course(stcs_ctl_left,
                                            labels_occ,
                                            src=inverse_operator["src"],
                                            mode = "mean_flip")

ts_ent_left = mne.extract_label_time_course(stcs_ent_left,
                                            labels_occ,
                                            src=inverse_operator["src"],
                                            mode = "mean_flip")

stcs_all_left = stcs_ctl_left + stcs_ent_left
ts_all_left = np.asarray(mne.extract_label_time_course(stcs_all_left,
                                            labels_occ,
                                            src=inverse_operator["src"],
                                            mode = "mean_flip"))

number_of_permutations = 2000
index = np.arange(0, len(ts_all_left))
permutations_results = np.empty(number_of_permutations)
fmin, fmax = 7, 12
tmin, tmax = 0, 1
con_method = "plv"

diff_permuatation = np.empty([6, 6, number_of_permutations])


# diff
con_ctl, freqs_ctl, times_ctl, n_epochs_ctl, n_tapers_ctl =\
        spectral_connectivity(
            ts_ctl_left,
            method=con_method,
            mode='multitaper',
            sfreq=250,
            fmin=fmin, fmax=fmax,
            faverage=True,
            tmin=tmin, tmax=tmax,
            mt_adaptive=False,
            n_jobs=1,
            verbose=None)

con_ent, freqs_ent, times_ent, n_epochs_ent, n_tapers_ent =\
        spectral_connectivity(
            ts_ent_left,
            method=con_method,
            mode='multitaper',
            sfreq=250,
            fmin=fmin, fmax=fmax,
            faverage=True,
            tmin=tmin, tmax=tmax,
            mt_adaptive=False,
            n_jobs=1,
            verbose=None)


diff = con_ctl[:, :, 0] - con_ent[:, :, 0]


for i in range(number_of_permutations):
    index = np.random.permutation(index)
    tmp_ctl = ts_all_left[index[:64], :, :]
    tmp_case = ts_all_left[index[64:], :, :]

    con_ctl, freqs_ctl, times_ctl, n_epochs_ctl, n_tapers_ctl =\
        spectral_connectivity(
             tmp_ctl,
             method=con_method,
             mode='multitaper',
             sfreq=250,
             fmin=fmin, fmax=fmax,
             faverage=True,
             tmin=tmin, tmax=tmax,
             mt_adaptive=False,
             n_jobs=1)

    con_case, freqs_case, times_case, n_epochs_case, n_tapers_case =\
        spectral_connectivity(
             tmp_case,
             method=con_method,
             mode='multitaper',
             sfreq=250,
             fmin=fmin, fmax=fmax,
             faverage=True,
             tmin=tmin, tmax=tmax,
             mt_adaptive=False,
             n_jobs=1)

    diff_permuatation[:, :, i] = con_ctl[:, :, 0] - con_case[:, :, 0]


pval = np.empty_like(diff)

for h in range(diff.shape[0]):
    for j in range(diff.shape[1]):
        if diff[h, j] != 0:
            pval[h, j] = np.sum(np.abs(diff_permuatation[h, h, :] >=
                         np.abs(diff[h, j, :])))/float(number_of_permutations)

#            np.sum(np.abs(diff[h, j]) >= np.abs(
#                diff_permuatation[h, j, :]))\
#                 / float(number_of_permutations)
