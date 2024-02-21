#!/bin/bash                                                           

# Set the paths below according to your needs:
jobpath=JobSub                                         # New directory to be created for the submission files
subpath=${PWD}/${jobpath}                              # Path to be used for the submission files of jobs to HTCondor

# Color variables for message and error printing
RED='\033[0;31m'
PURPLE='\033[1;35m'
NC='\033[0m' # No Color 
             
# Help message                                                       
Help(){
    echo                                                                
    printf "=%.0s" {1..114}; printf "\n"                                 
    echo -e "                ${RED}Usage:   $0  <Dataset>  <Year>  <Era>  <Output>${NC}" 
    printf "=%.0s" {1..114}; printf "\n"                                 
    echo
    echo "Dataset    ---> All / EGamma / Muon / SingleMuon / G-4Jets"    
    echo "Year       ---> 2022 / 2023"
    echo "Era        ---> C / D / E / F / G / Summer22 (Depending on the Year and Dataset: check Datasets.md)"   
    echo "Output     ---> Output directory to be created in /pnfs/iihe/cms/store/user/${USER}/JEC/<Year>/<Dataset>/Run<Era>/"
    printf "=%.0s" {1..114}; printf "\n"                                 
    echo                                                                
    exit 1                                                              
}

# Check number of arguments
if [ "$#" -ne 4 ]; then 
    Help                                           
fi

# Check if dataset name is correct and set the channel variable to be used later                                                    
# Use photon channel for the moment
dataset=$1                                                                                     
if ! [[ "$dataset" =~ ^(All|EGamma|Muon|SingleMuon|G-4Jets) ]]
then                                                                                     
    echo
    echo -e "${RED}Error : Invalid Dataset name!${NC}"                                                       
    Help
    exit 1                                                                                  
else
    case $dataset in
#        All)
#            channel=      
#            ;;
        EGamma)
            channel=Photon
            ;;
#        Muon)
#            channel=ZtoMuMu
#            ;;
#        SingleMuon)
#            channel=
#        G-Jets)
#            channel=
    esac
fi                                                                                          
    
# Check if year is correct
year=$2
if ! [[ "$year" =~ ^(2022|2023) ]]; then
    echo
    echo -e "${RED}Error : Invalid Year!${NC}"                                                       
    Help
    exit 1
fi

# To do: Check if era is correct (different eras per year) 
# Use carefully until then !!!
era=$3

# Prepare the output directory in personal pnfs store area
output=/pnfs/iihe/cms/store/user/${USER}/JEC/${year}/${dataset}/Run$era/$4
if [ ! -d $output ] 
then
    mkdir -p $output
else
    echo
    echo -e "${RED}The directory $output already exists, please give another Output name!${NC}"
    echo
    exit 1
fi

# Adapted to EGamma 2022 for the moment --> to be replaced for other years/channels.
if [[ "$year" -eq 2022 ]]; then
    #files="/pnfs/iihe/cms/ph/sc4/store/data/Run${year}${era}/${dataset}/NANOAOD/JMENano12p5-v1/70000/*.root" # Small subset of files
    files="/pnfs/iihe/cms/ph/sc4/store/data/Run${year}${era}/${dataset}/NANOAOD/JMENano12p5-v1/*/*.root"      # All files
fi

# Modify the template scripts and store the submitted files in the submission directory
# Template scripts
tmpexe="Template.sh"
tmpsub="Template.sub"

# New scripts where the parameters are set
newexe="$dataset"_"$year"_Run"$era".sh
newsub="$dataset"_"$year"_Run"$era".sub

# New executable script
sed 's@swpath@'$swpath'@g' $tmpexe > $newexe       # software path as set above
sed -i 's@subpath@'$subpath'@g' $newexe            # submission path as set above
sed -i 's@channel@'$channel'@g' $newexe            # channel as set above
chmod 744 $newexe

# New submission script
sed 's@exe.sh@'$newexe'@g' $tmpsub > $newsub        # executable name in the submit file
sed -i 's@path_to_output@'$output'@g' $newsub       # path for the output root files in the submit file
sed -i 's@list_of_files@'$files'@g' $newsub         # list of input files in the submit file

# Check whether the directory as set above exists. 
# Otherwise create it and move inside it to proceed with job submission.
if [ ! -d $jobpath ]; then
    mkdir $jobpath
fi

# New scripts will be moved inside the submission directory
mv $newexe ./${jobpath}
mv $newsub ./${jobpath}
cd ./${jobpath}

# Create directories error - log - output
if [ ! -d error ]; then
    mkdir error
fi
if [ ! -d log ]; then
    mkdir log
fi
if [ ! -d output ]; then
    mkdir output
fi

# Submit the jobs
condor_submit $newsub

# Print sumbission information
echo
printf "=%.0s" {1..120}; printf "\n"
echo -e "                                           ${PURPLE}Jobs submitted!${NC}"
printf "=%.0s" {1..120}; printf "\n"
echo
echo "The submission files can be found in: ${PWD}"
echo "The error/output/log files will be stored in: ${PWD}"
echo "The output root files will be stored in: $output"
printf "=%.0s" {1..120}; printf "\n"
echo
