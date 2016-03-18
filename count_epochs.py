import mne
import pandas as pd

from my_settings import *

reject = dict(grad=4000e-13,  # T / m (gradiometers)
              mag=4e-12,  # T (magnetometers)
              eeg=180e-6  #
              )

result = pd.DataFrame()

# for subject in subjects:

subject = "0004"

epochs = mne.read_epochs(epochs_folder + "%s_trail_start-epo.fif" % subject,
                         preload=False)
epochs.drop_bad_epochs(reject)

row = pd.DataFrame()
epoch_count = {}
for key in epochs.event_id.keys():
    epoch_count[key] = len(epochs[key])

result = result.append(row, ignore_index=True)
