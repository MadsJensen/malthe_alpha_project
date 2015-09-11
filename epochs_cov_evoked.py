"""

==============================================================
Extract epochs, estimate noise covariance matrix fvrom epochs,
average and save evoked response to disk
==============================================================
"""
import mne
import socket

from mne import compute_covariance

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    n_jobs = 1


raw = mne.io.Raw(data_path + "0001_p_03_filter_ds_ica-mc_raw_tsss.fif",
                 preload=True)

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12  # T (magnetometers)
              # eeg=180e-6 #
              )

####
# Set parameters
tmin, tmax = -0.5, 2

# Select events to extract epochs from.
event_id = {'ent_left': 1,
            'ent_right': 2,
            'ctl_left': 4,
            'ctl_right': 8}

#   Setup for reading the raw data
events = mne.find_events(raw)

#   Plot raw data
fig = raw.plot(events=events, event_color={1: 'cyan', 2: 'blue',
                                           4: "green", 8: "yellow"})

#   Set up pick list: EEG + STI 014 - bad channels (modify to your needs)
include = []  # or stim channels ['STI 014']
# raw.info['bads'] += ['EEG 053']  # bads + 1 more

# pick EEG and MEG channels
picks = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=True,
                       include=include, exclude='bads')
# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                    baseline=(None, 0), reject=reject,
                    preload=True)

epochs.save("0001_p_03_filter_ds_ica-mc_tsss-epo.fif")

# Plot epochs.
epochs.plot(trellis=False)

# Look at channels that caused dropped events, showing that the subject's
# blinks were likely to blame for most epochs being dropped
epochs.drop_bad_epochs()
epochs.plot_drop_log(subject='0001')

# Make noise cov
cov = compute_covariance(epochs, tmin=None, tmax=0, method="auto")

mne.write_cov("0001-cov.fif", cov)

# Average epochs and get evoked data corresponding to the left stimulation
###############################################################################
# Save evoked responses for different conditions to disk

# average epochs and get Evoked datasets
evokeds = [epochs[cond].average() for cond in ['ent_left', 'ent_right',
                                               'ctl_left', 'ctl_right']]

# save evoked data to disk
mne.write_evokeds('0001_p_03_filter_ds_ica-mc_raw_tsss-ave.fif', evokeds)
