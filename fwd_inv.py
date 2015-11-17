"""
Doc string goes here.

@author: mje mads [] cnru.dk
"""


import socket
import mne
from mne.minimum_norm import make_inverse_operator
import os
import numpy as np

# SETUP PATHS AND PREPARE RAW DATA
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    # data_path = "/home/mje/Projects/malthe_alpha_project/data/"
    # data_path = "/home/mje/mnt/scratch/MINDLAB2015_MEG-CorticalAlphaAttention/"
else:
    data_path = "/projects/" + \
                "projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

# CHANGE DIR TO SAVE FILES THE RIGTH PLACE
os.chdir(data_path)

subjects_dir = data_path + "fs_subjects_dir/"

raw_fname = data_path + "subj_2_filter_ica-mc_raw_tsss.fif"
bem = mne.read_bem_solution(subjects_dir + "/0002/bem/" +
                            "subj_2-5120-5120-5120-bem-sol.fif")

# src = mne.setup_source_space("0002",
#                              "subj_2-oct6-src.fif",
#                              spacing="oct6",
#                              subjects_dir=subjects_dir,
#                              n_jobs=2)
src = mne.read_source_spaces(data_path + "subj_2-oct6-src.fif")

# fwd = mne.make_forward_solution(raw_fname, trans=None,
#                                 src=src,
#                                 bem=bem,
#                                 meg=True,
#                                 eeg=True,
#                                 fname="subj_2-fwd.fif")

fwd = mne.read_forward_solution("subj_2-fwd.fif")

raw = mne.io.Raw(raw_fname, preload=False)

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12,  # T (magnetometers)
              eeg=180e-6,  # uV (EEG channels)
              )

# SET PARAMETERS
tmin, tmax = -0.5, 1.5

# SELECT EVENTS TO EXTRACT EPOCHS FROM.True
event_id = {'ent_left': 1,
            'ent_right': 2,
            'ctl_left': 4,
            'ctl_right': 8}

# Setup for reading the raw data
# events = mne.read_events("subj_2_filter_ica-mc_raw_tsss-eve.fif")

# events = mne.find_events(raw, stim_channel="STI101",
#                          consecutive="increasing")

# HACK!! to fix short triggers!
eve1 = mne.read_events("subj_2_filter_ica-mc_raw_tsss-eve.fif")
eve2 = mne.read_events("subj_2_filter_ica-mc_raw_tsss-1-eve.fif")
eve3 = mne.read_events("subj_2_filter_ica-mc_raw_tsss-2-eve.fif")

eve1_cln = eve1[eve1[:, 2] <= 8]
eve2_cln = eve2[eve2[:, 2] <= 8]
eve3_cln = eve3[eve3[:, 2] <= 8]

events_all_cln = np.vstack([eve1_cln, eve2_cln, eve3_cln])

raw.info["bads"] = ["EEG039", "EEG040", "EEG052"]
picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=False,
                       eog=False,
                       include=[], exclude='bads')


# Read epochs
epochs = mne.Epochs(raw, events_all_cln, event_id, tmin, tmax, picks=picks,
                    baseline=(None, -0.5), reject=reject,
                    preload=True)

epochs.save("subj_2-epo.fif")

# Make evoked data
evokeds = [epochs[cond].average() for cond in epochs.event_id.keys()]
mne.write_evokeds("subj_2-ave.fif", evokeds)

cov = mne.compute_covariance(epochs, tmin=None, tmax=-0.01,
                             method="auto")

cov.save("subj_2-cov.fif")


# REGULARIZE NOISE COVARIANCE
inv = make_inverse_operator(epochs.info, fwd, cov,
                            loose=0.2, depth=0.8)

mne.minimum_norm.write_inverse_operator("subj_2-inv.fif", inv)
