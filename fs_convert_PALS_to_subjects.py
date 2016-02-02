from __future__ import print_function
import subprocess

# path to submit_to_isis
cmd = "/usr/local/common/meeg-cfin/configurations/bin/submit_to_isis"
proj_code = "MINDLAB2015_MEG-CorticalAlphaAttention"

subjects = ["0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011",
            "0012", "0013", "0014", "0015", "0016", "0017", "0020", "0021",
            "0022", "0023", "0024", "0025"]  # subject to run

for subject in subjects:
    convert_cmd_lh = "mri_surf2surf --srcsubject fsaverage " +  \
                     "--trgsubject %s --hemi lh " % subject + \
                     "--sval-annot $SUBJECTS_DIR/fsaverage/label/lh.PALS_B12_Brodmann.annot " + \
                     "--tval $SUBJECTS_DIR/%s/label/lh.PALS_B12_Brodmann.annot" % subject
    convert_cmd_rh = "mri_surf2surf --srcsubject fsaverage " +  \
                     "--trgsubject %s --hemi rh " % subject + \
                     "--sval-annot $SUBJECTS_DIR/fsaverage/label/rh.PALS_B12_Brodmann.annot " + \
                     "--tval $SUBJECTS_DIR/%s/label/rh.PALS_B12_Brodmann.annot" % subject
    
    subprocess.call([cmd, "1", convert_cmd_lh])
    subprocess.call([cmd, "1", convert_cmd_rh])
