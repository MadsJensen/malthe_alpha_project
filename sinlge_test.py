import socket
import mne
from mne.minimum_norm import (make_inverse_operator, apply_inverse)

import os
# import subprocess
import glob

cmd = "/usr/local/common/meeg-cfin/configurations/bin/submit_to_isis"

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

os.chdir(mne_folder)
bem_list = glob.glob("*8192-8192*sol.fif")
bem_list.sort()

subject = "0006"

# Setup source space and forward model

raw_fname = save_folder + "%s_filtered_ica_mc_raw_tsss.fif" % subject
trans_fname = mne_folder + "%s-trans.fif" % subject
bem = bem_list[2]

src = mne.setup_source_space(subject,
                             mne_folder + "%s-oct-6-src.fif" % subject,
                             spacing="oct6",
                             subjects_dir=subjects_dir,
                             n_jobs=2,
                             overwrite=True)  # 1 for each hemispere

fwd = mne.make_forward_solution(raw_fname, trans=trans_fname,
                                src=src,
                                bem=bem,
                                meg=True,
                                eeg=True,
                                fname=mne_folder + "%s-fwd.fif" % subject,
                                overwrite=True)

fwd = mne.read_forward_solution(mne_folder + "%s-fwd.fif" % subject)
cov = mne.read_cov(mne_folder + "%s-cov.fif" % subject)
epochs = mne.read_epochs(epochs_folder +
                         "%s_filtered_ica_mc_tsss-epo.fif" % subject,
                         preload=False)
inv = make_inverse_operator(epochs.info, fwd, cov,
                            loose=0.2, depth=0.8)

mne.minimum_norm.write_inverse_operator(mne_folder +
                                        "%s-inv.fif" % subject,
                                        inv)


labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Lobes',
                                    # regexp="Bro",
                                    subjects_dir=subjects_dir)


snr = 3.0  # Standard assumption for average data but using it for single trial
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)


# Load data
fname_inv = mne_folder + "%s-inv.fif" % subject
fname_evoked = epochs_folder + "%s_filtered_ica_mc_tsss-ave.fif" % subject
evokeds = mne.read_evokeds(fname_evoked, baseline=(None, 0))

for evk in evokeds:
    stc = apply_inverse(evk, inv, lambda2=lambda2,
                        method=method)
    exec("stc_%s_%s = stc" % (subject, evk.comment))


src = mne.read_source_spaces(mne_folder + "%s-oct6-src.fif" % subject)
labels = mne.read_labels_from_annot(subject, parc='PALS_B12_Lobes',
                                    # regexp="Bro",
                                    subjects_dir=subjects_dir)
labels_occ = [labels[9], labels[10], labels[9]+labels[10]]

lbl_ent_left = mne.extract_label_time_course(stc_ent_left,
                                             labels=[labels[9]],
                                             src=src,
                                             mode="pca_flip")

lbl_ctl_left = mne.extract_label_time_course(stc_ctl_left,
                                             labels=[labels[9]],
                                             src=src,
                                             mode="pca_flip")
