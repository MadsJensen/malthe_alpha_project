# -*- coding: utf-8 -*-
"""
Script that load the DataFrame and do epoch sorting based on that.
@author: mje
"""

import mne
import pandas as pd
import sys
from mne.io import Raw

from my_settings import *

tmin, tmax = -0.5, 2  #Epoch time

subject = sys.argv[1]

# All the behavioral results
results = pd.read_csv(log_folder + "results_all.csv")
# select only the relevant subject
log_tmp = results[results.subject == int(subject)].reset_index()

include = []
raw = Raw(save_folder + "%s_filtered_ica_mc_raw_tsss.fif" % subject,
          preload=False)
# Select events to extract epochs from.
event_id = {"all_trials": 99}

#   Setup for reading the raw data
events = mne.find_events(raw, min_duration=0.015)
events = mne.event.merge_events(events, [1, 2, 4, 8], 99, replace_events=False)

picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=False, eog=False,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                    baseline=(None, 0), reject=None, preload=True)

for i, row in log_tmp.iterrows():
    if row.condition_type == "ctl":
        epoch_name = "ctl"
        epoch_id = "1"
    elif row.condition_type == "ent":
        epoch_name = "ent"
        epoch_id = "2"

    if row.condition_side == "left":
        epoch_name = epoch_name + "/" + "left"
        epoch_id = epoch_id + "1"
    elif row.condition_side == "right":
        epoch_name = epoch_name + "/" + "right"
        epoch_id = epoch_id + "0"

    epoch_name = epoch_name + "/" + str(row.PAS)
    epoch_id = epoch_id + str(row.PAS)

    tmp_epoch = epochs[i].copy()
    tmp_epoch.event_id = {epoch_name: int(epoch_id)}
    tmp_epoch.events = mne.event.merge_events(tmp_epoch.events, [99],
                                              int(epoch_id),
                                              replace_events=True)

    if i == 0:
        all_epochs = tmp_epoch
    else:
        all_epochs = mne.concatenate_epochs([all_epochs, tmp_epoch])


all_epochs.save(epochs_folder + "%-epo.fif" % subject, overwrite=True)
