"""
@author: cjb
@author: mje

last edited: Wed Sep 9 2015
"""

from __future__ import print_function
import os, sys
import subprocess
import numpy as np
from mne.preprocessing.maxfilter import apply_maxfilter

CLOBBER = False
FAKE = False
VERBOSE = True

# ENH: install "official" version of stormdb on isis/hyades
path_to_stormdb = '/users/cjb/src/git/cfin-tools/stormdb'
sys.path.append(path_to_stormdb)

from stormdb.access import Query


# MAXFILTER PARAMS #

#         #call to maxfilter
#         apply_maxfilter(in_fname=in_name,
#                         out_fname=out_name,
#                         frame='head',
# #                        origin= "0 0 40",
#                         autobad="on",
#                         st=True,
#                         st_buflen=30,
#                         st_corr=0.95,
#                         mv_comp=True,
#                         mv_hp=headpos_log,
#                         cal='/projects/MINDLAB2011_24-MEG-readiness/misc/sss_cal_Mar11-May13.dat',
#                         ctc='/projects/MINDLAB2011_24-MEG-readiness/misc/ct_sparse_Mar11-May13.fif',
#                         overwrite=True,
#                         mx_args=' -v | tee %s' % tsss_mc_log,
#                         )


proj_code = "MEG_EEG-Training"

db = Query(proj_code)
proj_folder = os.path.join('/projects', proj_code)
scratch_folder = os.path.join(proj_folder, 'scratch/mje_maxfilter_test/')

subjects_dir = os.path.join(scratch_folder, 'fs_subjects_dir')
script_dir = proj_folder + '/scripts/'

included_subjects = db.get_subjects()
# just test with first one!
included_subjects = included_subjects[:2]

for sub in included_subjects:
    # this is an example of getting the DICOM files as a list
    # sequence_name='t1_mprage_3D_sag'
    MEG_study = db.get_studies(sub, modality='MEG')
    if MEG_study is not None:
        # This is a 2D list with [series_name, series_number]
        series = db.get_series(sub, MEG_study, 'MEG', verbose=False)
    # Change this to be more elegant: check whether any item in series
    # matches sequence_name
        for serie in series:
            if serie[0] != "empty_room":
                in_name = db.get_files(sub, MEG_study, 'MEG', serie[1])
                out_name = "%s_%s-raw_tsss_mc_TEST.fif" % (sub[:4], serie[0])
                print(out_name)
    
                # if len(in_name) > 1:
                for j, in_file in enumerate(in_name):
                    if j == 0:
                        out_fname = scratch_folder + out_name
                    else:
                        out_fname = scratch_folder\
                                    + out_name[:-4] + "-%d.fif" % j
                                    
                    tsss_mc_log = out_fname[:-3] + "log"
                    headpos_log = out_fname[:-4] + "_hp.log"
                    
                    print(tsss_mc_log)
                    print(headpos_log)
                        
                    apply_maxfilter(in_fname=in_file,
                                    out_fname=out_fname,
                                    frame='head',
                                    # origin= "0 0 40",
                                    autobad="on",
                                    st=True,
                                    st_buflen=30,
                                    st_corr=0.95,
                                    mv_comp=True,
                                    mv_hp=headpos_log,
                                    # cal=cal,
                                    # ctc=ctc,
                                    overwrite=True,
                                    mx_args=' -v > %s' % tsss_mc_log)