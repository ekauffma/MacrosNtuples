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
    echo -e "${RED}1)                Usage:   $0  <Dataset>  <Year>  <Era>  <Output>  <Nano>${NC}"
    printf "=%.0s" {1..114}; printf "\n"                                 
    echo
    echo "Dataset            ---> EGamma / Muon / SingleMuon / G-4Jets"
    echo "Year               ---> 2022 / 2023"
    echo "Era or HT bin (MC) ---> CDEFG || XXtoYY  MC (Depending on the Year and Dataset: check Datasets.md)"
    echo "Output             ---> Output directory to be created in /pnfs/iihe/cms/store/user/${USER}/JEC/<Year>/<Dataset>/Run<Era>/"
    echo "Nano               ---> JMENano / Nano"
    echo
    echo -e "                                                 \033[1m OR \033[0m                                                               "
    echo
    printf "=%.0s" {1..114}; printf "\n"
    echo -e "${RED}2)                Usage:   $0 -f input.txt${NC}"
    printf "=%.0s" {1..114}; printf "\n"
    echo
    echo "input.txt  ---> Inputs folder"
    echo                                                                
    exit 1                                                              
}

# Check number of arguments: 5 if provided from the terminal, 2 if provided by input file
if [ "$#" -ne 5 ] && [ "$#" -ne 2 ]; then
    Help
    exit 1
fi

# If the number is 5, we initialize the variables from the values provided through the terminal
if [ "$#" -eq 5 ]; then
   dataset=$1
   year=$2
   era=$3
   folder=
   files=$5
# If the number is 2, then we initialize the variables from the values stored in the input file
elif [ "$#" -eq 2 ] && [ "$1" = "-f" ]; then
   infile="$2"
   if [ ! -f "$infile" ]; then
      echo
      echo -e "${RED}Error : Input file not found: $infile ${NC}"
      exit 1
   fi

   # Read the arguments from the file and store them in an array
   args=($(<"$infile"))

   # Check if the number of arguments is at least 5
   if [ ${#args[@]} -lt 5 ]; then
      echo "${RED}Error: Insufficient arguments in the input file. ${NC}"
      exit 1
   fi

   # Assign the arguments to the variables
   dataset=${args[0]}
   year=${args[1]}
   era=${args[2]}
   folder="${args[3]}_$(date '+%Y%m%d_%H%M%S')"
   files=${args[4]}
else
   Help
   exit 1
fi

# Check if dataset name is correct and set the channel variable to be used later                                                    
# Use photon channel for the moment
if ! [[ "$dataset" =~ ^(EGamma|Muon|SingleMuon|G-4Jets) ]]
then                                                                                     
    echo
    echo -e "${RED}Error : Invalid Dataset name!${NC}"                                                       
    Help
    exit 1                                                                                  
else
    case $dataset in
        EGamma)
            channel=Photon
            ;;
        Muon)
            channel=ZtoMuMu
#            channel=ZtoEE
            ;;
#        SingleMuon)
#            channel=
        G-Jets)
            channel=Photon
            ;;
        # Default channel below
        *)
            channel=Photon
            ;;
    esac
fi                                                                                          
    
# Check if year is correct
if ! [[ "$year" =~ ^(2022|2023) ]]; then
    echo
    echo -e "${RED}Error : Invalid Year!${NC}"                                                       
    Help
    exit 1
fi

# Check if era (depending on the year) or HT bin is correct
if [[ $year == 2022 && $dataset == "EGamma" ]]; then
   if ! [[ "$era" =~ ^(C|D|E|F|G) ]]; then
      echo -e "${RED}Error : Invalid era for year 2022!${NC}"
      echo -e "${RED}2022 eras : C D E F G${NC}"
      Help
      exit 1
   fi
elif [[ $year == 2022 && $dataset == "G-4Jets" ]]; then
   if ! [[ "$era" == "40to70" || "$era" == "70to100" || "$era" == "100to200" || "$era" == "200to400" || "$era" == "400to600" || "$era" == "600" ]]; then
      echo -e "${RED}Error : Invalid HT bin${NC}"
      echo -e "${RED} 40to70, 70to100, 100to200, 200to400, 400to600, 600 ${NC}"
      Help
      exit 1
   fi
