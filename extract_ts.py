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

for j in range(len(subjects)):
    src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subjects[j])
    labels = mne.read_labels_from_annot(subjects[j], parc='PALS_B12_Brodmann',
                                        regexp="Bro",
                                        subjects_dir=subjects_dir)
    labels_occ = [labels[6], labels[7]]

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

times = stc_0004_ent_left.times
