# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:17:09 2015

@author: mje
"""
import mne
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator)
import numpy as np

from my_settings import *

# Using the same inverse operator when inspecting single trials Vs. evoked
snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)


for subject in subjects:
    # Load data
    inverse_operator = read_inverse_operator(mne_folder +
                                             "%s-inv.fif" % subject)
    epochs = mne.read_epochs(epochs_folder +
                             "%s_filtered_ica_mc_tsss-epo.fif" % subject)


    for cond in epochs.event_id.keys():
        stcs = apply_inverse_epochs(epochs[cond], inverse_operator, lambda2,
                                    method, pick_ori="normal")
        exec("stcs_%s = stcs" % cond)


lbl_ctl_left = []
lbl_ent_left = []
lbl_ctl_right = []
lbl_ent_right = []

for j in range(len(subjects[:1])):
    src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subjects[j])
    labels = mne.read_labels_from_annot(subjects[j], parc='PALS_B12_Brodmann',
                                        regexp="Bro",
                                        subjects_dir=subjects_dir)
    labels_occ = [labels[6]]

    lbl_ent_left.append(mne.extract_label_time_course(ent_left[j],
                                                      labels=labels_occ,
                                                      src=src,
                                                      mode="pca_flip"))

    lbl_ctl_left.append(mne.extract_label_time_course(ctl_left[j],
                                                      labels=labels_occ,
                                                      src=src,
                                                      mode="pca_flip"))

    lbl_ent_right.append(mne.extract_label_time_course(ent_right[j],
                                                       labels=labels_occ,
                                                       src=src,
                                                       mode="pca_flip"))

    lbl_ctl_right.append(mne.extract_label_time_course(ctl_right[j],
                                                       labels=labels_occ,
                                                       src=src,
                                                       mode="pca_flip"))


lbl_ent_left = np.squeeze(np.asarray(lbl_ent_left))
lbl_ctl_left = np.squeeze(np.asarray(lbl_ctl_left))
lbl_ent_right = np.squeeze(np.asarray(lbl_ent_right))
lbl_ctl_right = np.squeeze(np.asarray(lbl_ctl_right))



def ITC_over_time(data, faverage=True):
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
    result = np.empty([data.shape[1], data.shape[0]])

    for freq in range(result.shape[0]):
        for i in range(result.shape[1]):
            result[freq, i] =\
                np.abs(np.mean(np.exp(1j * (np.angle(data[i, freq, :])))))

    if faverage:
        result = result.mean(axis=0).squeeze()

    return result