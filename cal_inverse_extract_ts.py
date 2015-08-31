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

method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

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

