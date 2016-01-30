"""
Doc string goes here.

@author: mje mads [] cnru.dk
"""
import socket
import mne
import os
import sys

cmd = "/usr/local/common/meeg-cfin/configurations/bin/submit_to_isis"

# SETUP PATHS AND PREPARE RAW DATA
hostname = socket.gethostname()

if hostname == "wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

# CHANGE DIR TO SAVE FILES THE RIGTH PLACE
subjects_dir = data_path + "fs_subjects_dir/"
save_folder = data_path + "filter_ica_data/"
maxfiltered_folder = data_path + "maxfiltered_data/"
epochs_folder = data_path + "epoched_data/"
tf_folder = data_path + "tf_data/"
mne_folder = data_path + "minimum_norm/"

os.chdir(mne_folder)

# import subject from commandline arg
subject = str(sys.argv[1])


epochs = mne.read_epochs(epochs_folder +
                         "%s_filtered_ica_mc_tsss-epo.fif" % subject)
cov = mne.compute_covariance(epochs, tmin=None, tmax=-0.01,
                             method="factor_analysis")
cov.save(mne_folder + "%s-cov.fif" % subject)
