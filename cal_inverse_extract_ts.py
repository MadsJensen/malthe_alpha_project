# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:17:09 2015

@author: mje
"""

import mne
from mne.minimum_norm import apply_inverse_epochs, read_inverse_operator
from mne.minimum_norm import apply_inverse

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


fname_inv = data_path + 'p_01-meg-oct-6-inv.fif'
fname_epochs = data_path + 'p_01_ica_filter_ds_tsss-epo.fif'

# Using the same inverse operator when inspecting single trials Vs. evoked
snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2

method = "MNE"  # use dSPM method (could also be MNE or sLORETA)

# Load data
inverse_operator = read_inverse_operator(fname_inv)
epochs = mne.read_epochs(fname_epochs)
# Set up pick list

# Get evoked data (averaging across trials in sensor space)
evoked = epochs.average()

# Compute inverse solution and stcs for each epoch
# Use the same inverse operator as with evoked data (i.e., set nave)
# If you use a different nave, dSPM just scales by a factor sqrt(nave)

for cond in epochs.event_id.keys():
    stcs = apply_inverse_epochs(epochs[cond], inverse_operator, lambda2, method,
                                pick_ori="normal")
    exec("stcs_%s = stcs" % cond)


from mne.minimum_norm import read_inverse_operator, source_induced_power

# Compute a source estimate per frequency band including and excluding the
# evoked response
frequencies = np.arange(7, 16, 1)  # define frequencies of interest
n_cycles = frequencies / 3.  # different number of cycle per frequency

# subtract the evoked response in order to exclude evoked activity
epochs_induced = epochs["ent_L", "ent_R" ].copy().subtract_evoked()

#plt.close('all')

for ii, (this_epochs, title) in enumerate(zip([epochs["ent_L", "ent_R"],
                                                epochs_induced],
                                              ['evoked + induced',
                                               'induced only'])):
    # compute the source space power and phase lock
    power, phase_lock = source_induced_power(
        this_epochs, inverse_operator, frequencies, label,
        baseline=(0.7, 0.95),
        baseline_mode='zscore', n_cycles=n_cycles, n_jobs=n_jobs)

    power = np.mean(power, axis=0)  # average over sources
    phase_lock = np.mean(phase_lock, axis=0)  # average over sources
    times = epochs.times

    ##########################################################################
    # View time-frequency plots
    plt.subplots_adjust(0.1, 0.08, 0.96, 0.94, 0.2, 0.43)
    plt.subplot(2, 2, 2 * ii + 1)
    plt.imshow(20 * power,
               extent=[times[60], times[260], frequencies[0], frequencies[-1]],
               aspect='auto', origin='lower', cmap='RdBu_r')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Power (%s)' % title)
    plt.colorbar()

    plt.subplot(2, 2, 2 * ii + 2)
    plt.imshow(phase_lock,
               extent=[times[60], times[260], frequencies[0], frequencies[-1]],
               aspect='auto', origin='lower',
               cmap='RdBu_r')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Phase-lock (%s)' % title)
    plt.colorbar()

plt.show()
