"""
Extract epochs.

Estimate noise covariance matrix fom epochs,
average and save evoked response to disk
==============================================================
"""
import mne
import socket
import os
import glob

from mne import compute_covariance
from mne.io import Raw

import matplotlib
matplotlib.use('Agg')

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"

save_folder = data_path + "filter_ica_data/"
maxfiltered_folder = data_path + "maxfiltered_data/"
epochs_folder = data_path + "epoched_data/"


reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12,  # T (magnetometers)
              eeg=180e-6  #
              )

####
# Set parameters
tmin, tmax = -0.5, 2

#   Plot raw data
# fig = raw.plot(events=events, event_color={ 21: 'cyan', 22: 'blue',
#                                           23: "green", 24: "yellow"})

# for j in range(len(events)):
#     if events[j, 2] == 1 and events[j+3, 2] == 21:
#         events[j, 2] = 40
#     elif events[j, 2] == 1 and events[j+3, 2] == 22:
#         events[j, 2] = 41
#     elif events[j, 2] == 1 and events[j+3, 2] == 23:
#         events[j, 2] = 42
#     elif events[j, 2] == 2 and events[j+3, 2] == 21:
#         events[j, 2] = 45
#     elif events[j, 2] == 2 and events[j+3, 2] == 22:
#         events[j, 2] = 46
#     elif events[j, 2] == 2 and events[j+3, 2] == 23:
#         events[j, 2] = 47
#     elif events[j, 2] == 4 and events[j+3, 2] == 21:
#         events[j, 2] = 50
#     elif events[j, 2] == 4 and events[j+3, 2] == 22:
#         events[j, 2] = 51
#     elif events[j, 2] == 4 and events[j+3, 2] == 23:
#         events[j, 2] = 52
#     elif events[j, 2] == 8 and events[j+3, 2] == 21:
#         events[j, 2] = 55
#     elif events[j, 2] == 8 and events[j+3, 2] == 22:
#         events[j, 2] = 56
#     elif events[j, 2] == 8 and events[j+3, 2] == 23:
#         events[j, 2] = 57

# event_id = {'ent_left_pas_1': 40,
#             'ent_left_pas_2': 41,
#             'ent_left_pas_3': 42,
#             'ent_right_pas_1': 45,
#             'ent_right_pas_2': 46,
#             'ent_right_pas_3': 47,
#             'ctl_left_pas_1': 50,
#             'ctl_left_pas_2': 51,
#             'ctl_left_pas_3': 52,
#             'ctl_right_pas_1': 55,
#             'ctl_right_pas_2': 56,
#             'ctl_right_pas_3': 57}


#   Set up pick list: EEG + STI 014 - bad channels (modify to your needs)
include = []  # or stim channels ['STI 014']
# raw.info['bads'] += ['EEG 053']  # bads + 1 more

# pick EEG and MEG channels


def compute_epochs_cov_evokeds(subject):
    """Epoch, compute noise covariance and average.

    params:
    subject : str
        the subject id to be loaded
    """
    raw = Raw(save_folder + "%s_filtered_ica_mc_raw_tsss.fif" % subject,
              preload=True)
    # Select events to extract epochs from.
    event_id = {'ent_left': 1,
                'ent_right': 2,
                'ctl_left': 4,
                'ctl_right': 8}

    #   Setup for reading the raw data
    events = mne.find_events(raw, min_duration=0.01)

    picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=False, eog=False,
                           include=include, exclude='bads')
    # Read epochs
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                        baseline=(None, 0), reject=reject,
                        preload=True)

    epochs.save(epochs_folder + "%s_filtered_ica_mc_tsss-epo.fif" % subject)

    # Plot epochs.
    # epochs.plot(trellis=False)

    # Look at channels that caused dropped events, showing that the subject's
    # blinks were likely to blame for most epochs being dropped
    epochs.drop_bad_epochs()
    fig = epochs.plot_drop_log(subject=subject, show=False)
    fig.savefig(epochs_folder + "pics/%s_drop_log.png" % subject)

    # Make noise cov
    cov = compute_covariance(epochs, tmin=None, tmax=0, method="auto")
    mne.write_cov(epochs_folder + "%s-cov.fif" % subject, cov)

    # Average epochs and get evoked data corresponding to the left stimulation
    ###########################################################################
    # Save evoked responses for different conditions to disk

    # average epochs and get Evoked datasets
    evokeds = [epochs[cond].average() for cond in ['ent_left', 'ent_right',
                                                   'ctl_left', 'ctl_right']]

    evokeds = [epochs[cond].average() for cond in epochs.event_id.keys()]

    # save evoked data to disk
    mne.write_evokeds(epochs_folder +\
        '%s_filtered_ica_mc_raw_tsss-ave.fif' % subject, evokeds)


os.chdir(save_folder)
subjects = glob.glob("*_filtered_ica_mc_raw_tsss.fif")
subjects = [sub[:4] for sub in subjects]
subjects.sort()

for subject in subjects:
    compute_epochs_cov_evokeds(subject)
