# This script is heavily based on the forward model script from cam meg wiki @:
# http://imaging.mrc-cbu.cam.ac.uk/meg/AnalyzingData/MNE_ForwardSolution

# variables
# datapath=/projects/projects/MINDLAB2013_18-MEG-HypnosisAnarchicHand/scratch # root directory for your MEG data
# SUBJECTS_DIR=/projects/MINDLAB2013_18-MEG-HypnosisAnarchicHand/scratch/fs_subjects_dir

# The subjects and sessions to be used
subjects=(\
    'p_01' \

)


nsubjects=${#subjects[*]}
lastsubj=`expr $nsubjects - 1`
## Processing

for m in `seq 0 $lastsubj`
do
  echo " "
  echo " Making BEM solution for SUBJECT:  ${subjects[m]}"
  echo " "

  mne_watershed_bem --subject ${subjects[m]} --overwrite

  ln -sf $SUBJECTS_DIR/${subjects[m]}/bem/watershed/${subjects[m]}_inner_skull_surface $SUBJECTS_DIR/${subjects[m]}/bem/${subjects[m]}-inner_skull.surf
  ln -sf $SUBJECTS_DIR/${subjects[m]}/bem/watershed/${subjects[m]}_outer_skull_surface $SUBJECTS_DIR/${subjects[m]}/bem/${subjects[m]}-outer_skull.surf
  ln -sf $SUBJECTS_DIR/${subjects[m]}/bem/watershed/${subjects[m]}_outer_skin_surface  $SUBJECTS_DIR/${subjects[m]}/bem/${subjects[m]}-outer_skin.surf
  ln -sf $SUBJECTS_DIR/${subjects[m]}/bem/watershed/${subjects[m]}_brain_surface       $SUBJECTS_DIR/${subjects[m]}/bem/${subjects[m]}-brain_surface.surf

  echo " "
  echo " Setting up forward model for  SUBJECT:  ${subjects[m]}"
  echo " "



done # subjects
