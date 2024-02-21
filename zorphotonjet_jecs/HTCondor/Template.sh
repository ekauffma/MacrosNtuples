#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_102 x86_64-centos7-gcc11-opt # T2B environment
cd subpath # path for the submission files to be set from the SubmitToHTCondor.sh script
cd ../../  # directory with scripts

# $1 input file to be set from Template.sub
# $2 output file to be set from Template.sub
# "channel" to be set from the SubmitToHTCondor.sh script
# remove --JEC if you want the raw pT of the jets 
python3 analysis.py --max_events -1 --JEC -i $1 -o $2 -c channel
