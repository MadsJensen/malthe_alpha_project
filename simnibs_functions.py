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


def make_symbolic_links(fname, subjects_dir):
    """Make symblic links between FS dir and subjects_dir.

    Parameters
    ----------
    fname : string
        The name of the subject to create for
    subjects_dir : string
        The subjects dir for FreeSurfer
    """

    make_links = "ln -s fs_%s/. *" % subject
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
    convert_csf = "meshfix csf.stl -u 10 --vertices 5120 --fsmesh"
    convert_skull = "meshfix skull.stl -u 10 --vertices 5120 --fsmesh"
    convert_skin = "meshfix skin.stl -u 10 --vertices 5120 --fsmesh"

    os.chdir(fs_subjects_dir + subject[:4] + "/m2m_%s" % subject[:4])
    subprocess.call([cmd, "1", convert_csf])
    subprocess.call([cmd, "1", convert_skull])
    subprocess.call([cmd, "1", convert_skin])


for subject in included_subjects[:4]:
    make_symbolic_links(subject, fs_subjects_dir)
