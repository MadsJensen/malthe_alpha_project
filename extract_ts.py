# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:17:09 2015

@author: mje
"""
import mne
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator)
from mne.time_frequency import cwt_morlet
import numpy as np

from my_settings import *

# Using the same inverse operator when inspecting single trials Vs. evoked
snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
freqs = np.arange(8, 13, 1)
n_cycle = freqs / 3.

conditions = ["ent_left", "ctl_left", "ent_right", "ctl_right"]

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


for condition in conditions:
    for subject in subjects[:1]:
        itc_res = []
        # Load data
        labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Brodmann',
                                            regexp="Bro",
                                            subjects_dir=subjects_dir)
        labels_occ = [labels[6]]

        inverse_operator = read_inverse_operator(mne_folder +
                                                 "%s-inv.fif" % subject)
        src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subject)

        epochs = mne.read_epochs(epochs_folder +
                                 "%s_ds_filtered_ica_mc_tsss-epo.fif" % subject)
        epochs.resample(250, n_jobs=1)

        stcs = apply_inverse_epochs(epochs[condition], inverse_operator,
                                    lambda2,
                                    method, pick_ori="normal")

        label_ts = []
        for j in range(len(stcs)):
            label_ts.append(mne.extract_label_time_course(stcs[j],
                                                          labels=labels_occ,
                                                          src=src,
                                                          mode="mean_flip"))

        label_ts = np.squeeze(np.asarray(label_ts))

        tfr = cwt_morlet(label_ts, epochs.info["sfreq"], freqs,
                         use_fft=True, n_cycles=n_cycle)

        itc_res.append(ITC_over_trials(tfr))

    itc_res = np.asarray(itc_res)
    np.save(tf_folder + "itc_%S.npy" % condition, itc_res)
