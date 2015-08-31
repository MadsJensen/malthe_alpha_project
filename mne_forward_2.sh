# This script is heavily based on the forward model script from cam meg wiki @:
# http://imaging.mrc-cbu.cam.ac.uk/meg/AnalyzingData/MNE_ForwardSolution

# variables
#datapath='/projects/MINDLAB2011_24-MEG-readiness/scratch' # root directory for your MEG data
#MRIpath='/projects/MINDLAB2011_24-MEG-readiness/scratch/mri'    # where your MRI subdirectories are

datapath='/projects/MINDLAB2011_24-MEG-readiness/scratch' # root directory for your MEG data
MRIpath='/projects/MINDLAB2011_24-MEG-readiness/scratch/mri'

# The subjects and sessions to be used
subjects=(\
    'p_01' \
)
sessions=(\
    'classic-tsss-mc-autobad_ver_4' \
    'plan-tsss-mc-autobad_ver_4' \
)

## setup the filename to be used
nsessions=${#sessions[*]}
lastsession=`expr $nsessions - 1`

nsubjects=${#subjects[*]}
lastsubj=`expr $nsubjects - 1`
## Processing

for m in `seq 0 $lastsubj` 
do
  echo " "
  echo " Setup forward model, source space, make morph maps and"
  echo "Computing forward solution for SUBJECT:  ${subjects[m]}"
  echo " "
  
  # Source space
  mne_setup_source_space --subject fs_${subjects[m]} --ico 4 --overwrite

  ### setup model 1 layer (MEG only)
  mne_setup_forward_model --overwrite  --subject fs_${subjects[m]} --surf --ico 4

 
  # Generate morph maps for morphing between subject and fsaverage
  #mne_make_morph_maps --from fs_${subject[m]} --to fsaverage

  echo " "
  echo "Compute forward model"
  echo " "

    for j in `seq 0 ${lastsession}`
    do
        fname=${subjects[m]}_${sessions[j]}
        #echo ${fname}
        mne_do_forward_solution \
            --overwrite \
            --subject fs_${subjects[m]} \
            --mindist 5 \
            --spacing ico-4 \
            --megonly \
            --bem ${MRIpath}/fs_${subjects[m]}/bem/fs_${subjects[m]}-5120 \
            --meas ${datapath}/${fname}.fif \
            --mri ${datapath}/${fname}-trans.fif \
            --fwd ${datapath}/${fname}-fwd.fif
            #--src ${MRIpath}/fs_${subjects[m]}/bem/fs_${subjects[m]}-5-src.fif \
    done

done 
