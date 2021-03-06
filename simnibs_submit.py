"""
Doc string here.

@author: cjb
@author: mje

last edited: Wed Sep 9 2015
"""

from __future__ import print_function
import os
import sys
import subprocess
# import subprocess
# import numpy as np
# from mne.preprocessing.maxfilter import apply_maxfilter

CLOBBER = False
FAKE = False
VERBOSE = True

# ENH: install "official" version of stormdb on isis/hyades
path_to_stormdb = '/usr/local/common/meeg-cfin/stormdb'
# path_to_stormdb = "/volatile/mje/meeg-cfin/stormdb"
sys.path.append(path_to_stormdb)

from stormdb.access import Query

# path to submit_to_isis
cmd = "/usr/local/common/meeg-cfin/configurations/bin/submit_to_isis"
proj_code = "MINDLAB2015_MEG-CorticalAlphaAttention"

db = Query(proj_code)
proj_folder = os.path.join('/projects', proj_code)
scratch_folder = os.path.join(proj_folder, 'scratch/')
fs_subjects_dir = os.path.join(scratch_folder, 'fs_subjects_dir/')

subjects_dir = os.path.join(scratch_folder, 'fs_subjects_dir')
script_dir = proj_folder + '/scripts/'

included_subjects = db.get_subjects()
# just test with first one!

sub_new = []
#
for sub in [included_subjects[5]]:
    if not os.path.isfile(fs_subjects_dir +
                          "%s/%s_t1.nii.gz" % (sub[:4], sub[:4])):
        # this is an example of getting the DICOM files as a list
        # sequence_name='t1_mprage_3D_sag'
        MR_study = db.get_studies(sub, modality='MR')
        if len(MR_study) > 0:
            # This is a 2D list with [series_name, series_number]
            series = db.get_series(sub, MR_study[0], 'MR')
            t1 = series["t1_mpr_sag_weakFS"]
            t2 = series["t2_tse_sag_HighBW"]

            # Change this to be more elegant: check whether any item in series
            # matches sequence_name
            in_t1 = db.get_files(sub, MR_study[0], 'MR', t1)
            in_t2 = db.get_files(sub, MR_study[0], 'MR', t2)

            subj_fname = sub[:4]
            sub_new += [sub]

            convert_t1 = "mri_convert %s %s_t1.nii.gz" % (in_t1[0], subj_fname)
            print(convert_t1)
            convert_t2 = "mri_convert %s %s_t2.nii.gz" % (in_t2[0], subj_fname)
            print(convert_t2)
            
            os.chdir(fs_subjects_dir + subj_fname)
            subprocess.call([cmd, "1", convert_t1])
            subprocess.call([cmd, "1", convert_t2])


#for sub in included_subjects[5]:
#    run_simnibs = "mri2mesh --all %s %s_t1.nii.gz %s_t2.nii.gz"  \
#                  % (sub[:4], sub[:4], sub[:4])
#
#    if os.path.isfile(fs_subjects_dir +
#                      "%s/%s_t1.nii.gz" % (sub[:4], sub[:4])) &\
#        os.path.isfile(fs_subjects_dir +
#                       "%s/%s_t2.nii.gz" % (sub[:4], sub[:4])):
#        if os.path.isfile(fs_subjects_dir + "%s/m2m_%s/csf.stl"
#                          % (sub[:4], sub[:4])):
#          print("sub: %s" % sub[:4])
#                              
#          os.chdir(fs_subjects_dir + sub[:4])
#          subprocess.call([cmd, "1", run_simnibs])
