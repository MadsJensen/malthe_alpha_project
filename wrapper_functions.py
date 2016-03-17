"""
Doc string here.

@author mje
@email: mads [] cnru.dk

"""
import os
import sys
import subprocess
import socket

cmd = "/usr/local/common/meeg-cfin/configurations/bin/submit_to_isis"

# SETUP PATHS AND PREPARE RAW DATA
hostname = socket.gethostname()

if hostname == "wintermute":
    data_path = "/home/mje/mnt/caa/scratch/"
    script_path = "/home/mje/mnt/caa/scripts/"
else:
    data_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scratch/"
    script_path = "/projects/MINDLAB2015_MEG-CorticalAlphaAttention/scripts/"

# CHANGE DIR TO SAVE FILES THE RIGTH PLACE
os.chdir(script_path)


subjects = ["0004", "0005", "0006", "0007", "0008", "0009", "0010", "0011",
            "0012", "0013", "0014", "0015", "0016", "0017", "0020", "0021",
            "0022", "0023", "0024", "0025"]  # subject to run


for subject in subjects:
    submit_cmd = "python epoching_from_pd.py %s" % subject
    subprocess.call([cmd, "4", submit_cmd])
