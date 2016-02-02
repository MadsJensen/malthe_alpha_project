# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 14:47:21 2016

@author: mje
"""

from mne import read_evokeds
from mne.viz import plot_trans

import socket
import mne
import os


# SETUP PATHS AND PREPARE RAW DATA
hostname = socket.gethostname()

if hostname == "wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

# CHANGE DIR TO SAVE FILES THE RIGTH PLACE
os.chdir(data_path)

subjects_dir = data_path + "fs_subjects_dir/"
save_folder = data_path + "filter_ica_data/"
maxfiltered_folder = data_path + "maxfiltered_data/"
epochs_folder = data_path + "epoched_data/"
tf_folder = data_path + "tf_data/"
mne_folder = data_path + "minimum_norm/"


subject = "0025"
trans_fname = mne_folder + "%s-trans.fif" % subject
epochs = mne.read_epochs(epochs_folder +
                         "%s_filtered_ica_mc_tsss-epo.fif" % subject, 
                         preload=False)
plot_trans(epochs.info, trans_fname, subject=subject, dig=True,
           subjects_dir=subjects_dir)
