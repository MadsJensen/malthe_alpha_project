"""
This is a group of function to be used on TF data.

@author: mje
@email: mads [] cnru.dk
"""

from my_settings import *
# import numpy as np
import mne


def calc_ALI(subject, condition):
    u"""Function calculates the alpha lateralization index (ALI).

    The alpha lateralization index (ALI) is based on:
    Huurne, N. ter, Onnink, M., Kan, C., Franke, B., Buitelaar, J.,
    & Jensen, O. (2013). Behavioral Consequences of Aberrant Alpha
    Lateralization in Attention-Deficit/Hyperactivity Disorder.
    Biological Psychiatry, 74(3), 227–233.
    http://doi.org/10.1016/j.biopsych.2013.02.001

    Parameters
    ----------
    subject : string
        The name of the subject to calculate ALI for.
    condition : string
        The condition to be calculated.

    RETURNS
    -------
    ali_left : the ALI for the left cue
    ali_right : the ALI for the right cue
    """
    pow_left_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_%s_left_OCCIPITAL_lh" % (subject,
                                                                 condition))
    pow_right_roi_left_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_%s_left_OCCIPITAL_rh" % (subject,
                                                                 condition))
    pow_left_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_%s_right_OCCIPITAL_lh" % (subject,
                                                                  condition))
    pow_right_roi_right_cue =\
        mne.read_source_estimate(tf_folder +
                                 "BP_%s_%s_right_OCCIPITAL_rh" % (subject,
                                                                  condition))

    ALI_left_cue = ((pow_left_roi_left_cue.data.mean(axis=0) -
                     pow_right_roi_left_cue.data.mean(axis=0)) /
                    (pow_left_roi_left_cue.data.mean(axis=0) +
                     pow_right_roi_left_cue.data.mean(axis=0)))

    ALI_right_cue = ((pow_left_roi_right_cue.data.mean(axis=0) -
                      pow_right_roi_right_cue.data.mean(axis=0)) /
                     (pow_left_roi_right_cue.data.mean(axis=0) +
                      pow_right_roi_right_cue.data.mean(axis=0)))

    return ALI_left_cue, ALI_right_cue
