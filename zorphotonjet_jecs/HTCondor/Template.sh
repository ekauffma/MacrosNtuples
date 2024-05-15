#!/bin/bash

# All the variables in capital letters are set from the SubmitToHTCondor.sh script
# $1 input file to be set from Template.sub
# $2 output file to be set from Template.sub
# remove --JEC if you want the raw pT of the jets 

source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_102 x86_64-centos7-gcc11-opt # T2B environment
cd SUBPATH
cd ../../  # directory with scripts

python3 analysis.py --max_events -1 -i $1 -o $2 -c CHANNEL --year YEAR --era ERA --isData --JEC
