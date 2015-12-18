"""
Time-frequency analysis.

something here

"""
# Authors: mje mads [] cnru.dk
import cPickle as pickle
import glob
import os
import socket

import matplotlib.pyplot as plt
import mne
import numpy as np
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
tf_folder = data_path + "tf_data/"

###############################################################################
# Set parameters
freqs = np.arange(6, 16, 1)  # define frequencies of interest
n_cycles = 4  # freqs / 2.  # different number of cycle per frequency

###############################################################################
# Calculate power and intertrial coherence

os.chdir(epochs_folder)
subjects = glob.glob("*_filtered_ica_mc_tsss-epo.fif")
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


power_ent_left = []
itc_ent_left = []
power_ent_right = []
itc_ent_right = []
power_ctl_left = []
itc_ctl_left = []
power_ctl_right = []
itc_ctl_right = []

for sub in subjects:
    epochs = mne.read_epochs("%s_filtered_ica_mc_tsss-epo.fif" % sub)
    for cond in epochs.event_id.keys():
        exec("power_%s, itc_%s = compute_tf(epochs[\"%s\"])"
             % (sub, sub, cond))
        exec("power_%s.append(power_%s)" % (cond, sub))
        exec("itc_%s.append(itc_%s)" % (cond, sub))


os.chdir(tf_folder)
# save power list
pickle.dump(power_ent_left, open("power_ent_left.p", "wb"))
pickle.dump(power_ent_right, open("power_ent_right.p", "wb"))
pickle.dump(power_ctl_right, open("power_ctl_right.p", "wb"))
pickle.dump(power_ctl_left, open("power_ctl_left.p", "wb"))

# save ITC list
pickle.dump(itc_ent_left, open("itc_ent_left.p", "wb"))
pickle.dump(itc_ent_right, open("itc_ent_right.p", "wb"))
pickle.dump(itc_ctl_right, open("itc_ctl_right.p", "wb"))
pickle.dump(itc_ctl_left, open("itc_ctl_left.p", "wb"))

# apply baseline
sides = ["left", "right"]
conditions = ["ent", "ctl"]

for side in sides:
    for condition in conditions:
        exec("[tf.apply_baseline((None, 0), mode=\"zscore\") \
            for tf in power_%s_%s]" % (condition, side))


times = power_ctl_left[0].times * 1e3  # to get miliseconds
occ_r = mne.read_selection("Right-occipital")
occ_l = mne.read_selection("Left-occipital")
occ_r = [o[:3] + o[4:] for o in occ_r]
occ_l = [o[:3] + o[4:] for o in occ_l]

power_ent_left_sel = [pow.pick_channels(occ_r, copy=True) for
                      pow in power_ent_left]
power_ctl_left_sel = [pow.pick_channels(occ_r, copy=True) for
                      pow in power_ctl_left]
power_ent_right_sel = [pow.pick_channels(occ_r, copy=True) for
                       pow in power_ent_right]
power_ctl_right_sel = [pow.pick_channels(occ_r, copy=True) for
                       pow in power_ctl_right]


mp_ent_left_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                   pow in power_ent_left_sel], axis=1), axis=1)
mp_ctl_left_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                   pow in power_ctl_left_sel], axis=1), axis=1)
mp_ent_right_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                    pow in power_ent_right_sel], axis=1),
                           axis=1)
mp_ctl_right_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                    pow in power_ctl_right_sel], axis=1),
                           axis=1)

plt.figure()
plt.plot(times, mp_ent_right_sel.mean(axis=0), 'm',
         label="ent_right", linewidth=3)
plt.plot(times, mp_ctl_right_sel.mean(axis=0), 'k',
         label="ctl_right", linewidth=3)
plt.plot(times, mp_ctl_left_sel.mean(axis=0), 'b',
         label="ctl_left", linewidth=3)
plt.plot(times, mp_ent_left_sel.mean(axis=0), 'r',
         label="ent_left", linewidth=3)
plt.legend()
plt.title("Power: Right occ sensors")
plt.xlabel("time (in ms)")
plt.ylabel("Power value")
plt.savefig(tf_folder + "pics/power_right_occ_sens.png")


power_ent_left_sel = [pow.pick_channels(occ_l, copy=True) for
                      pow in power_ent_left]
power_ctl_left_sel = [pow.pick_channels(occ_l, copy=True) for
                      pow in power_ctl_left]
power_ent_right_sel = [pow.pick_channels(occ_l, copy=True) for
                       pow in power_ent_right]
