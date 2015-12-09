#  -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 14:45:02 2014.

@author: mje
"""
import mne
import socket
import numpy as np
import os

from mne.io import Raw
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs

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
        The number of CPU to use
    """
    raw = Raw(maxfiltered_folder + "%s_data_mc_raw_tsss.fif" % subject,
              preload=True)

    if n_freq is not None:
        raw.notch_filter(n_freq, n_jobs=n_jobs)

    raw.filter(l_freq, h_freq, n_jobs=n_jobs)

    if save is True:
        raw.save(save_folder + "%s_filtered_data_mc_raw_tsss.fif" % subject,
                 overwrite=True)


os.chdir(maxfiltered_folder)
subjects = !ls *_data_mc_raw_tsss.fif
subjects = [sub[:4] for sub in subjects]


for subject in subjects:
    filter_data(subject)


for subject in subjects:


def compute_ica(subject):
    """ Function will compute ICA on raw and apply the ICA.

    params:
    subject : str
        the subject id to be loaded
    """
    raw = Raw(save_folder + "%s_filterd_data_mc_raw_tsss.fif" % subject,
              preload=True)

    # ICA Part
    ica = ICA(n_components=0.95, method='fastica')

    picks = mne.pick_types(raw.info, meg=True, eeg=True,
                           stim=False, exclude='bads')

    ica.fit(raw, picks=picks, decim=decim, reject=reject)

    # maximum number of components to reject
    n_max_ecg, n_max_eog = 3, 1

    ##########################################################################
    # 2) identify bad components by analyzing latent sources.
    title = 'Sources related to %s artifacts (red)'

    # generate ECG epochs use detection via phase statistics
    ecg_epochs = create_ecg_epochs(raw, ch_name="ECG002",
                                   tmin=-.5, tmax=.5, picks=picks)
    n_ecg_epochs_found = len(ecg_epochs.events)
    sel_ecg_epochs = np.range(0, n_ecg_epochs_found, 10)
    ecg_epochs = ecg_epochs[sel_ecg_epochs]

    ecg_inds, scores = ica.find_bads_ecg(ecg_epochs, method='ctps')
    ica.plot_scores(scores, exclude=ecg_inds, title=title % 'ecg')

    if ecg_inds:
        show_picks = np.abs(scores).argsort()[::-1][:5]

        ica.plot_sources(raw, show_picks, exclude=ecg_inds,
                         title=title % 'ecg')
        ica.plot_components(ecg_inds, title=title % 'ecg', colorbar=True)

        ecg_inds = ecg_inds[:n_max_ecg]
        ica.exclude += ecg_inds

    # estimate average artifact
    ecg_evoked = ecg_epochs.average()

    # plot ECG sources + selection
    ica.plot_sources(ecg_evoked, exclude=ecg_inds)

    # plot ECG cleaning
    ica.plot_overlay(ecg_evoked, exclude=ecg_inds)

    # DETECT EOG BY CORRELATION
    # HORIZONTAL EOG
    eog_epochs = create_eog_epochs(raw, ch_name="EOG001")
    eog_inds, scores = ica.find_bads_eog(raw)
    # ica.plot_scores(scores, exclude=eog_inds, title=title % 'eog')

    eog_inds, scores = ica.find_bads_eog(raw)
    ica.plot_scores(scores, exclude=eog_inds, title=title % 'eog')

    show_picks = np.abs(scores).argsort()[::-1][:5]

    ica.plot_sources(raw, show_picks, exclude=eog_inds, title=title % 'eog')
    ica.plot_components(eog_inds, title=title % 'eog', colorbar=True)

    eog_inds = eog_inds[:n_max_eog]
    ica.exclude += eog_inds

    if eog_inds:
        show_picks = np.abs(scores).argsort()[::-1][:5]

        ica.plot_sources(raw, show_picks, exclude=eog_inds,
                        title="Sources related to EOG artifacts (red)")
        ica.plot_components(eog_inds, title="Sources related to EOG artifacts",
                            colorbar=True)

        eog_inds = eog_inds[:n_max_eog]
        ica.exclude += eog_inds

    eog_evoked = create_eog_epochs(raw, tmin=-.5, tmax=.5,
                                picks=picks).average()
    # plot EOG sources + selection
    ica.plot_sources(eog_evoked, exclude=eog_inds)
    ica.plot_overlay(eog_evoked, exclude=eog_inds)  # plot EOG cleaning

    # check the amplitudes do not change
    ica.plot_overlay(raw)  # EOG artifacts remain

    del ecg_epochs
    del ecg_evoked

    # VERTICAL EOG
eog_epochs = create_eog_epochs(raw, ch_name="EOG003")

eog_inds, scores = ica.find_bads_eog(raw)
# ica.plot_scores(scores, exclude=eog_inds, title=title % 'eog')

eog_inds, scores = ica.find_bads_eog(raw)
ica.plot_scores(scores, exclude=eog_inds, title=title % 'eog')

show_picks = np.abs(scores).argsort()[::-1][:5]

ica.plot_sources(raw, show_picks, exclude=eog_inds, title=title % 'eog')
ica.plot_components(eog_inds, title=title % 'eog', colorbar=True)

eog_inds = eog_inds[:n_max_eog]
ica.exclude += eog_inds

if eog_inds:
    show_picks = np.abs(scores).argsort()[::-1][:5]

    ica.plot_sources(raw, show_picks, exclude=eog_inds,
                        title="Sources related to EOG artifacts (red)")
    ica.plot_components(eog_inds, title="Sources related to EOG artifacts",
                        colorbar=True)

    eog_inds = eog_inds[:n_max_eog]
    ica.exclude += eog_inds

###########################################################################
# 3) Assess component selection and unmixing quality

eog_evoked = create_eog_epochs(raw, tmin=-.5, tmax=.5,
                                picks=picks).average()
# plot EOG sources + selection
ica.plot_sources(eog_evoked, exclude=eog_inds)
ica.plot_overlay(eog_evoked, exclude=eog_inds)  # plot EOG cleaning

# check the amplitudes do not change
ica.plot_overlay(raw)  # EOG artifacts remain

##########################################################################
# Apply the solution to Raw, Epochs or Evoked like this:
raw_ica = ica.apply(raw, copy=False)
ica.save("subj_%d-ica.fif" % subject)  # save ICA componenets
# Save raw with ICA removed
raw_ica.save("subj_%d_filter_ica-mc_raw_tsss.fif" % subject,
                overwrite=True)
