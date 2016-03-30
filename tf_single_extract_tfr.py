from my_settings import *
import numpy as np
import mne
from mne.minimum_norm import read_inverse_operator
from tf_analyses_functions import single_epoch_tf_source


conditions = ["ctl_left", "ent_left", "ent_right", "ctl_right"]
ctl_left_results = []
ctl_right_results = []
ent_left_results = []
ent_right_results = []

for subject in subjects[:1]:
    epochs = mne.read_epochs(epochs_folder +
                             "%s_ds_filtered_ica_mc_tsss-epo.fif" % subject)
    inv = read_inverse_operator(mne_folder + "%s-inv.fif" % subject)
    src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subject)
    labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Brodmann',
                                        regexp="Bro",
                                        subjects_dir=subjects_dir)
    for condition in conditions:
        res = single_epoch_tf_source(epochs[condition], condition,
                                     inv, src, label=[labels[6]])

        if condition == "ctl_left":
            ctl_left_results.append(res)
        elif condition == "ctl_right":
            ctl_right_results.append(res)
        elif condition == "ent_left":
            ent_left_results.append(res)
        elif condition == "ent_right":
            ent_right_results.append(res)

    for condition in conditions:
        if condition == "ctl_left":
            np.save(tf_folder + "%s_%s_ba-17_left.npy" % (subject, condition),
                    ctl_left_results)
        elif condition == "ctl_right":
            np.save(tf_folder + "%s_%s_ba-17_left.npy" % (subject, condition),
                    ctl_right_results)
        elif condition == "ent_left":
            np.save(tf_folder + "%s_%s_ba-17_left.npy" % (subject, condition),
                    ent_left_results)
        elif condition == "ent_right":
            np.save(tf_folder + "%s_%s_ba-17_left.npy" % (subject, condition),
                    ent_right_results)
