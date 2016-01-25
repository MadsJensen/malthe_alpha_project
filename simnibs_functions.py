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


def make_symbolic_links(subject, subjects_dir):
    """Make symblic links between FS dir and subjects_dir.

    Parameters
    ----------
    fname : string
        The name of the subject to create for
    subjects_dir : string
        The subjects dir for FreeSurfer
    """

    make_links = "ln -s fs_%s/* ." % subject[:4]
    os.chdir(fs_subjects_dir + subject[:4])
    subprocess.call([cmd, "1", make_links])


def convert_surfaces(subject, subjects_dir):
    """Convert the SimNIBS surface to FreeSurfer surfaces.

    Parameters
    ----------
    subject : string
       The name of the subject
    subjects_dir : string
        The subjects dir for FreeSurfer
    """
    convert_csf = "meshfix csf.stl -u 10 --vertices 4098 --fsmesh"
    convert_skull = "meshfix skull.stl -u 10 --vertices 4098 --fsmesh"
    convert_skin = "meshfix skin.stl -u 10 --vertices 4098 --fsmesh"

    os.chdir(fs_subjects_dir + subject[:4] + "/m2m_%s" % subject[:4])
    subprocess.call([cmd, "1", convert_csf])
    subprocess.call([cmd, "1", convert_skull])
    subprocess.call([cmd, "1", convert_skin])


def copy_surfaces(subject, subjects_dir):
    """Copy the converted FreeSurfer surfaces to the bem dir.

    Parameters
    ----------
    subject : string
       The name of the subject
    subjects_dir : string
        The subjects dir for FreeSurfer
    """
    os.chdir(fs_subjects_dir + subject[:4] + "/m2m_%s" % subject[:4])
    copy_inner_skull = "cp -f csf_fixed.fsmesh " + subjects_dir + \
                       "/%s/bem/inner_skull.surf" % subject[:4]
    copy_outer_skull = "cp -f skull_fixed.fsmesh " + subjects_dir + \
                       "/%s/bem/outer_skull.surf" % subject[:4]
    copy_outer_skin = "cp -f skin_fixed.fsmesh " + subjects_dir + \
                       "/%s/bem/outer_skin.surf" % subject[:4]

    subprocess.call([cmd, "1", copy_inner_skull])
    subprocess.call([cmd, "1", copy_outer_skull])
    subprocess.call([cmd, "1", copy_outer_skin])

    os.chdir(fs_subjects_dir + subject[:4] + "/bem")
    convert_skin_to_head = "mne_surf2bem --surf outer_skin.surf --fif %s-head.fif --id 4" % subject[:4]
    subprocess.call([cmd, "1", convert_skin_to_head])


def setup_mne_c_forward(subject):
    setup_forward = "mne_setup_forward_model --subject %s --surf --ico -6" %subject[:4]
    subprocess.call([cmd, "1", setup_forward])


for subject in included_subjects[3:5]:
    make_symbolic_links(subject, fs_subjects_dir)
        
for subject in included_subjects[3:5]:
    convert_surfaces(subject, fs_subjects_dir)    

for subject in included_subjects[3:5]:
    copy_surfaces(subject, fs_subjects_dir)    

for subject in included_subjects[3:5]:
    setup_mne_c_forward(subject)    

