#!/bin/bash

for run in '2023B' '2023C'
do
    for skim in 'Muon','ZToMuMu' 'Muon','MuonJet' 'EGamma','ZToEE' 'EGamma','PhotonJet'
    do
        IFS=','
        set $skim
        case $run in
            "2023B")
                dir=/pnfs/iihe/cms/ph/sc4/store/data/Run$run/$1?/NANOAOD/PromptNanoAODv11p9_v1-v?
                golden='Cert_Collisions2023_eraB_366403_367079_Golden.json'
                ;;

            "2023C")
		# a bit of globbing to take directories v11p9_v1-v1, v12_v2-v2 and v12_v4-v1, but not v12_v3-v1
                dir=/pnfs/iihe/cms/ph/sc4/store/data/Run$run/$1?/NANOAOD/PromptNanoAODv*_v[!3]*
                golden='Cert_Collisions2023_eraC_367095_368224_Golden.json'
                ;;
	    
           "2022Nano")
                dir=/pnfs/iihe/cms/store/user/lathomas/$1/Run2022G-PromptReco-v1_NANOAODv11p9/230619_*/
                golden='Cert_Collisions2022_355100_362760_Golden.json'
                ;;

            "2018Nano")
                dir=/pnfs/iihe/cms/store/user/lathomas/*$1/Run2018D-UL2018_MiniAODv2_GT36-v?_NANOAODv11p9/230620_*/
                golden='Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
                ;;
            *)
                dir=''
                golden=''
                ;;
        esac


        echo $run $2
        sh SubmitToCondor_nano.sh outdir/"$run"/outputcondor_"$2" "$2" "$dir/*/*.root"
        
	if  [ ! -z $golden ]
        then 
            sh SubmitToCondor_nano.sh outdir/golden_"$run"/outputcondor_"$2" "$2" "$dir/*/*.root" $golden
        fi
    done
done
