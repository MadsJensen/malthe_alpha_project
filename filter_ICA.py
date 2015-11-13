#  -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 14:45:02 2014.

@author: mje
"""
import mne
import socket
import numpy as np
# import matplotlib.pylab as plt

from mne.io import Raw
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs

# %%
# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    n_jobs = 3


raw = Raw(data_path + "subj_2_tsss-mc_autobad-raw.fif", preload=True)
raw2 = Raw(data_path + "subj_2_tsss-mc_autobad-raw-1.fif", preload=True)
raw3 = Raw(data_path + "subj_2_tsss-mc_autobad-raw-2.fif", preload=True)

raw.append([raw2, raw3])

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12  # T (magnetometers)
              # eeg=180e-6 #
              )

#raw_orig = raw.copy()

# raw.resample(400, n_jobs=n_jobs)
raw.filter(1, 98, n_jobs=n_jobs)
raw.notch_filter(50, n_jobs=n_jobs)
# raw.resample(250, n_jobs=3)


# ICA Part
ica = ICA(n_components=0.95, method='fastica')

picks = mne.pick_types(raw.info, meg=True, eeg=False,
                       stim=False, exclude='bads')

ica.fit(raw, picks=picks, reject=reject)

# maximum number of components to reject
n_max_ecg, n_max_eog = 3, 1

##########################################################################
# 2) identify bad components by analyzing latent sources.

title = 'Sources related to %s artifacts (red)'

# generate ECG epochs use detection via phase statistics

ecg_epochs = create_ecg_epochs(raw, ch_name="ECG002",
                               tmin=-.5, tmax=.5, picks=picks)

ecg_inds, scores = ica.find_bads_ecg(ecg_epochs, method='ctps')
ica.plot_scores(scores, exclude=ecg_inds, title=title % 'ecg')

if ecg_inds:
    show_picks = np.abs(scores).argsort()[::-1][:5]

    ica.plot_sources(raw, show_picks, exclude=ecg_inds,
                     title=title % 'ecg')
    ica.plot_components(ecg_inds, title=title % 'ecg', colorbar=True)

    ecg_inds = ecg_inds[:n_max_ecg]
    ica.exclude += ecg_inds

# detect EOG by correlation


eog_epochs = create_eog_epochs(raw, ch_name="EOG001")

eog_inds, scores = ica.find_bads_eog(raw)
ica.plot_scores(scores, exclude=eog_inds, title=title % 'eog')

if eog_inds:
    show_picks = np.abs(scores).argsort()[::-1][:5]

    # ica.plot_sources(raw, show_picks, exclude=eog_inds,
#  title="Sources related to EOG artifacts (red)")
    ica.plot_components(eog_inds, title="Sources related to EOG artifacts",
                        colorbar=True)

    eog_inds = eog_inds[:n_max_eog]
    ica.exclude += eog_inds


#eog_epochs = create_eog_epochs(raw, ch_name="ECG005")
#
#eog_inds, scores = ica.find_bads_eog(raw)
#ica.plot_scores(scores, exclude=eog_inds, title=title % 'eog')
#
#if eog_inds:
#    show_picks = np.abs(scores).argsort()[::-1][:5]
#
#    # ica.plot_sources(raw, show_picks, exclude=eog_inds,
##  title="Sources related to EOG artifacts (red)")
#    ica.plot_components(eog_inds, title="Sources related to EOG artifacts",
#                        colorbar=True)
#
#    eog_inds = eog_inds[:n_max_eog]
#    ica.exclude += eog_inds
#


###########################################################################
# 3) Assess component selection and unmixing quality

# estimate average artifact
ecg_evoked = ecg_epochs.average()
# plot ECG sources + selection
ica.plot_sources(ecg_evoked, exclude=ecg_inds)
# plot ECG cleaning
ica.plot_overlay(ecg_evoked, exclude=ecg_inds)

eog_evoked = create_eog_epochs(raw, tmin=-.5, tmax=.5,
                               picks=picks).average()
# plot EOG sources + selection
# ica.plot_sources(eog_evoked, exclude=eog_inds)
ica.plot_overlay(eog_evoked, exclude=eog_inds)  # plot EOG cleaning

# check the amplitudes do not change
ica.plot_overlay(raw)  # EOG artifacts remain

##########################################################################
# Apply the solution to Raw, Epochs or Evoked like this:
raw_ica = ica.apply(raw, copy=False)
raw_ica.save("subj_2_filter_ica-mc_raw_tsss.fif",
             overwrite=True)
