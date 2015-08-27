
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
event_id = {'entrainment': 1,
            'Control': 2,
            'left': 4,
            'right': 8}

#   Setup for reading the raw data
events = mne.find_events(raw)

#   Plot raw data
# fig = raw.plot(events=events)

#   Set up pick list: EEG + STI 014 - bad channels (modify to your needs)
include = []  # or stim channels ['STI 014']
# raw.info['bads'] += ['EEG 053']  # bads + 1 more

# pick EEG and MEG channels
picks = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=False,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
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

freqs = np.arange(6, 20, 1)  # define frequencies of interest
n_cycles = freqs / 2.  # different number of cycle per frequency
power_clt, itc_ctl = mne.time_frequency.tfr_morlet(epochs["Control"],
                                                   freqs=freqs,
                                                   n_cycles=n_cycles,
                                                   use_fft=True,
                                                   return_itc=True,
                                                   decim=1,
                                                   n_jobs=1)
power_ent, itc_ent = mne.time_frequency.tfr_morlet(epochs["entrainment"],
                                                   freqs=freqs,
                                                   n_cycles=n_cycles,
                                                   use_fft=True,
                                                   return_itc=True,
                                                   decim=1,
                                                   n_jobs=1)


# In[27]:

power_clt.plot_topo(baseline=baseline, mode='logratio',
                    title='Average power: Control')
power_ent.plot_topo(baseline=baseline, mode='logratio',
                    title='Average power: Entraiment')

# In[31]:



#### Power ####
power_clt.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='Power Control: Alpha',
                     cmap="RdBu_r")
#                     vmin=0, vmax=5)
power_ent.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='Entrain: Alpha',
                     cmap="RdBu_r")

power_clt.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='power Control: Alpha, Mags',
                     cmap="RdBu_r",
                     vmin=None, vmax=None)

power_ent.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='power Entrain: Alpha, mags',
                     cmap="RdBu_r",
                     vmin=None, vmax=None)

# grads                     
power_clt.plot_topomap(ch_type='grad', tmin=0, tmax=0.5, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='power Control: Alpha, grads',
                     cmap="RdBu_r",
                     vmin=None, vmax=None)

power_ent.plot_topomap(ch_type='grad', tmin=0, tmax=0.5, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='power Entrain: Alpha, grads',
                     cmap="RdBu_r",
                     vmin=None, vmax=None)



#### ITC ####
itc_ctl.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Control: Alpha')
#                     vmin=0, vmax=5)
itc_ent.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='logratio',
                     title='Entrain: Alpha')


itc_ctl.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Control: Alpha, Mags',
                     cmap="RdBu_r",
                     vmin=None, vmax=20)

itc_ent.plot_topomap(ch_type='mag', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Entrain: Alpha, mags',
                     cmap="RdBu_r",
                     vmin=None, vmax=20)
# grads                     
itc_ctl.plot_topomap(ch_type='grad', tmin=0.7, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Control: Alpha, grads',
                     cmap="RdBu_r",
                     vmin=None, vmax=None)

itc_ent.plot_topomap(ch_type='grad', tmin=1, tmax=2, fmin=8, fmax=12,
                     baseline=baseline, mode='zscore',
                     title='ITC Entrain: Alpha, grads',
                     cmap="RdBu_r",
                     vmin=None, vmax=None)


# In[39]:

print power_clt.data.max()
print power_ent.data.max()


# In[41]:

epochs.ch_names[-10]


# In[45]:

itc_ctl.plot([-12], baseline=baseline, mode='zscore',
             title='ITC: Ctl', vmin=0., vmax=None, cmap='RdBu_r')
itc_ent.plot([-12], baseline=baseline, mode='zscore',
             title='ITC: Ent', vmin=0., vmax=None, cmap='RdBu_r')




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
