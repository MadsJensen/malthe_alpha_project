import os

import mne
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


X = []
ent_left_lh = np.empty([20, 73809])
ent_left_rh = []
ent_right_lh = []
ent_right_rh = []
ctl_left_lh = []
ctl_left_rh = []
ctl_right_lh = []
ctl_right_rh = []

for subject in subjects[:2]:
        # Load data
    ent_left_lh.append(np.load("itc_%s_8-12_Brodmann.17-lh_ent_left_dSPM.npy" %
                               subject).mean(axis=1).reshape(-1))
    ctl_left_lh.append(np.load("itc_%s_8-12_Brodmann.17-lh_ctl_left_dSPM.npy" %
                               subject).mean(axis=1).reshape(-1))
    ent_right_lh.append(np.load("itc_%s_8-12_Brodmann.17-lh_ent_right_dSPM.npy"
                                % subject).mean(axis=1).reshape(-1))
    ctl_right_lh.append(np.load("itc_%s_8-12_Brodmann.17-lh_ctl_right_dSPM.npy"
                                % subject).mean(axis=1).reshape(-1))
    ent_left_rh.append(np.load("itc_%s_8-12_Brodmann.17-rh_ent_left_dSPM.npy" %
                               subject).mean(axis=1).reshape(-1))
    ctl_left_rh.append(np.load("itc_%s_8-12_Brodmann.17-rh_ctl_left_dSPM.npy" %
                               subject).mean(axis=1).reshape(-1))
    ent_right_rh.append(np.load("itc_%s_8-12_Brodmann.17-rh_ent_right_dSPM.npy"
                                % subject).mean(axis=1).reshape(-1))
    ctl_right_rh.append(np.load("itc_%s_8-12_Brodmann.17-rh_ctl_right_dSPM.npy"
                                % subject).mean(axis=1).reshape(-1))

ent_left_lh = np.empty([20, 73809])
ent_left_rh = np.empty([20, 73809])
ent_right_lh = np.empty([20, 73809])
ent_right_rh = np.empty([20, 73809])
ctl_left_lh = np.empty([20, 73809])
ctl_left_rh = np.empty([20, 73809])
ctl_right_lh = np.empty([20, 73809])
ctl_right_rh = np.empty([20, 73809])

for i, subject in enumerate(subjects[:2]):
    tmp = np.load("itc_%s_8-12_Brodmann.17-lh_ent_left_dSPM.npy" %
                  subject.mean(axis=1).reshape(-1)
    ent_left_lh[i, :] = tmp

    tmp = np.load("itc_%s_8-12_Brodmann.17-lh_ctl_left_dSPM.npy" %
                  subject.mean(axis=1).reshape(-1)
    ctl_left_lh[i, :] = tmp

    tmp = np.load("itc_%s_8-12_Brodmann.17-lh_ent_right_dSPM.npy"
                  % subject.mean(axis=1).reshape(-1)
    ent_right_lh[i, :] = tmp

    tmp = np.load("itc_%s_8-12_Brodmann.17-lh_ctl_right_dSPM.npy"
                  % subject).mean(axis=1).reshape(-1)
    ctl_right_lh[i, :] = tmp

    tmp = np.load("itc_%s_8-12_Brodmann.17-rh_ent_left_dSPM.npy" %
                  subject).mean(axis=1).reshape(-1)
    ent_left_rh[i, :] = tmp

    tmp = np.load("itc_%s_8-12_Brodmann.17-rh_ctl_left_dSPM.npy" %
                  subject).mean(axis=1).reshape(-1)
    ctl_left_rh[i,: ] = tmp

    tmp = np.load("itc_%s_8-12_Brodmann.17-rh_ent_right_dSPM.npy"
                  % subject).mean(axis=1).reshape(-1)
    ent_right_rh[i, :] = tmp

    tmp np.load("itc_%s_8-12_Brodmann.17-rh_ctl_right_dSPM.npy"
                % subject).mean(axis=1).reshape(-1)
    ctl_right_rh[i, :] = tmp


ent_left_lh = np.array(ent_left_lh)
ent_left_rh = np.array(ent_left_rh)
ent_right_lh = np.array(ent_right_lh)
ent_right_rh = np.array(ent_right_rh)
ctl_left_lh = np.array(ctl_left_lh)
ctl_left_rh = np.array(ctl_left_rh)
ctl_right_lh = np.array(ctl_right_lh)
ctl_right_rh = np.array(ctl_right_rh)


X = np.vstack([ent_left_lh, ent_left_rh, ent_right_lh, ent_right_rh,
               ctl_left_lh, ctl_left_rh, ctl_right_lh, ctl_right_rh])

y = np.concatenate([[0]*20, [1]*20, [2]*20, [3]*20,
                    [4]*20, [5]*20, [6]*20, [7]*20])


def make_log_file(data):
    events = mne.read_events(data)
    columns_keys = ["condition_type", "condition_side", "target_side",
                    "target_type", "response", "PAS", "correct"]
    df = pd.DataFrame(columns=columns_keys)
    cond_dict = {1: ["ent", "left"], 2: ["ent", "right"],
                 4: ["con", "left"], 8: ["con", "right"]}
    target_dict = {16: ["left", "+"], 32: ["right", "+"],
                   64: ["left", "X"], 128: ["right", "X"]}
    response_dict = {9: "+", 10: "X"}
    pas_dict = {21: 1, 22: 2, 23: 3, 24: 4}
    idx = np.arange(0, len(events), 4)
    for i in idx:
        row = pd.DataFrame([{"condition_type": cond_dict[events[i][2]][0],
                             "condition_side": cond_dict[events[i][2]][1],
                             "target_side": target_dict[events[i+1][2]][0],
                             "target_type": target_dict[events[i+1][2]][1],
                             "response": response_dict[events[i+2][2]],
                             "PAS": pas_dict[events[i+3][2]]}])
        df = df.append(row, ignore_index=True)

    df["correct"] = df["response"] == df["target_type"]

    return df

