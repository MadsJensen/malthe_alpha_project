import mne
import os
import socket
from mne.minimum_norm import (read_inverse_operator, point_spread_function,
                              cross_talk_function)
from mayavi import mlab

# Setup paths and prepare raw data
hostname = socket.gethostname()

if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    n_jobs = 1

subjects_dir = data_path + "fs_subjects_dir/"

# change dir to save files the rigth place
os.chdir(data_path)

fname_inv = mne_folder + '0004-inv.fif'
fname_epochs = epochs_folder + "0004_filtered_ica_mc_tsss-epo.fif"
fname_evoked = epochs_folder = "0004_filtered_ica_mc_tsss-ave.fif"

labels = mne.read_labels_from_annot('0004', parc='PALS_B12_Lobes',
                                    # regexp="Bro",
                                    subjects_dir=subjects_dir)

labels_occ = [labels[9], labels[10], labels[9]+labels[10]]

# Load data
inverse_operator = read_inverse_operator(fname_inv)
forward = mne.read_forward_solution(fname_fwd)
epochs = mne.read_epochs(fname_epochs)
evokeds = mne.read_evokeds(fname_evoked, baseline=(None, 0))


reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12,  # T (magnetometers)
              #  eog=250e-6  # uV (EOG channels)
              )

labels = mne.read_labels_from_annot('0001', parc='PALS_B12_Lobes',
                                    # regexp="Bro",
                                    subjects_dir=subjects_dir)

labels_occ = [labels[9], labels[10], labels[9]+labels[10]]

# regularisation parameter
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = 'MNE'  # can be 'MNE' or 'sLORETA'
mode = 'svd'
n_svd_comp = 1

# Point spread
stc_psf_meg, _ = point_spread_function(inverse_operator,
                                       forward, method=method,
                                       labels=[labels_occ[1]],
                                       lambda2=lambda2,
                                       pick_ori='normal',
                                       mode=mode,
                                       n_svd_comp=n_svd_comp)

# save for viewing in mne_analyze in order of labels in 'labels'
# last sample is average across PSFs
# stc_psf_eegmeg.save('psf_eegmeg')
# stc_psf_meg.save('psf_meg')

fmin = 0.
time_label = "MEG %d"
fmax = stc_psf_meg.data[:, 0].max()
fmid = fmax / 2.
brain_meg = stc_psf_meg.plot(surface='inflated', hemi='both',
                             subjects_dir=subjects_dir,
                             time_label=time_label,
                             figure=mlab.figure(size=(500, 500)))

#brain_meg.add_label(labels_occ[0], hemi="lh", borders=True)
brain_meg.add_label(labels_occ[1], hemi="rh", borders=True)

# The PSF is centred around the right auditory cortex label,
# but clearly extends beyond it.
# It also contains "sidelobes" or "ghost sources"
# in middle/superior temporal lobe.
# For the Aud-RH example, MEG and EEGMEG do not seem to differ a lot,
# but the addition of EEG still decreases point-spread to distant areas
# (e.g. to ATL and IFG).
# The chosen labels are quite far apart from each other, so their PSFs
# do not overlap (check in mne_analyze)


## %% CROSS-TALK FUNCTION
# regularisation parameter
snr = 3.0
lambda2 = 1.0 / snr ** 2
mode = 'svd'
n_svd_comp = 1

method = 'dSPM'  # can be 'MNE', 'dSPM', or 'sLORETA'
stc_ctf_mne = cross_talk_function(inverse_operator,
                                  forward,
                                  labels=[labels_occ[0]],
                                  method=method, 
                                  lambda2=lambda2,
                                  signed=False, 
                                  mode=mode,
                                  n_svd_comp=n_svd_comp)

# from mayavi import mlab
fmin = 0.
time_label = "MNE %d"
fmax = stc_ctf_mne.data[:, 0].max()
fmid = fmax / 2.
brain_mne = stc_ctf_mne.plot(surface='inflated', hemi='both',
                             subjects_dir=subjects_dir,
                             time_label=time_label,
                             figure=mlab.figure(size=(500, 500)))

brain_mne.add_label(labels_occ[0], hemi="lh", borders=True)

# Cross-talk functions for MNE and dSPM (and sLORETA) have the same shapes
# (they may still differ in overall amplitude).
# Point-spread functions (PSfs) usually differ significantly.
