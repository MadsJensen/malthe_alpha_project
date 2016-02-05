"""
These are general settings to be used in the current project.

@author: mje
@email: mads [] cnru.dk
"""

import socket

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

subjects_dir = data_path + "fs_subjects_dir/"
save_folder = data_path + "filter_ica_data/"
maxfiltered_folder = data_path + "maxfiltered_data/"
epochs_folder = data_path + "epoched_data/"
tf_folder = data_path + "tf_data/"
mne_folder = data_path + "minimum_norm/"


subjects = ["0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011",
            "0012", "0013", "0014", "0015", "0016", "0017", "0020", "0021",
            "0022", "0023", "0024", "0025"]  # subject to run
