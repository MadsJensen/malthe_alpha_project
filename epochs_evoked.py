"""
========================================================
Extract epochs, average and save evoked response to disk
========================================================

This script shows how to read the epochs from a raw file given
a list of events. The epochs are averaged to produce evoked
data and then saved to disk.

"""
# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Denis A. Engemann <denis.engemann@gmail.com>
#
# License: BSD (3-clause)

import mne
from mne import io
import socket

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/Hyp_meg/scratch/Tone_task_MNE/"
    n_jobs = 1
elif hostname == "isis":
    data_path = "/projects/MINDLAB2015_MEG-Gambling/scratch/"
    n_jobs = 3


raw = mne.io.Raw(data_path + "p_01_data_ica_filter_resample_tsss_raw.fif",
          preload=True)

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12,  # T (magnetometers)
              eeg=180e-6 #
              )

####
# Set parameters
tmin, tmax = -0.2, 0.4

# Select events to extract epochs from.
event_id = {'entrainment': 1,
            'Control': 2,
            'left': 4,
            'right': 8}

#   Setup for reading the raw data
raw = io.Raw(raw_fname)
events = mne.find_events(raw)

#   Plot raw data
fig = raw.plot(events=events, event_color={1: 'cyan', -1: 'lightgray'})

#   Set up pick list: EEG + STI 014 - bad channels (modify to your needs)
include = []  # or stim channels ['STI 014']
# raw.info['bads'] += ['EEG 053']  # bads + 1 more

# pick EEG and MEG channels
picks = mne.pick_types(raw.info, meg=True, eeg=True, stim=False, eog=True,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                    baseline=(None, 0), reject=dict(eeg=80e-6, eog=150e-6),
                    preload=True)

# Plot epochs.
epochs.plot(trellis=False, title='Auditory left/right')

# Look at channels that caused dropped events, showing that the subject's
# blinks were likely to blame for most epochs being dropped
epochs.drop_bad_epochs()
epochs.plot_drop_log(subject='sample')

# Average epochs and get evoked data corresponding to the left stimulation
evoked = epochs['Left'].average()

evoked.save('sample_audvis_eeg-ave.fif')  # save evoked data to disk

###############################################################################
# View evoked response

evoked.plot()

###############################################################################
# Save evoked responses for different conditions to disk

# average epochs and get Evoked datasets
evokeds = [epochs[cond].average() for cond in ['Left', 'Right']]

# save evoked data to disk
mne.write_evokeds('sample_auditory_and_visual_eeg-ave.fif', evokeds)
o