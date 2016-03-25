#  -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 14:45:02 2014.

@author: mje
"""
import mne
import socket
import numpy as np
import os
import glob

from mne.io import Raw
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs

import matplotlib
matplotlib.use('Agg')

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

save_folder = data_path + "filter_ica_data/"
maxfiltered_folder = data_path + "maxfiltered_data/"

# SETTINGS
n_jobs = 1
reject = dict(grad=5000e-13,  # T / m (gradiometers)
              mag=5e-12,  # T (magnetometers)
              eeg=300e-6)  # uVolts (EEG)
l_freq, h_freq = 1, 98  # High and low frequency setting for the band pass
n_freq = 50  # notch filter frequency
decim = 7  # decim value


# Functions #
def filter_data(subject, l_freq=l_freq, h_freq=h_freq, n_freq=n_freq,
                save=True, n_jobs=1):
    """Filter the data.

    params:
    subject : str
        the subject id to be loaded
    l_freq :  int
        the low frequency to filter
    h_freq : int
        the high frequency to filter
    n_freq : int
        the notch filter frequency
    save : bool
        save the filtered data
    n_jobs : int
        The number of CPUs to use in parallel.
    """
    raw = Raw(maxfiltered_folder + "%s_data_mc_raw_tsss.fif" % subject,
              preload=True)

    if n_freq is not None:
        raw.notch_filter(n_freq, n_jobs=n_jobs)

    raw.filter(l_freq, h_freq, n_jobs=n_jobs)

    if save is True:
        raw.save(save_folder + "%s_filtered_data_mc_raw_tsss.fif" % subject,
                 overwrite=True)


def compute_ica(subject):
    """Function will compute ICA on raw and apply the ICA.

    params:
    subject : str
        the subject id to be loaded
    """
    raw = Raw(save_folder + "%s_filtered_data_mc_raw_tsss.fif" % subject,
              preload=True)

    # ICA Part
    ica = ICA(n_components=0.95, method='fastica', max_iter=256)

    picks = mne.pick_types(raw.info, meg=True, eeg=True,
                           stim=False, exclude='bads')

    ica.fit(raw, picks=picks, decim=decim, reject=reject)

    # maximum number of components to reject
    n_max_ecg, n_max_eog = 3, 1

    ##########################################################################
    # 2) identify bad components by analyzing latent sources.
    title = 'Sources related to %s artifacts (red) for sub: %s'

    # generate ECG epochs use detection via phase statistics
    ecg_epochs = create_ecg_epochs(raw, ch_name="ECG002",
                                   tmin=-.5, tmax=.5, picks=picks)
    n_ecg_epochs_found = len(ecg_epochs.events)
    sel_ecg_epochs = np.arange(0, n_ecg_epochs_found, 10)
    ecg_epochs = ecg_epochs[sel_ecg_epochs]

    ecg_inds, scores = ica.find_bads_ecg(ecg_epochs, method='ctps')
    fig = ica.plot_scores(scores, exclude=ecg_inds,
                          title=title % ('ecg', subject))
    fig.savefig(save_folder + "pics/%s_ecg_scores.png" % subject)

    if ecg_inds:
        show_picks = np.abs(scores).argsort()[::-1][:5]

        fig = ica.plot_sources(raw, show_picks, exclude=ecg_inds,
                               title=title % ('ecg', subject), show=False)
        fig.savefig(save_folder + "pics/%s_ecg_sources.png" % subject)
        fig = ica.plot_components(ecg_inds, title=title % ('ecg', subject),
                                  colorbar=True)
        fig.savefig(save_folder + "pics/%s_ecg_component.png" % subject)

        ecg_inds = ecg_inds[:n_max_ecg]
        ica.exclude += ecg_inds

    # estimate average artifact
    ecg_evoked = ecg_epochs.average()
    del ecg_epochs

    # plot ECG sources + selection
    fig = ica.plot_sources(ecg_evoked, exclude=ecg_inds)
    fig.savefig(save_folder + "pics/%s_ecg_sources_ave.png" % subject)

    # plot ECG cleaning
    ica.plot_overlay(ecg_evoked, exclude=ecg_inds)
    fig.savefig(save_folder + "pics/%s_ecg_sources_clean_ave.png" % subject)

    # DETECT EOG BY CORRELATION
    # HORIZONTAL EOG
    eog_epochs = create_eog_epochs(raw, ch_name="EOG001")
    eog_inds, scores = ica.find_bads_eog(raw)
    fig = ica.plot_scores(scores, exclude=eog_inds,
                          title=title % ('eog', subject))
    fig.savefig(save_folder + "pics/%s_eog_scores.png" % subject)

    fig = ica.plot_components(eog_inds, title=title % ('eog', subject),
                              colorbar=True)
    fig.savefig(save_folder + "pics/%s_eog_component.png" % subject)

    eog_inds = eog_inds[:n_max_eog]
    ica.exclude += eog_inds

    del eog_epochs

    ##########################################################################
    # Apply the solution to Raw, Epochs or Evoked like this:
    raw_ica = ica.apply(raw, copy=False)
    ica.save(save_folder + "%s-ica.fif" % subject)  # save ICA componenets
    # Save raw with ICA removed
    raw_ica.save(save_folder + "%s_filtered_ica_mc_raw_tsss.fif" % subject,
                 overwrite=True)
    plt.close("all")


# Run code
os.chdir(maxfiltered_folder)
subjects = glob.glob("*_data_mc_raw_tsss.fif")
subjects = [sub[:4] for sub in subjects]
subjects.sort()
subjects = subjects[-3:]


for subject in subjects:
    filter_data(subject)


for subject in subjects:
    compute_ica(subject)
