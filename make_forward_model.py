# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 09:12:52 2015

@author: mje
"""
import mne
import socket

import numpy as np
import matplotlib.pyplot as plt
# Setup paths and prepare raw data
hostname = socket.gethostname()
if hostname == "Wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    n_jobs = 1
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    n_jobs = 1

subjects_dir = data_path + "fs_subjects_dir/"

raw_fname = data_path + "0001_p_03_filter_ds_ica-mc_raw_tsss.fif"
trans = data_path + "0001-trans.fif"
src = subjects_dir + '0001/bem/0001-oct-6-src.fif'
bem = subjects_dir + '0001/bem/0001-inner_skull-bem-sol.fif'


# Note that forward solutions can also be read with read_forward_solution
fwd = mne.make_forward_solution(raw_fname, trans, src, bem,
                                fname="0001-fwd.fif", meg=True, eeg=False,
                                mindist=5.0,
                                n_jobs=n_jobs, overwrite=True)

# convert to surface orientation for better visualization
fwd = mne.convert_forward_solution(fwd, surf_ori=True)
leadfield = fwd['sol']['data']

print("Leadfield size : %d x %d" % leadfield.shape)

grad_map = mne.sensitivity_map(fwd, ch_type='grad', mode='fixed')
mag_map = mne.sensitivity_map(fwd, ch_type='mag', mode='fixed')

###############################################################################
# Show gain matrix a.k.a. leadfield matrix with sensitivity map

picks_meg = mne.pick_types(fwd['info'], meg=True, eeg=False)

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Lead field matrix (500 dipoles only)', fontsize=14)
for ax, picks, ch_type in zip(axes, [picks_meg], ['meg']):
    im = ax.imshow(leadfield[picks, :], origin='lower', aspect='auto',
                   cmap='RdBu_r')
    ax.set_title(ch_type.upper())
    ax.set_xlabel('sources')
    ax.set_ylabel('sensors')
    plt.colorbar(im, ax=ax, cmap='RdBu_r')
plt.show()

plt.figure()
plt.hist([grad_map.data.ravel(), mag_map.data.ravel()],
         bins=20, label=['Gradiometers', 'Magnetometers'],
         color=['c', 'b'])
plt.legend()
plt.title('Normal orientation sensitivity')
plt.xlabel('sensitivity')
plt.ylabel('count')
plt.show()


grad_map.plot(time_label='Gradiometer sensitivity', subjects_dir=subjects_dir,
              clim=dict(lims=[0, 50, 100]),
              hemi="both")

mag_map.plot(time_label='MAG sensitivity', subjects_dir=subjects_dir,
             clim=dict(lims=[0, 50, 100]),
             hemi="split")
