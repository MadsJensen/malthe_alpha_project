# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:17:09 2015

@author: mje
"""
import mne
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator,
                              source_induced_power, source_band_induced_power,
                              compute_source_psd_epochs, apply_inverse)

import socket
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns

import socket
import mne
from mne.minimum_norm import make_inverse_operator
import os
# import subprocess
import glob

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

# Using the same inverse operator when inspecting single trials Vs. evoked
snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2

method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

# Plot evoked
# right ctl, left ent & diff
mne.viz.plot_evoked_topo([evokeds[2], evokeds[0]],
                         color=['r', 'g'])

# topoplot all conditions
colors = "blue", "green", 'red', 'm'
mne.viz.plot_evoked_topo([evokeds[0], evokeds[1], evokeds[2], evokeds[3]],
                         color=colors)

conditions = [e.comment for e in evokeds]
for cond, col, pos in zip(conditions, colors, (0.02, 0.07, 0.12, 0.17)):
    plt.figtext(0.97, pos, cond, color=col, fontsize=12,
                horizontalalignment='right')


# Get evoked data (averaging across trials in sensor space)

# Compute inverse solution and stcs for each epoch
# Use the same inverse operator as with evoked data (i.e., set nave)
# If you use a different nave, dSPM just scales by a factor sqrt(nae)

    for cond in epochs.event_id.keys():
        stcs = apply_inverse_epochs(epochs[cond], inverse_operator, lambda2,
                                    method, pick_ori="normal")
        exec("stcs_%s = stcs" % cond)


snr = 3.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)


for subject in subjects:
    # Load data
    fname_inv = mne_folder + "%s-inv.fif" % subject
    fname_evoked = epochs_folder + "%s_filtered_ica_mc_tsss-ave.fif" % subject
    inverse_operator = read_inverse_operator(fname_inv)
    evokeds = mne.read_evokeds(fname_evoked, baseline=(None, 0))

    for evk in evokeds:
        stc = apply_inverse(evk, inverse_operator, lambda2=lambda2,
                            method=method, pick_ori="normal")
        exec("stc_%s_%s = stc" % (subject, evk.comment))


ctl_left = [stc_0004_ctl_left, stc_0005_ctl_left, stc_0006_ctl_left,
            stc_0007_ctl_left, stc_0008_ctl_left, stc_0009_ctl_left,
            stc_0010_ctl_left, stc_0011_ctl_left, stc_0012_ctl_left,
            stc_0013_ctl_left, stc_0014_ctl_left, stc_0015_ctl_left,
            stc_0016_ctl_left, stc_0017_ctl_left, stc_0020_ctl_left,
            stc_0021_ctl_left, stc_0022_ctl_left, stc_0023_ctl_left,
            stc_0024_ctl_left, stc_0025_ctl_left]


ent_left = [stc_0004_ent_left, stc_0005_ent_left, stc_0006_ent_left,
            stc_0007_ent_left, stc_0008_ent_left, stc_0009_ent_left,
            stc_0010_ent_left, stc_0011_ent_left, stc_0012_ent_left,
            stc_0013_ent_left, stc_0014_ent_left, stc_0015_ent_left,
            stc_0016_ent_left, stc_0017_ent_left, stc_0020_ent_left,
            stc_0021_ent_left, stc_0022_ent_left, stc_0023_ent_left,
            stc_0024_ent_left, stc_0025_ent_left]

ctl_right = [stc_0004_ctl_right, stc_0005_ctl_right, stc_0006_ctl_right,
             stc_0007_ctl_right, stc_0008_ctl_right, stc_0009_ctl_right,
             stc_0010_ctl_right, stc_0011_ctl_right, stc_0012_ctl_right,
             stc_0013_ctl_right, stc_0014_ctl_right, stc_0015_ctl_right,
             stc_0016_ctl_right, stc_0017_ctl_right, stc_0020_ctl_right,
             stc_0021_ctl_right, stc_0022_ctl_right, stc_0023_ctl_right,
             stc_0024_ctl_right, stc_0025_ctl_right]


ent_right = [stc_0004_ent_right, stc_0005_ent_right, stc_0006_ent_right,
             stc_0007_ent_right, stc_0008_ent_right, stc_0009_ent_right,
             stc_0010_ent_right, stc_0011_ent_right, stc_0012_ent_right,
             stc_0013_ent_right, stc_0014_ent_right, stc_0015_ent_right,
             stc_0016_ent_right, stc_0017_ent_right, stc_0020_ent_right,
             stc_0021_ent_right, stc_0022_ent_right, stc_0023_ent_right,
             stc_0024_ent_right, stc_0025_ent_right]

lbl_ctl_left = []
lbl_ent_left = []
lbl_ctl_right = []
lbl_ent_right = []

for j in range(len(subjects)):
    src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subjects[j])
    labels = mne.read_labels_from_annot(subjects[j], parc='PALS_B12_Lobes',
                                        # regexp="Bro",
                                        subjects_dir=subjects_dir)
    labels_occ = [labels[9], labels[10]]

    lbl_ent_left.append(mne.extract_label_time_course(ent_left[j],
                                                      labels=labels_occ,
                                                      src=src,
                                                      mode="pca_flip"))

    lbl_ctl_left.append(mne.extract_label_time_course(ctl_left[j],
                                                      labels=labels_occ,
                                                      src=src,
                                                      mode="pca_flip"))

    lbl_ent_right.append(mne.extract_label_time_course(ent_right[j],
                                                       labels=labels_occ,
                                                       src=src,
                                                       mode="pca_flip"))

    lbl_ctl_right.append(mne.extract_label_time_course(ctl_right[j],
                                                       labels=labels_occ,
                                                       src=src,
                                                       mode="pca_flip"))


lbl_ent_left = np.squeeze(np.asarray(lbl_ent_left))
lbl_ctl_left = np.squeeze(np.asarray(lbl_ctl_left))
lbl_ent_right = np.squeeze(np.asarray(lbl_ent_right))
lbl_ctl_right = np.squeeze(np.asarray(lbl_ctl_right))

times = stc_0004_ent_left.times

plt.figure()
plt.plot(times, lbl_ent_left[:, 0, :].mean(axis=0), 'b', label="ent_left")
plt.plot(times, lbl_ent_right[:, 0, :].mean(axis=0), 'g', label="ent_right")
plt.plot(times, lbl_ctl_left[:, 0, :].mean(axis=0), 'r', label="ctl_left")
plt.plot(times, lbl_ctl_right[:, 0, :].mean(axis=0), 'm', label="ctl_right")
plt.legend()
plt.title("label: %s" % labels_occ[0].name)
plt.show()


plt.figure()
plt.plot(times, lbl_ent_left[:, 1, :].mean(axis=0), 'b', label="ent_left")
plt.plot(times, lbl_ent_right[:, 1, :].mean(axis=0), 'g', label="ent_right")
plt.plot(times, lbl_ctl_left[:, 1, :].mean(axis=0), 'r', label="ctl_left")
plt.plot(times, lbl_ctl_right[:, 1, :].mean(axis=0), 'm', label="ctl_right")
plt.legend()
plt.title("label: %s" % labels_occ[1].name)
plt.show()


plt.figure()
plt.plot(times, lbl_ent_left[:, 1, :].T, 'b', label="ent_left")
# plt.plot(times, lbl_ent_right[:, 1, :].mean(axis=0),'g', label="ent_right")
plt.plot(times, lbl_ctl_left[:, 1, :].T, 'r', label="ctl_left")
# plt.plot(times, lbl_ctl_right[:, 1, :].mean(axis=0),'m', label="ctl_right")
plt.legend()
plt.title("label: %s" % labels_occ[1].name)
plt.show()


# for label in labels_occ:
#    plt.figure()
#    plt.plot(times[:425],stc_ctl_left.in_label(label).data.mean(axis=0)[:425],
#             'r', linewidth=2, label="ctl_left")
#    plt.plot(times[:425], stc_ctl_right.in_label(label).data.mean(axis=0)[:425],
#             'm', linewidth=2, label="ctl_right")
#    plt.plot(times[:425], stc_ent_left.in_label(label).data.mean(axis=0)[:425],
#             'b', linewidth=2, label="ent_left")
#    plt.plot(times[:425], stc_ent_right.in_label(label).data.mean(axis=0)[:425],
#             'g', linewidth=2, label="ent_right")
#
#    plt.legend()
#    plt.title("label: %s" % label.name)
#    plt.ylabel("dSPM")
#    plt.xlabel("Time (seconds)")
#    plt.savefig("%s_source_evoked.png" % label.name)
#

for label in labels_occ:
    plt.figure()
#    plt.plot(times[:425], stc_ctl_left_pas_2.in_label(label).data.mean(axis=0),
#             'r', linewidth=2, label="ctl_left_pas_2")
#    plt.plot(times[:425], stc_ctl_right_pas_2.in_label(label).data.mean(axis=0),
#             'm', linewidth=2, label="ctl_right_pas_2")
    plt.plot(times, stc_ent_left_pas_2.in_label(label).data.mean(axis=0),
             'b', linewidth=2, label="ent_left_pas_2")
    plt.plot(times, stc_ent_left_pas_3.in_label(label).data.mean(axis=0),
             'b:', linewidth=2, label="ent_left_pas_3")
    plt.plot(times, stc_ent_right_pas_2.in_label(label).data.mean(axis=0),
             'g', linewidth=2, label="ent_right_pas_2")
    plt.plot(times, stc_ent_left_pas_3.in_label(label).data.mean(axis=0),
             'g:', linewidth=2, label="ent_right_pas_3")

    plt.legend()
    plt.title("label: %s" % label.name)
    plt.ylabel("dSPM")
    plt.xlabel("Time (seconds)")
    plt.savefig("%s_source_evoked.png" % label.name)

# Compute a source estimate per frequency band including and excluding the
# evoked response
frequencies = np.arange(8, 13, 1)  # define frequencies of interest
n_cycles = frequencies / 3.  # different number of cycle per frequency

# subtract the evoked response in order to exclude evoked activity

labels_occ = [labels[10]]

# plt.close('all')
for cond in ["ent_left_pas_3", "ent_left_pas_2"]:  # epochs.event_id.keys():
    for label in labels_occ:
        plt.figure()
        epochs_induced = epochs[cond].copy().subtract_evoked()
        for ii, (this_epochs, title) in enumerate(zip([epochs["ent_left_pas_3",
                                                              "ent_left_pas_2"
                                                              # "ent_right",
                                                              # "ctl_left",
                                                              # "ctl_right"
                                                              ],
                                                       epochs_induced],
                                                      ['evoked + induced',
                                                       'induced only'])):
            # compute the source space power and phase lock
            power, phase_lock = source_induced_power(
                this_epochs, inverse_operator, frequencies, label,
                baseline=(None, 0),
                baseline_mode='zscore', n_cycles=n_cycles, pca=True,
                n_jobs=n_jobs)

            power = np.mean(power, axis=0)  # average over sources
            phase_lock = np.mean(phase_lock, axis=0)  # average over sources
            times = epochs.times

            ###################################################################
            # View time-frequency plots
            plt.subplots_adjust(0.1, 0.08, 0.96, 0.94, 0.2, 0.43)
            plt.subplot(2, 2, 2 * ii + 1)
            plt.imshow(20 * power,
                       extent=[times[60], times[220],
                               frequencies[0], frequencies[-1]],
                       aspect='auto', origin='lower', cmap='RdBu_r')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('Power (%s), condition: %s' % (title, cond))
            plt.colorbar()

            plt.subplot(2, 2, 2 * ii + 2)
            plt.imshow(phase_lock,
                       extent=[times[60], times[260],
                               frequencies[0], frequencies[-1]],
                       aspect='auto', origin='lower',
                       cmap='RdBu_r')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('Phase-lock (%s), cond: %s, label: %s'
                      % (title, cond, label.name))
            plt.colorbar()

            plt.show()


bands = dict(alpha=[8, 12])
snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)


BP_list = []

for subject in subjects:
    # Load data
    fname_inv = mne_folder + "%s-inv.fif" % subject
    epochs = mne.read_epochs(epochs_folder +
                             "%s_filtered_ica_mc_tsss-epo.fif" % subject)
    epochs.resample(500)
    inverse_operator = read_inverse_operator(fname_inv)

    labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Lobes',
                                        # regexp="Bro",
                                        subjects_dir=subjects_dir)

    for j, label in enumerate([labels[9], labels[10]]):
        for cond in epochs.event_id.keys():
            stcs = source_band_induced_power(epochs[cond],
                                             inverse_operator,
                                             bands=bands,
                                             label=label,
                                             lambda2=lambda2,
                                             method=method,
                                             n_cycles=4,
                                             pick_ori="normal",
                                             baseline=None,
                                             # baseline_mode='percent',
                                             pca=True)

            if len(label.name.split()) > 2:
                l_name = label.name.split()[0][5:][:-3] + "_lh_rh"
            else:
                l_name = label.name[5:][:-3] + "_" + label.name[-2:]

            BP_list.append("BP_%s_%s_%s" % (subject, cond, l_name))

            exec("BP_%s_%s_%s = stcs['alpha']" % (subject, cond, l_name))
            stcs["alpha"].save(tf_folder + "BP_%s_%s_%s_%s"
                               % (subject, cond, l_name, method))


# difference waves plots
super_ctl = (BP_ctl_left_OCCIPITAL_lh.data.mean(axis=0) +
             BP_ctl_right_OCCIPITAL_rh.data.mean(axis=0)) -\
             (BP_ctl_left_OCCIPITAL_rh.data.mean(axis=0) +
              BP_ctl_right_OCCIPITAL_lh.data.mean(axis=0))

super_ent = (BP_ent_left_OCCIPITAL_lh.data.mean(axis=0) +
             BP_ent_right_OCCIPITAL_rh.data.mean(axis=0)) -\
             (BP_ent_left_OCCIPITAL_rh.data.mean(axis=0) +
              BP_ent_right_OCCIPITAL_lh.data.mean(axis=0))

times = BP_ctl_left_OCCIPITAL_lh.times

plt.figure()
plt.plot(times, super_ctl, 'r', linewidth=2, label="joint ctl")
plt.plot(times, super_ent, 'b', linewidth=2, label="joint ent")

plt.legend()
plt.title("Joint power difference waves (power)")
plt.ylabel("zscore")
plt.xlabel("Time (seconds)")
# plt.savefig("%s_BP_alpha.png" % label.name)

plt.figure()
plt.plot(times, source_psd_ent_left.mean(axis=0), 'b',
         linewidth=2, label="ent_left")
#    plt.plot(times, source_psd_ent_left.mean(axis=0) +
#             source_psd_ent_left.std(axis=0), 'b--')
#    plt.plot(times, source_psd_ent_left.mean(axis=0) -
#             source_psd_ent_left.std(axis=0), 'b--')

plt.plot(times, source_psd_ctl_left.mean(axis=0), 'r',
         linewidth=2, label="ctl_left")
#    plt.plot(times, source_psd_ctl_left.mean(axis=0) -
#             source_psd_ctl_left.std(axis=0), 'r--')
#    plt.plot(times, source_psd_ctl_left.mean(axis=0) +
#             source_psd_ctl_left.std(axis=0), 'r--')

plt.plot(times, source_psd_ent_right.mean(axis=0), 'g',
         linewidth=2, label="ent_right")
#    plt.plot(times, source_psd_ent_right.mean(axis=0) +
#             source_psd_ent_right.std(axis=0), 'g--')
#    plt.plot(times, source_psd_ent_right.mean(axis=0) -
#             source_psd_ent_right.std(axis=0), 'g--')

plt.plot(times, source_psd_ctl_right.mean(axis=0), 'm',
         linewidth=2, label="ctl_right")
#    plt.plot(times, source_psd_ctl_right.mean(axis=0) +
#             source_psd_ctl_right.std(axis=0), 'y--')
#    plt.plot(times, source_psd_ctl_right.mean(axis=0) -
#             source_psd_ctl_right.std(axis=0), 'y--')
plt.legend()
plt.title(label.name)


def psds_to_DataFrame(psds, times, condition=None):
    """
    convert a list of stcs to a pandas dataframe for plotting with seaborn.

    stcs : list of stcs to be converted.
    times : Numpy array with the times of the stcs.
    condition : string to add a condition column.
    """
    results_tmp = []

    for j in range(len(psds)):
        tmp_pd = pd.DataFrame()
        tmp_pd["psd"] = psds[j]
        tmp_pd["times"] = times
        tmp_pd["trial"] = j

        if condition is not None:
            tmp_pd["Condition"] = condition

        results_tmp += [tmp_pd]

    return pd.concat(results_tmp)


psds_ent_left_pas_2 = psds_to_DataFrame(source_psd_ent_left_pas_2, times,
                                        "ent_l_pas_2")
psds_ent_left_pas_3 = psds_to_DataFrame(source_psd_ent_left_pas_3, times,
                                        "ent_l_pas_3")
psds_ctl_left_pas_2 = psds_to_DataFrame(source_psd_ctl_left_pas_2, times,
                                        " ctl_l_pas_2")
psds_ctl_left_pas_3 = psds_to_DataFrame(source_psd_ctl_left_pas_3, times,
                                        "ctl_l_pas_3")

psds_ent_right_pas_2 = psds_to_DataFrame(source_psd_ent_right_pas_2, times,
                                         "ent_r_pas_2")
psds_ent_right_pas_3 = psds_to_DataFrame(source_psd_ent_right_pas_3, times,
                                         "ent_r_pas_3")
psds_ctl_right_pas_2 = psds_to_DataFrame(source_psd_ctl_right_pas_2, times,
                                         "ctl_r_pas_2")
psds_ctl_right_pas_3 = psds_to_DataFrame(source_psd_ctl_right_pas_3, times,
                                         "ctl_r_pas_3")


psds_ent_r = psds_to_DataFrame(source_psd_ent_right, times, "ent_r")
psds_ctl_l = psds_to_DataFrame(source_psd_ctl_left, times, "ctl_l")
psds_ctl_r = psds_to_DataFrame(source_psd_ctl_right, times, "ctl_r")

psds_all = pd.concat([psds_ent_left_pas_2,
                      psds_ent_left_pas_3,
                      psds_ctl_left_pas_2,
                      psds_ctl_left_pas_3,
                      psds_ent_right_pas_2,
                      psds_ent_right_pas_3,
                      psds_ctl_right_pas_2,
                      psds_ctl_right_pas_3])

plt.figure()
sns.tsplot(psds_all, time="times", unit="trial", condition="Condition",
           value="psd", err_style="ci_bars", interpolate=True)
