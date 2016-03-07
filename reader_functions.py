import os

import numpy as np
import pandas as pd
from my_settings import *
# os.chdir(tf_folder)

os.chdir("/home/mje/Projects/malthe_alpha_project/data/tf_data")

subject = "0004"

column_keys = ["subject", "condition", "hemi", "itc"]
result = pd.DataFrame(columns=column_keys)

for subject in subjects:
    # Load data
    ent_left_lh = np.load("itc_%s_8-12_Brodmann.17-lh_ent_left_dSPM.npy" %
                          subject)
    ctl_left_lh = np.load("itc_%s_8-12_Brodmann.17-lh_ctl_left_dSPM.npy" %
                          subject)
    ent_right_lh = np.load("itc_%s_8-12_Brodmann.17-lh_ent_right_dSPM.npy" %
                           subject)
    ctl_right_lh = np.load("itc_%s_8-12_Brodmann.17-lh_ctl_right_dSPM.npy" %
                           subject)
    ent_left_rh = np.load("itc_%s_8-12_Brodmann.17-rh_ent_left_dSPM.npy" %
                          subject)
    ctl_left_rh = np.load("itc_%s_8-12_Brodmann.17-rh_ctl_left_dSPM.npy" %
                          subject)
    ent_right_rh = np.load("itc_%s_8-12_Brodmann.17-rh_ent_right_dSPM.npy" %
                           subject)
    ctl_right_rh = np.load("itc_%s_8-12_Brodmann.17-rh_ctl_right_dSPM.npy" %
                           subject)

    row = pd.DataFrame([{"subject": subject, "condition": "ent_left",
                         "hemi": "lh",
                         "itc": ent_left_lh[:, :, 250:600].mean(),
                         "std": ent_left_lh[:, :, 250:600].std(),
                         "max": ent_left_lh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ctl_left",
                         "hemi": "lh",
                         "itc": ctl_left_lh[:, :, 250:600].mean(),
                         "std": ctl_left_lh[:, :, 250:600].std(),
                         "max": ctl_left_lh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ent_right",
                         "hemi": "lh",
                         "itc": ent_right_lh[:, :, 250:600].mean(),
                         "std": ent_right_lh[:, :, 250:600].std(),
                         "max": ent_right_lh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ctl_right",
                         "hemi": "lh",
                         "itc": ctl_right_lh[:, :, 250:600].mean(),
                         "std": ctl_right_lh[:, :, 250:600].std(),
                         "max": ctl_right_lh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ent_left",
                         "hemi": "rh",
                         "itc": ent_left_rh[:, :, 250:600].mean(),
                         "std": ent_left_rh[:, :, 250:600].std(),
                         "max": ent_left_rh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ctl_left",
                         "hemi": "rh",
                         "itc": ctl_left_rh[:, :, 250:600].mean(),
                         "std": ctl_left_rh[:, :, 250:600].std(),
                         "max": ctl_left_rh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ent_right",
                         "hemi": "rh",
                         "itc": ent_right_rh[:, :, 250:600].mean(),
                         "std": ent_right_rh[:, :, 250:600].std(),
                         "max": ent_right_rh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)

    row = pd.DataFrame([{"subject": subject, "condition": "ctl_right",
                         "hemi": "rh",
                         "itc": ctl_right_rh[:, :, 250:600].mean(),
                         "std": ctl_right_rh[:, :, 250:600].std(),
                         "max": ctl_right_rh[:, :, 250:600].max()}])
    result = result.append(row, ignore_index=True)
