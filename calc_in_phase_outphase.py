import mne
import numpy as np
import os

from my_settings import *

os.chdir(log_folder)

# for subject in subjects[5:]
subject = "0009"

for subject in subjects:
    raw = mne.io.Raw(maxfiltered_folder + "%s_data_mc_raw_tsss.fif" % subject,
                     preload=True)
    dio = raw._data[395]
    fe = mne.find_events(raw, min_duration=0.01)

    for i in range(len(fe)):
        fe[i][0] = fe[i][0] - raw.first_samp

    phase_res = []
    for i in range(len(fe)):
        if ((fe[i][2] == 16) or (fe[i][2] == 32) or
                (fe[i][2] == 64) or (fe[i][2] == 128)):
            target_sample = fe[i][0]
            back_sample = fe[i][0] - 120
            first_idx = np.argmax(dio[back_sample:back_sample+150] < 0.035)
            target_idx = np.argmax(dio[target_sample:target_sample+50] < 0.035)
            phase_res.append(np.abs((back_sample + first_idx) -
                                    (target_sample + target_idx)))

    phase_res = np.asarray(phase_res)
    phase_bin = phase_res < 130

    np.save(log_folder + "%s_phase_bin" % subject, phase_bin)

