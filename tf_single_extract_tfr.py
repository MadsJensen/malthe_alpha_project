from my_settings import *
import numpy as np
import mne
from mne.minimum_norm import (apply_inverse_epochs, read_inverse_operator,
                              source_induced_power)
from mne.time_frequency import cwt_morlet

snr = 1.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "MNE"  # use dSPM method (could also be MNE or sLORETA)


def single_epoch_tfr(epochs, condition, inv, src,
                     label):
    """Calculates single trail power

    Parameter
    ---------
    epochs : ???
        The subject number to use.
    condition : string
        ...
    inv = inverse_operator
        ...
    src : source space
        ...
    label : label
        ...
    """
    frequencies = np.arange(8, 13, 1)
    stcs = apply_inverse_epochs(epochs, inv, lambda2=lambda2, method=method,
                                label=None, pick_ori=None)
    time_series = [stc.extract_label_time_course(labels=label, src=src,
                                                 mode="pca_flip")[0]
                   for stc in stcs]

    ts_signed = []
    for j in range(len(time_series)):
        tmp = time_series[j]
        tmp *= np.sign(tmp[np.argmax(np.abs(tmp))])
        ts_signed.append(tmp)

    fs = cwt_morlet(np.asarray(ts_signed), epochs.info["sfreq"], frequencies,
                    use_fft=True, n_cycles=4)

    return fs

conditions = ["ctl_left", "ent_left", "ent_right", "ctl_right"]
ctl_left_results = []
ctl_right_results = []
ent_left_results = []
ent_right_results = []

for subject in subjects:
    epochs = mne.read_epochs(epochs_folder +
                             "%s_ds_filtered_ica_mc_tsss-epo.fif" % subject)
    inv = read_inverse_operator(mne_folder + "%s-inv.fif" % subject)
    src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subject)
    labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Lobes',
                                        # regexp="Bro",
                                        subjects_dir=subjects_dir)
    for condition in conditions:
        res = single_epoch_tfr(epochs[condition], condition,
                               inv, src, label=[labels[9]])

        if condition == "ctl_left":
            ctl_left_results.append(res)
        elif condition == "ctl_right":
            ctl_right_results.append(res)
        elif condition == "ent_left":
            ent_left_results.append(res)
        elif condition == "ent_right":
            ent_right_results.append(res)