power_ctl_right_sel = [pow.pick_channels(occ_l, copy=True) for
                       pow in power_ctl_right]


mp_ent_left_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                   pow in power_ent_left_sel], axis=1), axis=1)
mp_ctl_left_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                   pow in power_ctl_left_sel], axis=1), axis=1)
mp_ent_right_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                    pow in power_ent_right_sel], axis=1),
                           axis=1)
mp_ctl_right_sel = np.mean(np.mean([pow.data[:, 2:-3, :] for
                                    pow in power_ctl_right_sel], axis=1),
                           axis=1)

plt.figure()
plt.plot(times, mp_ent_right_sel.mean(axis=0), 'm',
         label="ent_right", linewidth=3)
plt.plot(times, mp_ctl_right_sel.mean(axis=0), 'k',
         label="ctl_right", linewidth=3)
plt.plot(times, mp_ctl_left_sel.mean(axis=0), 'b',
         label="ctl_left", linewidth=3)
plt.plot(times, mp_ent_left_sel.mean(axis=0), 'r',
         label="ent_left", linewidth=3)
plt.legend()
plt.title("Power: Left occ sensors")
plt.xlabel("time (in ms)")
plt.ylabel("Power")
plt.savefig(tf_folder + "pics/power_left_occ_sens.png")


# ITC plots
itc_ent_left_sel = [itc.pick_channels(occ_r, copy=True) for
                    itc in itc_ent_left]
itc_ctl_left_sel = [itc.pick_channels(occ_r, copy=True) for
                    itc in itc_ctl_left]
itc_ent_right_sel = [itc.pick_channels(occ_r, copy=True) for
                     itc in itc_ent_right]
itc_ctl_right_sel = [itc.pick_channels(occ_r, copy=True) for
                     itc in itc_ctl_right]


mp_ent_left_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                   itc in itc_ent_left_sel], axis=1), axis=1)
mp_ctl_left_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                   itc in itc_ctl_left_sel], axis=1), axis=1)
mp_ent_right_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                    itc in itc_ent_right_sel], axis=1), axis=1)
mp_ctl_right_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                    itc in itc_ctl_right_sel], axis=1), axis=1)

plt.figure()
plt.plot(times, mp_ent_right_sel.mean(axis=0), 'm',
         label="ent_right", linewidth=3)
plt.plot(times, mp_ctl_right_sel.mean(axis=0), 'k',
         label="ctl_right", linewidth=3)
plt.plot(times, mp_ctl_left_sel.mean(axis=0), 'b',
         label="ctl_left", linewidth=3)
plt.plot(times, mp_ent_left_sel.mean(axis=0), 'r',
         label="ent_left", linewidth=3)
plt.legend()
plt.title("ITC: Right occ sensors")
plt.xlabel("time (in ms)")
plt.ylabel("ITC value")
plt.savefig(tf_folder + "pics/itc_right_occ_sens.png")

itc_ent_left_sel = [itc.pick_channels(occ_l, copy=True) for
                    itc in itc_ent_left]
itc_ctl_left_sel = [itc.pick_channels(occ_l, copy=True) for
                    itc in itc_ctl_left]
itc_ent_right_sel = [itc.pick_channels(occ_l, copy=True) for
                     itc in itc_ent_right]
itc_ctl_right_sel = [itc.pick_channels(occ_l, copy=True) for
                     itc in itc_ctl_right]


mp_ent_left_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                   itc in itc_ent_left_sel], axis=1), axis=1)
mp_ctl_left_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                   itc in itc_ctl_left_sel], axis=1), axis=1)
mp_ent_right_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                    itc in itc_ent_right_sel], axis=1), axis=1)
mp_ctl_right_sel = np.mean(np.mean([itc.data[:, 2:-3, :] for
                                    itc in itc_ctl_right_sel], axis=1), axis=1)

plt.figure()
plt.plot(times, mp_ent_right_sel.mean(axis=0), 'm',
         label="ent_right", linewidth=3)
plt.plot(times, mp_ctl_right_sel.mean(axis=0), 'k',
         label="ctl_right", linewidth=3)
plt.plot(times, mp_ctl_left_sel.mean(axis=0), 'b',
         label="ctl_left", linewidth=3)
plt.plot(times, mp_ent_left_sel.mean(axis=0), 'r',
         label="ent_left", linewidth=3)
plt.legend()
plt.title("ITC: Left occ sensors")
plt.xlabel("time (in ms)")
plt.ylabel("ITC value")
plt.savefig(tf_folder + "pics/itc_left_occ_sens.png")
