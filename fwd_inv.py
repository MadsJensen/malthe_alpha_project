"""
Doc string goes here.

@author: mje mads [] cnru.dk
"""


import socket
import mne
from mne.minimum_norm import make_inverse_operator
import os
import subprocess

cmd = "/usr/local/common/meeg-cfin/configurations/bin/submit_to_isis"

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


subjects = ["0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011",
            "0012", "0013", "0014", "0015", "0016", "0017", "0020", "0021",
            "0022", "0023", "0024", "0025"]  # subject to run

os.chdir(mne_folder)
bem_list = glob.glob("*8192-8192*sol.fif")
# bem_list = !ls *8192-8192*sol.fif

subjects = ["0004", "0005"]

# Setup source space and forward model
for j, sub in enumerate(subjects):
    raw_fname = save_folder + "%s_filtered_ica_mc_raw_tsss.fif" % sub
    trans_fname = mne_folder + "%s-trans.fif" % sub
    bem = bem_list[j]
    cov = mne.read_cov(mne_folder + "%s-cov.fif" % sub)
#    cov = cov[0]

    src = mne.setup_source_space(sub,
                                 mne_folder + "%s-oct6-src.fif" % sub,
                                 spacing="oct6",
                                 subjects_dir=subjects_dir,
                                 n_jobs=2)  # use a job for each hemispere

    fwd = mne.make_forward_solution(raw_fname, trans=trans_fname,
                                    src=src,
                                    bem=bem,
                                    meg=True,
                                    eeg=True,
                                    fname=mne_folder + "%s-fwd.fif" % sub)


# Calculate covariance matrix
best_fit = []
for sub in subjects[2:]:
    epochs = mne.read_epochs(epochs_folder +
                             "%s_filtered_ica_mc_tsss-epo.fif" % sub)
    cov = mne.compute_covariance(epochs, tmin=None, tmax=-0.01,
                                 method="auto", return_estimators="all")
    best_fit.append({"method": cov[0]["method"], "loglik": cov[0]["loglik"]})
    cov = cov[0]
    cov.save(mne_folder + "%s-cov.fif" % sub, overwrite=True)


# Make inverse model
for sub in subjects:
    fwd = mne.read_forward_solution(mne_folder + "%s-fwd.fif" % sub)
    cov = mne.read_cov(mne_folder + "%s-cov.fif" % sub)
    epochs = mne.read_epochs(epochs_folder +\
                            "%s_filtered_ica_mc_tsss-epo.fif" % sub)
    inv = make_inverse_operator(epochs.info, fwd, cov,
                                loose=0.2, depth=0.8)

    mne.minimum_norm.write_inverse_operator(mne_folder + "%s-inv.fif" % sub,
                                            inv)
