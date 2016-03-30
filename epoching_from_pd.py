# -*- coding: utf-8 -*-
"""
Script that load the DataFrame and do epoch sorting based on that.
@author: mje
"""

import mne
import pandas as pd
import numpy as np
import sys
from mne.io import Raw

from my_settings import *

tmin, tmax = -0.5, 1.5  # Epoch time

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
events = mne.event.merge_events(events, [1, 2, 4, 8], 99, replace_events=True)


event_id = {}
epoch_ids = []
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

    if row.congruent is True:
        epoch_name = epoch_name + "/" + "cong"
        epoch_id = epoch_id + "1"
    elif row.congruent is False:
        epoch_name = epoch_name + "/" + "incong"
        epoch_id = epoch_id + "0"

    if row.correct is True:
        epoch_name = epoch_name + "/" + "correct"
        epoch_id = epoch_id + "1"
    elif row.correct is False:
        epoch_name = epoch_name + "/" + "incorrect"
        epoch_id = epoch_id + "0"

    if row.in_phase is True:
        epoch_name = epoch_name + "/" + "in_phase"
        epoch_id = epoch_id + "1"
    elif row.in_phase is False:
        epoch_name = epoch_name + "/" + "out_phase"
        epoch_id = epoch_id + "0"

    epoch_name = epoch_name + "/" + str(row.PAS)
    epoch_id = epoch_id + str(row.PAS)
    epoch_ids.append(int(epoch_id))

    if epoch_name is not event_id:
        event_id[str(epoch_name)] = int(epoch_id)


idx = np.arange(0, len(events), 4)
for i in range(len(events[idx])):
    events[idx[i]][2] = epoch_ids[i]


picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=False, eog=False,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                    baseline=(None, -0.2), reject=None, preload=False)

epochs.save(epochs_folder + "%s_trial_start-epo.fif" % subject)
