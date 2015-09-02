# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:00:32 2015

@author: mje
"""
import mne
from mne.minimum_norm import (make_inverse_operator, apply_inverse,
                              write_inverse_operator)
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
                           
fname_fwd = data_path + 'p_01-fwd.fif'
fname_cov = data_path + 'p_01-cov.fif'


snr = 1.0
lambda2 = 1.0 / snr ** 2

# Load data
evoked = mne.read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
forward_meeg = mne.read_forward_solution(fname_fwd, surf_ori=True)
noise_cov = mne.read_cov(fname_cov)

# Restrict forward solution as necessary for MEG
forward_meg = mne.pick_types_forward(forward_meeg, meg=True, eeg=False)
# Alternatively, you can just load a forward solution that is restricted
forward_eeg = mne.read_forward_solution(fname_fwd_eeg, surf_ori=True)

# make an M/EEG, MEG-only, and EEG-only inverse operators
info = epochs.info
inverse_operator_meeg = make_inverse_operator(info, forward_meeg, noise_cov,
                                              loose=0.2, depth=0.8)
inverse_operator_meg = make_inverse_operator(epochs.info, forward_meg, noise_cov,
                                             loose=0.2, depth=0.8)
inverse_operator_eeg = make_inverse_operator(info, forward_eeg, noise_cov,
                                             loose=0.2, depth=0.8)

write_inverse_operator('sample_audvis-meeg-oct-6-inv.fif',
                       inverse_operator_meeg)
write_inverse_operator('p_01-meg-oct-6-inv.fif',
                       inverse_operator_meg)
write_inverse_operator('sample_audvis-eeg-oct-6-inv.fif',
                       inverse_operator_eeg)
                              