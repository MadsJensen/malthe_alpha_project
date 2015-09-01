
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
from mne.viz import iter_topography
from mne.connectivity import spectral_connectivity

import socket

import numpy as np
import matplotlib.pyplot as plt
# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/Malthe_proj/scratch/"
    n_jobs = 1
elif hostname == "isis":
    data_path = "/projects/MINDLAB2015_MEG-Gambling/scratch/"
    n_jobs = 3


subjects_dir = data_path + "fs_subjects_dir/"

raw = mne.io.Raw(data_path + "p_01_data_ica_filter_resample_tsss_raw.fif",
          preload=False)

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12  # T (magnetometers)
#              eeg=180e-6 #
              )

####
# Set parameters
tmin, tmax = 0.7, 2.5
baseline = (0.7, 0.95)


# Select events to extract epochs from.
event_id = {'ent_L': 10,
            'ent_R': 11,
            'ctl_R': 21,
            'ctl_L': 20}

#   Setup for reading the raw data
events = mne.find_events(raw)

tmp_eve = events.copy()

for j in range(len(tmp_eve)):
    if tmp_eve[j, 2] == 1 and tmp_eve[j+1, 2] == 4:
        tmp_eve[j, 2] = 10
    elif tmp_eve[j, 2] == 1 and tmp_eve[j+1, 2] == 8:
        tmp_eve[j, 2] = 11
    elif tmp_eve[j, 2] == 2 and tmp_eve[j+1, 2] == 4:
        tmp_eve[j, 2] = 20
    elif tmp_eve[j, 2] == 2 and tmp_eve[j+1, 2] == 8:
        tmp_eve[j, 2] = 21


#   Plot raw data
# fig = raw.plot(events=events)

#   Set up pick list: EEG + STI 014 - bad channels (modify to your needs)
include = []  # or stim channels ['STI 014']
# raw.info['bads'] += ['EEG 053']  # bads + 1 more

# pick EEG and MEG channels
picks = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=False,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, tmp_eve, event_id, tmin, tmax, picks=picks,
                    baseline=(0.7, 0.95), reject=reject,
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

freqs = np.arange(6, 30, 1)  # define frequencies of interest
n_cycles = freqs / 2.  # different number of cycle per frequency
power_ent_L, itc_ent_L = mne.time_frequency.tfr_morlet(epochs["ent_L"],
                                                       freqs=freqs,
                                                       n_cycles=n_cycles,
                                                       use_fft=True,
                                                       return_itc=True,
                                                       decim=1,
                                                       n_jobs=n_jobs)
power_ent_R, itc_ent_R = mne.time_frequency.tfr_morlet(epochs["ent_R"],
                                                       freqs=freqs,
                                                       n_cycles=n_cycles,
                                                       use_fft=True,
                                                       return_itc=True,
                                                       decim=1,
                                                       n_jobs=n_jobs)

power_ctl_L, itc_ctl_L = mne.time_frequency.tfr_morlet(epochs["ctl_l"],
                                                       freqs=freqs,
                                                       n_cycles=n_cycles,
                                                       use_fft=True,
                                                       return_itc=True,
                                                       decim=1,
                                                       n_jobs=n_jobs)
power_ctl_R, itc_ctl_R = mne.time_frequency.tfr_morlet(epochs["ctl_R"],
                                                       freqs=freqs,
                                                       n_cycles=n_cycles,
                                                       use_fft=True,
                                                       return_itc=True,
                                                       decim=1,
                                                       n_jobs=n_jobs)


# In[27]:

power_ent_L.plot_topo(baseline=baseline, mode='logratio',
                    title='Average power: ent_L')
power_ent_R.plot_topo(baseline=baseline, mode='logratio',
                    title='Average power: ent_R')
                    
power_ctl_L.plot_topo(baseline=baseline, mode='logratio',
                      title='Average power: ctl_L')
power_ctl_R.plot_topo(baseline=baseline, mode='logratio',
                      title='Average power: ctl_R')



itc_ent_L.plot_topo(baseline=baseline, mode='logratio',
                    title='ITC: ent_L')
itc_ent_R.plot_topo(baseline=baseline, mode='logratio',
                    title='ITC: ent_R')
                    
itc_ctl_L.plot_topo(baseline=baseline, mode='logratio',
                      title='ITC: ctl_L')
itc_ctl_R.plot_topo(baseline=baseline, mode='logratio',
                      title='ITC: ctl_R')
# In[31]:



#### Power ####
power_ctl_L.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, grads: ctl_L')
#                     vmin=0, vmax=5)
power_ent_L.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, grads: ent_L')

power_ctl_R.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, grads: Ctl_R')
#                     vmin=0, vmax=5)
power_ent_R.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, grads: ent_R')



power_ctl_L.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, mags: ctl_L')
#                     vmin=0, vmax=5)
power_ent_L.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, mags: ent_L')

power_ctl_R.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, mags: ctl_R')
#                     vmin=0, vmax=5)
power_ent_R.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Power Alpha, mags: ent_R')



#### ITC ####
itc_ctl_L.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, grads: ctl_L')
#                     vmin=0, vmax=5)
itc_ent_L.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, grads: ent_L')

itc_ctl_R.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, grads: ctl_R')
#                     vmin=0, vmax=5)
itc_ent_R.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, grads: ent_R')



itc_ctl_L.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, mags: ctl_L')

#                     vmin=0, vmax=5)
itc_ent_L.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, mags: ent_L')

itc_ctl_R.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, mags: ctl_R')
#                     vmin=0, vmax=5)
itc_ent_R.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, mags: ent_R')




#### Diff plots ####
itc_diff_L.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, mags: diff')

itc_diff_L.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Alpha, grad: diff')

itc_diff_L.plot_topo(baseline=baseline, mode='zscore',
                    title='ITC: diff_L')

itc_diff_R.plot_topo(baseline=baseline, mode='zscore',
                    title='ITC: diff_R')

# In[39]:

print power_clt.data.max()
print power_ent.data.max()


# In[41]:

epochs.ch_names[-10]


fmin, fmax = 8., 13.
sfreq = epochs.info['sfreq']  # the sampling frequency
tmin = 0.0  # exclude the baseline period

conditions = ["ent_L", "ent_R", "ctl_L", "ctl_R"]
#conditions = ["ent_L"]
plv_results = {}

for cond in conditions:
    con, freqs, times, n_epochs, n_tapers = spectral_connectivity(
        epochs[cond], method='plv', 
        mode='multitaper', 
        sfreq=sfreq,
        fmin=fmin, fmax=fmax,
        faverage=True,
        tmin=1, tmax=2,
        mt_adaptive=False,
        n_jobs=1)
    
    res = {"con": con, "freqs": freqs, "times": times,
           "n_epochs": n_epochs, "n_tapers": n_tapers}
    plv_results.update({cond: res})



#### Plot Psds ####
def my_callback(ax, ch_idx):
    """
    This block of code is executed once you click on one of the channel axes
    in the plot. To work with the viz internals, this function should only take
    two parameters, the axis and the channel or data index.
    """
    ax.plot(freqs, psds[ch_idx], color='red')
    ax.set_xlabel = 'Frequency (Hz)'
    ax.set_ylabel = 'Power (dB)'

for ax, idx in iter_topography(epochs.info,
                               fig_facecolor='white',
                               axis_facecolor='white',
                               axis_spinecolor='white',
                               on_pick=my_callback):
    ax.plot(psds_db[idx], color='red')

plt.gcf().suptitle('Power spectral densities')
plt.show()
