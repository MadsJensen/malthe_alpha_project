# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 11:37:45 2015

@author: mje
"""


###############################################################################
# Show event related fields images

# and order with spectral reordering
# If you don't have scikit-learn installed set order_func to None
from sklearn.cluster.spectral import spectral_embedding  # noqa
from sklearn.metrics.pairwise import rbf_kernel   # noqa


def order_func(times, data):
    this_data = data[:, (times > 0.0) & (times < 0.350)]
    this_data /= np.sqrt(np.sum(this_data ** 2, axis=1))[:, np.newaxis]
    return np.argsort(spectral_embedding(rbf_kernel(this_data, gamma=1.),
                      n_components=1, random_state=0).ravel())

good_pick = -92# channel with a clear evoked response
#bad_pick = 98  # channel with no evoked response

plt.close('all')
mne.viz.plot_image_epochs(epochs["ent_L"], [good_pick], sigma=0.5, vmin=-100,
                          vmax=250, colorbar=True, order=order_func, show=True)