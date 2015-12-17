"""
Time-frequency analysis.

something here

"""
# Authors: mje mads [] cnru.dk

import numpy as np
import matplotlib.pyplot as plt
import socket
import os
import glob

import mne
from mne.time_frequency import tfr_morlet

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

save_folder = data_path + "filter_ica_data/"
maxfiltered_folder = data_path + "maxfiltered_data/"
epochs_folder = data_path + "epoched_data/"


###############################################################################
# Set parameters
freqs = np.arange(6, 16, 1)  # define frequencies of interest
n_cycles = 4  # freqs / 2.  # different number of cycle per frequency

###############################################################################
# Calculate power and intertrial coherence

os.chdir(epochs_folder)
subjects = glob.glob("*_filtered_ica_mc_raw_tsss.fif")
subjects = [sub[:4] for sub in subjects]
subjects.sort()


def compute_tf(epochs):
    """Function to compute time-frequency decomposition.

    params:
    subject : str
        the subject id to be loaded
    """
    # epochs = mne.read_epochs(epochs_folder +
    #                          "%s_filtered_ica_mc_tsss-epo.fif" % subject)
    power, itc = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles,
                            use_fft=True,
                            return_itc=True, decim=2, n_jobs=1)

    return power, itc


for sub in subjects:
    exec("power_%s, itc_%s = compute_tf(%s)" % (sub, sub, sub))



# Baseline correction can be applied to power or done in plots
# To illustrate the baseline correction in plots the next line is commented
# power.apply_baseline(baseline=(-0.5, 0), mode='logratio')

# Inspect power
power.plot_topo(baseline=(-0.5, 0), mode='logratio', title='Average power')
power.plot([82], baseline=(-0.5, 0), mode='logratio')

fig, axis = plt.subplots(1, 2, figsize=(7, 4))
power.plot_topomap(ch_type='grad', tmin=0.5, tmax=1.5, fmin=8, fmax=12,
                   baseline=(-0.5, 0), mode='logratio', axes=axis[0],
                   title='Alpha', vmax=0.45)
power.plot_topomap(ch_type='grad', tmin=0.5, tmax=1.5, fmin=13, fmax=25,
                   baseline=(-0.5, 0), mode='logratio', axes=axis[1],
                   title='Beta', vmax=0.45)
mne.viz.tight_layout()

# Inspect ITC
itc.plot_topo(title='Inter-Trial coherence', vmin=0., vmax=1., cmap='Reds')


# for subject in subjects:
#     compute_tf(subject)
