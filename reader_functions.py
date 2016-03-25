import os

import mne
import numpy as np
import pandas as pd

from my_settings import *
os.chdir(tf_folder)

# os.chdir("/home/mje/Projects/malthe_alpha_project/data/tf_data")


def make_log_file(subject):
    """ Create log file from events file

    Parameters
    ----------
    subjects : str
        string with subject id.

    returns
    -------
    df : Dataframe
        Pandas Dataframe
    """

    events = mne.read_events("%s-eve.fif" % subject)
    in_phase = np.load("%s_phase_bin.npy" % subject)
    columns_keys = ["condition_type", "condition_side", "target_side",
                    "target_type", "response", "PAS", "correct"]
    df = pd.DataFrame(columns=columns_keys)
    cond_dict = {1: ["ent", "left"], 2: ["ent", "right"],
                 4: ["ctl", "left"], 8: ["ctl", "right"]}
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
        row["congruent"] = row["condition_side"] == row["target_side"]
        df = df.append(row, ignore_index=True)

    df["correct"] = df["response"] == df["target_type"]
    df["in_phase"] = in_phase

    return df
