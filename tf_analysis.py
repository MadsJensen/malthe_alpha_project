"""
Time-frequency analysis.

something here

"""
# Authors: mje mads [] cnru.dk
import mne
import numpy as np

from my_settings import *
from tf_analyses_functions import calc_power


conditions = ["ctl_left", "ctl_right", "ent_left", "ent_right"]

for subject in subjects:
    epochs = mne.read_epochs(epochs_folder +
                             "%s_ds_filtered_ica_mc_tsss-epo.fif" % subject)
    for condition in conditions:
        power, itc = calc_power(epochs, condition=condition, save=True)
