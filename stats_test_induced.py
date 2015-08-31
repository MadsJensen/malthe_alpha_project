# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 12:35:33 2015

@author: mje
"""

import numpy as np
import matplotlib.pyplot as plt

import mne
from mne import io
from mne.time_frequency import single_trial_power
from mne.stats import permutation_cluster_test

###############################################################################
# Set parameters
raw_fname = data_path + '/MEG/sample/sample_audvis_raw.fif'
event_fname = data_path + '/MEG/sample/sample_audvis_raw-eve.fif'
event_id = 1
tmin = 0.7
tmax = 2

# Setup for reading the raw data

ch_name = foo.info['ch_names'][220]

# Load condition 1
data_condition_1 = foo["ctl_L", "ctl_R"].get_data()  # as 3D matrix
data_condition_1 *= 1e13  # change unit to fT / cm

data_condition_2= foo["ent_L", "ent_R"].get_data()  # as 3D matrix
data_condition_2 *= 1e13  # change unit to fT / cm


# Take only one channel
data_condition_1 = data_condition_1[:, 220:221, :]
data_condition_2 = data_condition_2[:, 220:221, :]

# Time vector
times = 1e3 * foo.times  # change unit to ms

# Factor to downsample the temporal dimension of the PSD computed by
# single_trial_power.  Decimation occurs after frequency decomposition and can
# be used to reduce memory usage (and possibly comptuational time of downstream
# operations such as nonparametric statistics) if you don't need high
# spectrotemporal resolution.
decim = 1
frequencies = np.arange(8, 13, 1)  # define frequencies of interest
sfreq = foo.info['sfreq']  # sampling in Hz
n_cycles = frequencies / 2.

foo_power_1 = single_trial_power(data_condition_1, sfreq=sfreq,
                                 frequencies=frequencies,
                                 n_cycles=n_cycles, decim=decim)

foo_power_2 = single_trial_power(data_condition_2, sfreq=sfreq,
                                 frequencies=frequencies,
                                 n_cycles=n_cycles, decim=decim)

foo_power_1 = foo_power_1[:, 0, :, :]  # only 1 channel to get 3D matrix
foo_power_2 = foo_power_2[:, 0, :, :]  # only 1 channel to get 3D matrix

# Compute ratio with baseline power (be sure to correct time vector with
# decimation factor)
baseline_mask = times[::decim] < 950
foo_baseline_1 = np.mean(foo_power_1[:, :, baseline_mask], axis=2)
foo_power_1 /= foo_baseline_1[..., np.newaxis]
foo_baseline_2 = np.mean(foo_power_2[:, :, baseline_mask], axis=2)
foo_power_2 /= foo_baseline_2[..., np.newaxis]

###############################################################################
# Compute statistic
threshold = 4
T_obs, clusters, cluster_p_values, H0 = \
    permutation_cluster_test([foo_power_1, foo_power_2],
                             n_permutations=5000, threshold=threshold, tail=0)

###############################################################################
# View time-frequency plots
plt.clf()
plt.subplots_adjust(0.12, 0.08, 0.96, 0.94, 0.2, 0.43)
plt.subplot(2, 1, 1)
evoked_contrast = np.mean(data_condition_1, 0) - np.mean(data_condition_2, 0)
plt.plot(times, evoked_contrast.T)
plt.title('Contrast of evoked response (%s)' % ch_name)
plt.xlabel('time (ms)')
plt.ylabel('Magnetic Field (fT/cm)')
plt.xlim(times[0], times[-1])
plt.ylim(-100, 200)

plt.subplot(2, 1, 2)

# Create new stats image with only significant clusters
T_obs_plot = np.nan * np.ones_like(T_obs)
for c, p_val in zip(clusters, cluster_p_values):
    if p_val <= 0.05:
        T_obs_plot[c] = T_obs[c]

plt.imshow(T_obs,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', cmap='RdBu_r')
plt.imshow(T_obs_plot,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', cmap='RdBu_r')

plt.xlabel('time (ms)')
plt.ylabel('Frequency (Hz)')
plt.title('Induced power (%s)' % ch_name)
plt.show()
