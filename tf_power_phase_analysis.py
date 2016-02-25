"""
"""

import numpy as np
import matplotlib.pyplot as plt
import socket
import os

import mne
from mne.minimum_norm import read_inverse_operator, source_induced_power

###############################################################################
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


# Compute a source estimate per frequency band including and excluding the
# evoked response
frequencies = np.arange(6, 90, 3)  # define frequencies of interest
n_cycles = frequencies / 3.  # different number of cycle per frequency

subject = "0005"

# TODO: insert loop here

# subtract the evoked response in order to exclude evoked activity
epochs = mne.read_epochs(epochs_folder +
                         "%s_filtered_ica_mc_tsss-epo.fif" % subject)
epochs = epochs["ent_left", "ctl_left"]
epochs.crop(None, 0.8)
epochs.resample(500)
# epochs_clt_left = epochs["ctl_left"].copy()
# ind_ent_left = epochs["ent_left"].copy().subtract_evoked()
# ind_clt_left = epochs["ctl_left"].copy().subtract_evoked()
# ind_clt_left = epochs_clt_left.copy().subtract_evoked()

inverse_operator = read_inverse_operator(mne_folder + "%s-inv.fif" % subject)
labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Lobes',
                                    # regexp="Bro",
                                    subjects_dir=subjects_dir)
label = labels[9]


for cond in ["ent_left", "ctl_left"]:
        # compute the source space power and phase lock
    power, phase_lock = source_induced_power(
        epochs[cond], inverse_operator, frequencies, label, baseline=(-0.3, 0.),
        baseline_mode="percent", n_cycles=n_cycles, n_jobs=1, pca=True)

    exec("power_%s = np.mean(power, axis=0)" % cond)  # average over sources
    exec("phase_lock_%s = np.mean(phase_lock, axis=0)" % cond)  # average over sources
    times = epochs.times
    power = np.mean(power, axis=0)
    phase_lock = np.mean(phase_lock, axis=0)

    ##########################################################################
    # View time-frequency plots
    plt.figure()
    plt.imshow(20 * power,
               extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
               aspect='auto', origin='lower', vmin=0., vmax=None, cmap='hot')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Power (%s)' % (cond,))
    plt.colorbar()
    plt.show()

    plt.figure()
    plt.imshow(phase_lock,
               extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
               aspect='auto', origin='lower', vmin=0, vmax=None,
               cmap='hot')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Phase-lock (%s)' % (cond))
    plt.colorbar()
    plt.show()


diff_phase = phase_lock_ctl_left - phase_lock_ent_left
diff_power = power_ctl_left - power_ent_left

plt.figure()
plt.imshow(diff_power,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', vmin=None, vmax=None, cmap='RdBu_r')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Power (%s)' % ("Difference"))
plt.colorbar()
plt.show()

plt.figure()
plt.imshow(diff_phase,
           extent=[times[0], times[-1], frequencies[0], frequencies[-1]],
           aspect='auto', origin='lower', vmin=None, vmax=None,
           cmap='RdBu_r')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Phase-lock (%s)' % ("Difference"))
plt.colorbar()
plt.show()
