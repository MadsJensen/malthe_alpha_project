"""
This is a group of function to be used on TF data.

@author: mje
@email: mads [] cnru.dk
"""

from my_settings import *
import numpy as np
import mne
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator,
                              source_induced_power)

import matplotlib.pyplot as plt


def calc_ALI(subject, show_plot=False):
   """Function calculates the alpha lateralization index (ALI).

    The alpha lateralization index (ALI) is based on:
    Huurne, N. ter, Onnink, M., Kan, C., Franke, B., Buitelaar, J.,
    & Jensen, O. (2013).
    Parameters
    ----------
    subject : string
        The name of the subject to calculate ALI for.
    show_plot : bool
        Whether to plot the data or not.

    RETURNS
    -------
    ali_left : the ALI for the left cue
    ali_right : the ALI for the right cue
    """
    ctl_left_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_left_OCCIPITAL_lh_dSPM" % (subject))
    ctl_right_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_left_OCCIPITAL_rh_dSPM" % (subject))
    ctl_left_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_right_OCCIPITAL_lh_dSPM" % (subject))
    ctl_right_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_right_OCCIPITAL_rh_dSPM" % (subject))

    ALI_left_cue_ctl = ((ctl_left_roi_left_cue.data.mean(axis=0) -
                         ctl_right_roi_left_cue.data.mean(axis=0)) /
                        (ctl_left_roi_left_cue.data.mean(axis=0) +
                         ctl_right_roi_left_cue.data.mean(axis=0)))

    ALI_right_cue_ctl = ((ctl_left_roi_right_cue.data.mean(axis=0) -
                          ctl_right_roi_right_cue.data.mean(axis=0)) /
                         (ctl_left_roi_right_cue.data.mean(axis=0) +
                          ctl_right_roi_right_cue.data.mean(axis=0)))

    ent_left_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_left_OCCIPITAL_lh_dSPM" % (subject))
    ent_right_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_left_OCCIPITAL_rh_dSPM" % (subject))
    ent_left_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_right_OCCIPITAL_lh_dSPM" % (subject))
    ent_right_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_right_OCCIPITAL_rh_dSPM" % (subject))

    ALI_left_cue_ent = ((ent_left_roi_left_cue.data.mean(axis=0) -
                         ent_right_roi_left_cue.data.mean(axis=0)) /
                        (ent_left_roi_left_cue.data.mean(axis=0) +
                         ent_right_roi_left_cue.data.mean(axis=0)))

    ALI_right_cue_ent = ((ent_left_roi_right_cue.data.mean(axis=0) -
                          ent_right_roi_right_cue.data.mean(axis=0)) /
                         (ent_left_roi_right_cue.data.mean(axis=0) +
                          ent_right_roi_right_cue.data.mean(axis=0)))

    if show_plot:
        times = ent_left_roi_left_cue.times
        plt.figure()
        plt.plot(times, ALI_left_cue_ctl, 'r', label="ALI Left cue control")
        plt.plot(times, ALI_left_cue_ent, 'b', label="ALI Left ent control")
        plt.plot(times, ALI_right_cue_ctl, 'g', label="ALI Right cue control")
        plt.plot(times, ALI_right_cue_ent, 'm', label="ALI Right ent control")
        plt.legend()
        plt.title("ALI curves for subject: %s" % subject)
        plt.show()

    return (ALI_left_cue_ctl, ALI_right_cue_ctl,
            ALI_left_cue_ent, ALI_right_cue_ent)


def calc_power(subject, epochs, condition=None, save=True):
    """Calculates induced power
    
    Does TF...

    Parameters
    ----------
    subject : string
        the subject number.
    epochs : ???  # TODO give proper name for epochs file
        the epochs to calculate power from.
    condition : string
        the condition to use if there several in the epochs file.
    save : bool
        whether for save the results. Defaults to True.
    """
    frequencies = np.arange(8, 13, 1)  # define frequencies of interest
    n_cycles = 4   # frequencies / 3.
    inverse_operator = read_inverse_operator(mne_folder +
                                             "%s-inv.fif" % subject)
    labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Brodmann',
                                        regexp="Bro",
                                        subjects_dir=subjects_dir)
    label = labels[6]  # Left BA17
    snr = 1.0  # Standard assumption for average data but using it for single trial
    lambda2 = 1.0 / snr ** 2
    method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

    if condition:
        epochs_test = epochs[condition]
    else:
        epochs_test = epochs    
    
    power, phase_lock = source_induced_power(epochs_test,
                                             inverse_operator,
                                             frequencies,
                                             label=label,
                                             method=method,
                                             lambda2=lambda2,
                                             n_cycles=n_cycles,
                                             use_fft=True,
                                             pick_ori=None,
                                             baseline=(None, -0.3),
                                             baseline_mode='zscore',
                                             pca=True,
                                             n_jobs=2)

    if save:
        np.save(tf_folder + "pow_%s_%s-%s_%s_%s_%s.npy" % (subject,
                                                        frequencies[0],
                                                        frequencies[-1],
                                                        label.name, condition,
                                                        method),
                                                        power)

    return power, phase_lock



