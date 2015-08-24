
# coding: utf-8

# In[5]:

get_ipython().magic(u'matplotlib inline')


# In[6]:


"""
Created on Wed Oct  8 14:45:02 2014

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
    data_path = "/home/mje/mnt/Hyp_meg/scratch/Tone_task_MNE/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-Gambling/scratch/"
    n_jobs = 1


raw = Raw(data_path + "/p_01_data_resample_raw_tsss.fif", preload=True)

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12  # T (magnetometers)
            #   eeg=180e-6 #
              )

# raw.resample(200, n_jobs=n_jobs)
raw.filter(None, 30, n_jobs=n_jobs)

# ICA Part
ica = ICA(n_components=0.95, method='fastica')

picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=False,
                       stim=False, exclude='bads')

ica.fit(raw, picks=picks, reject=reject)

# maximum number of components to reject
n_max_ecg, n_max_eog = 3, 1

##########################################################################
# 2) identify bad components by analyzing latent sources.

title = 'Sources related to %s artifacts (red)'

# generate ECG epochs use detection via phase statistics

ecg_epochs = create_ecg_epochs(raw, tmin=-.5, tmax=.5, picks=picks)

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
raw_ica.save(data_path + "p_01_data_ica_filter_resample_tsss_raw.fif", overwrite=True)


# In[7]:

raw_ica.save(data_path + "p_01_data_ica_filter_resample_tsss_raw.fif", overwrite=True)


# In[9]:

"""
========================================================
Extract epochs, average and save evoked response to disk
========================================================

This script shows how to read the epochs from a raw file given
a list of events. The epochs are averaged to produce evoked
data and then saved to disk.

"""
# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Denis A. Engemann <denis.engemann@gmail.com>
#
# License: BSD (3-clause)

import mne
from mne import io
import socket

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/Hyp_meg/scratch/Tone_task_MNE/"
    n_jobs = 1
elif hostname == "isis":
    data_path = "/projects/MINDLAB2015_MEG-Gambling/scratch/"
    n_jobs = 3


raw = mne.io.Raw(data_path + "p_01_data_ica_filter_resample_tsss_raw.fif",
          preload=True)

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12,  # T (magnetometers)
              eeg=180e-6 #
              )

####
# Set parameters
tmin, tmax = -0.2, 0.4

# Select events to extract epochs from.
event_id = {'entrainment': 1,
            'Control': 2,
            'left': 4,
            'right': 8}

#   Setup for reading the raw data
events = mne.find_events(raw)

#   Plot raw data
fig = raw.plot(events=events)

#   Set up pick list: EEG + STI 014 - bad channels (modify to your needs)
include = []  # or stim channels ['STI 014']
# raw.info['bads'] += ['EEG 053']  # bads + 1 more

# pick EEG and MEG channels
picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=False, eog=False,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                    baseline=(None, 0), reject=reject,
                    preload=True)

# Plot epochs.
# epochs.plot(trellis=False, title='Auditory left/right')

# Look at channels that caused dropped events, showing that the subject's
# blinks were likely to blame for most epochs being dropped
# epochs.drop_bad_epochs()
# epochs.plot_drop_log(subject='sample')

# Average epochs and get evoked data corresponding to the left stimulation
#
###############################################################################
# View evoked response


# In[10]:

epochs


# In[13]:

epochs["Control"].plot_psd(fmin=6, fmax=20)


# In[14]:

epochs["entrainment"].plot_psd(fmin=6, fmax=20)


# In[18]:

epochs["entrainment"].plot_psd_topomap()


# In[19]:

epochs["Control"].plot_psd_topomap()


# In[21]:

epochs["entrainment"]


# In[30]:

freqs = np.arange(6, 20, 1)  # define frequencies of interest
n_cycles = freqs / 2.  # different number of cycle per frequency
power_clt, itc_ctl = mne.time_frequency.tfr_morlet(epochs["Control"], freqs=freqs, n_cycles=2, use_fft=True,
                        return_itc=True, decim=1, n_jobs=1)
power_ent, itc_ent = mne.time_frequency.tfr_morlet(epochs["entrainment"], freqs=freqs, n_cycles=2, use_fft=True,
                        return_itc=True, decim=1, n_jobs=1)


# In[27]:

power_cnt.plot_topo(baseline=(None, 0), mode='zscore', title='Average power')


# In[31]:

power_cnt.plot_topomap(ch_type='grad', tmin=0, tmax=None, fmin=8, fmax=12,
                   baseline=(None, 0), mode='zscore', title='Alpha')
power_ent.plot_topomap(ch_type='grad', tmin=0, tmax=None, fmin=8, fmax=12,
                   baseline=(None, 0), mode='zscore', title='Alpha')


# In[32]:

itc_ctl.plot_topomap(ch_type='grad', tmin=0, tmax=None, fmin=8, fmax=12,
                   baseline=(None, 0), mode='zscore', title='Alpha')
itc_ent.plot_topomap(ch_type='grad', tmin=0, tmax=None, fmin=8, fmax=12,
                   baseline=(None, 0), mode='zscore', title='Alpha')


# In[ ]:

itc_ctl.plot_topo(title='Inter-Trial coherence', baseline=(None, 0), mode='zscore',
                  cmap='RdBu')
itc_ent.plot_topo(title='Inter-Trial coherence', baseline=(None, 0), mode='zscore',
                  cmap='RdBu')


# In[39]:

print power_clt.data.max()
print power_ent.data.max()


# In[41]:

epochs.ch_names[-10]


# In[45]:

itc_ctl.plot([-12], baseline=(None, 0), mode='zscore', title='Inter-Trial coherence', vmin=0., vmax=1., cmap='Reds')
itc_ent.plot([-12], baseline=(None, 0), mode='zscore', title='Inter-Trial coherence', vmin=0., vmax=1., cmap='Reds')


# In[ ]:
