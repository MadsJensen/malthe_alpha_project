# coding=utf-8
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
from mne.time_frequency import (psd_multitaper, cwt_morlet)
from mne.viz import iter_topography
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
                                 "BP_%s_ctl_left_OCCIPITAL_lh_dSPM"
                                 % (subject))
    ctl_right_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_left_OCCIPITAL_rh_dSPM"
                                 % (subject))
    ctl_left_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_right_OCCIPITAL_lh_dSPM"
                                 % (subject))
    ctl_right_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ctl_right_OCCIPITAL_rh_dSPM"
                                 % (subject))

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
                                 "BP_%s_ent_left_OCCIPITAL_lh_dSPM"
                                 % (subject))
    ent_right_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_left_OCCIPITAL_rh_dSPM"
                                 % (subject))
    ent_left_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_right_OCCIPITAL_lh_dSPM"
                                 % (subject))
    ent_right_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_ent_right_OCCIPITAL_rh_dSPM"
                                 % (subject))

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
    n_cycles = frequencies / 3.
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
                                                           label.name,
                                                           condition,
                                                           method),
                power)
        np.save(tf_folder + "itc_%s_%s-%s_%s_%s_%s.npy" % (subject,
                                                           frequencies[0],
                                                           frequencies[-1],
                                                           label.name,
                                                           condition,
                                                           method),
                power)

    return power, phase_lock


def calc_psd_epochs(epochs, plot=False):
    """Calculate PSD for epoch.

    Parameters
    ----------
    epochs : list of epochs
    plot : bool
        To show plot of the psds.
        It will be average for each condition that is shown.

    Returns
    -------
    psds_vol : numpy array
        The psds for the voluntary condition.
    psds_invol : numpy array
        The psds for the involuntary condition.
    """
    tmin, tmax = -0.5, 0.5
    fmin, fmax = 2, 90
    # n_fft = 2048  # the FFT size (n_fft). Ideally a power of 2
    psds_vol, freqs = psd_multitaper(epochs["voluntary"],
                                     tmin=tmin, tmax=tmax,
                                     fmin=fmin, fmax=fmax)
    psds_inv, freqs = psd_multitaper(epochs["involuntary"],
                                     tmin=tmin, tmax=tmax,
                                     fmin=fmin, fmax=fmax)

    psds_vol = 20 * np.log10(psds_vol)  # scale to dB
    psds_inv = 20 * np.log10(psds_inv)  # scale to dB

    if plot:
        def my_callback(ax, ch_idx):
            """Executed once you click on one of the channels in the plot."""
            ax.plot(freqs, psds_vol_plot[ch_idx], color='red',
                    label="voluntary")
            ax.plot(freqs, psds_inv_plot[ch_idx], color='blue',
                    label="involuntary")
            ax.set_xlabel = 'Frequency (Hz)'
            ax.set_ylabel = 'Power (dB)'
            ax.legend()

        psds_vol_plot = psds_vol.copy().mean(axis=0)
        psds_inv_plot = psds_inv.copy().mean(axis=0)

        for ax, idx in iter_topography(epochs.info,
                                       fig_facecolor='k',
                                       axis_facecolor='k',
                                       axis_spinecolor='k',
                                       on_pick=my_callback):
            ax.plot(psds_vol_plot[idx], color='red', label="voluntary")
            ax.plot(psds_inv_plot[idx], color='blue', label="involuntary")
        plt.legend()
        plt.gcf().suptitle('Power spectral densities')
        plt.show()

    return psds_vol, psds_inv, freqs


def single_trial_tf(epochs, n_cycles=4.):
    """


    Parameters
    ----------
    epochs : Epochs object
        The epochs to calculate TF analysis on.
    n_cycles : int
        The number of cycles for the Morlet wavelets.

    Returns
    -------
    results : numpy array
    """
    results = []
    frequencies = np.arange(6., 30., 1.)

    for j in range(len(epochs)):
        tfr = cwt_morlet(epochs.get_data()[j],
                         sfreq=epochs.info["sfreq"],
                         freqs=frequencies,
                         use_fft=True,
                         n_cycles=n_cycles,
                         zero_mean=False)
        results.append(tfr)
    return results


def calc_spatial_resolution(freqs, n_cycles):
    """Calculate the spatial resolution for a Morlet wavelet.

    The formula is: (freqs * cycles)*2.

    Parameters
    ----------
    freqs : numpy array
        The frequencies to be calculated.
    n_cycles : int or numpy array
        The number of cycles used. Can be integer for the same cycle for all
        frequencies, or a numpy array for individual cycles per frequency.

    Returns
    -------
    result : numpy array
        The results
    """
    result = np.empty_like(freqs)

    for i in range(len(result)):
        result[i] = (freqs[i] / float(n_cycles[i])) * 2

    return result


def calc_wavelet_duration(freqs, n_cycles):
    """Calculate the wavelet duration for a Morlet wavelet in ms.

    The formula is: (cycle / frequencies / pi)*1000

    Parameters
    ----------
    freqs : numpy array
        The frequencies to be calculated.
    n_cycles : int or numpy array
        The number of cycles used. Can be integer for the same cycle for all
        frequencies, or a numpy array for individual cycles per frequency.

    Returns
    -------
    result : numpy array
        The results
    """
    result = np.empty_like(freqs)

    for i in range(len(result)):
        result[i] = (float(n_cycles[i]) / freqs[i] / np.pi) * 1000

    return result
