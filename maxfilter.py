from mne.preprocessing.maxfilter import apply_maxfilter
import os

# change data files dir
os.chdir('/projects/MINDLAB2015_MEG-Gambling/scratch/')
#
#

# file and log names
in_name = "p_01_data.fif"
out_name = "p_01_data_tsss-mc_autobad_raw.fif"
tsss_mc_log = "p_01_data_tsss-mc_autobad_raw.log"
headpos_log = "p_01_data_tsss-mc_autobad_headpos.log"

# call to maxfilter
apply_maxfilter(in_fname=in_name,
                out_fname=out_name,
                frame='head',
                # origin= "0 0 40",
                autobad="on",
                st=True,
                st_buflen=30,
                st_corr=0.95,
                mv_comp=True,
                mv_hp=headpos_log,
                # cal='/projects/MINDLAB2013_18-MEG-HypnosisAnarchicHand/misc/sss_cal.dat',
                # ctc='/projects/MINDLAB2013_18-MEG-HypnosisAnarchicHand/misc/ct_sparse.fif',
                overwrite=True,
                mx_args=' -v | tee %s' % tsss_mc_log,
                )
