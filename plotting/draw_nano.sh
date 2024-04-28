#!/bin/bash

for dir in "2022EG" "golden_2022EG" "2023B" "golden_2023B" "2023C" "golden_2023C" "all2023" "golden_all2023"
do
    # Using CMS OMS to get an approximation of the lumi:
    case $dir in
        "2023B")
            # 2023B: 1038.638 pb^-1
            lumi="1.04 fb^{-1}"
            ;;
        "2023C")
            # 2023C: 4292.837 pb^-1
            lumi="4.29 fb^{-1}"
            ;;
        "all2023")
            lumi="5 fb^{-1}"
            ;;
        *)
            lumi=""
            ;;
    esac

    python3 make_ZToMuMu_plots.py --dir $dir --lumi "$lumi"
    python3 make_ZToEE_plots.py --dir $dir --lumi "$lumi"
    python3 make_MuonJet_plots.py --dir $dir --lumi "$lumi"
    python3 make_PhotonJet_plots.py --dir $dir --lumi "$lumi"
done