elif [[ $year == 2023 && $channel == "Photon" ]]; then
   if ! [[ "$era" =~ ^(C|D) ]]; then
      echo -e "${RED}Error : Invalid era for year 2023!${NC}"
      echo -e "${RED}2022 eras : C D${NC}"
      Help
      exit 1
   fi
elif [[ $year == 2023 && $dataset == "G-4Jets" ]]; then
   if ! [[ "$era" == "40to70" || "$era" == "70to100" || "$era" == "100to200" || "$era" == "200to400" || "$era" == "400to600" || "$era" == "600" ]]; then
      echo -e "${RED}Error : Invalid HT bin${NC}"
      echo -e "${RED} 40to70, 70to100, 100to200, 200to400, 400to600, 600 ${NC}"
      Help
      exit 1
   fi
fi

# The output directory in personal pnfs store area
output=/pnfs/iihe/cms/store/user/${USER}/JEC/${year}/${dataset}/Run$era/$folder

# Check if it's Data or MC
isData=true
if [[ $dataset == "G-4Jets" ]]; then
   isData=false
   output=/pnfs/iihe/cms/store/user/${USER}/JEC/${year}/${dataset}/HT_$era/$folder 
fi

if [ ! -d $output ] 
then
    mkdir -p $output
else
    echo
    echo -e "${RED}The directory $output already exists, please give another Output name!${NC}"
    echo
    exit 1
fi

# Running on NANOAOD or JME custom NANOAOD based on the last argument
if [[ $files == "JMENano" ]]; then
   # This is for JME custom NanoAOD
   # Data
   if [[ "$isData" == true ]]; then
      #files="/pnfs/iihe/cms/ph/sc4/store/data/Run${year}${era}/${dataset}/NANOAOD/JMENano12p5-v1/70000/*.root" # Small subset of files
      files="/pnfs/iihe/cms/ph/sc4/store/data/Run${year}${era}/${dataset}/NANOAOD/JMENano12p5-v1/*/*.root"      # All files
   # MC
   else
      files="/pnfs/iihe/cms/ph/sc4/store/mc/Run3Summer22NanoAODv12/G-4Jets_HT-${era}_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/JMENano12p5_132X_mcRun3_2022_realistic_v*/*/*.root"      # All files
   fi
elif [[ $files == "Nano" ]]; then
   # TODO: This is for CMS NanoAOD
   #files="/pnfs/iihe/cms/ph/sc4/store/data/Run${year}${era}/${dataset}/NANOAOD/JMENano12p5-v1/70000/*.root" # Small subset of files
   files="/pnfs/iihe/cms/ph/sc4/store/data/Run${year}${era}/${dataset}/NANOAOD/JMENano12p5-v1/*/*.root"      # All files
else
    echo -e "${RED}Select either Nano of JMENano for the last argument!${NC}"
    Help
    exit 1
fi

# Modify the template scripts and store the submitted files in the submission directory
# Template scripts
tmpexe="Template.sh"
tmpsub="Template.sub"

# New scripts where the parameters are set
newexe="$dataset"_"$year"_Run"$era".sh
newsub="$dataset"_"$year"_Run"$era".sub

# New executable script
sed 's@SUBPATH@'$subpath'@g' $tmpexe > $newexe     # submission path as set above
sed -i 's@CHANNEL@'$channel'@g' $newexe            # channel as set above
sed -i 's@YEAR@'$year'@g' $newexe                  # year as set above
sed -i 's@ERA@'$era'@g' $newexe                    # era as set above
if [[ "$isData" == false ]]; then
   sed -i 's@--isData @@g' $newexe                  # Data or MC as set above
fi
chmod 744 $newexe

# New submission script
sed 's@exe.sh@'$newexe'@g' $tmpsub > $newsub       # executable name in the submit file
sed -i 's@PATH_TO_OUTPUT@'$output'@g' $newsub      # path for the output root files in the submit file
sed -i 's@LIST_OF_FILES@'$files'@g' $newsub        # list of input files in the submit file

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
