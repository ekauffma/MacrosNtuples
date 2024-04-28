# Script for L1 studies 

## Introduction 

This folder contains several scripts: 

- ```performances.py, performances_nano.py```: for L1T performances studies of the various objects (efficiency, response, resolution, pre/postfiring). 

- ```rate.py```: for L1 menu rate estimate vs PU, using HLTPhysics or ZeroBias (use the latter unless you know what you do!). The script allows you to define your customized menu. 

For 2022 data, the inputs are customized IIHE-CMS ntuples (https://github.com/iihe-cms-sw/GenericTreeProducerMINIAOD) but can fairly easily be adapted to run on L1 ntuples or custom NANO containing L1 objects/decisions. 

For example ```performances_L1NTuples.py``` is a simplified version of ```performances.py```, adapted to run on L1Ntuples.  

For 2023 data, as L1 objects were added to NANO, new scripts were added to run directly on NANO inputs.

## L1T performances:  ```performances.py``` 

The code produces and stores various histograms such as numerators and denominators for efficiency, 2D histograms of pt(L1)/pt(reco) vs variable(s) of interest for response/resolution, etc. At the moment, four channels/analyses are considered: 

- ```ZToMuMu``` : Tag and Probe with pairs of muons from a Z decay. Used for L1Mu performance studies. 
- ```ZToEE``` : Tag and Probe with pairs of electrons from a Z decay. Used for L1EG performance studies. 
- ```MuonJet``` : Muon+jet selection using the (Single)Muon dataset. For L1 jet/MET performance studies.
- ```PhotonJet``` : Photon+jet selection using the EGamma dataset. For L1 jet performance studies. This channel is complementary with ```MuonJet``` as it allows to collec more statistits for high pt jets. 

### 2022 setup

The code can be run using the following command: 

``` python3 performances.py -i INPUTFILE -o OUTPUTFILE -c CHANNEL --max_events MAX_EVENTS```

### 2023 setup

The code can be run using the following command: 
 
``` python3 performances_nano.py -i INPUTFILE -o OUTPUTFILE -c CHANNEL --max_events MAX_EVENTS --config CONFIG_CARD```

The script for the 2023 setup takes one extra argument, a configuration card in YAML,
that can be used to modify the histograms produced, or to only produce some of them.
If the `--config` argument is not passed, the default card for that channel is used.
The default card are stored in `MacrosNtuples/config_cards/`. 
These contain comments on how to use them.

### Submission to condor

`performances.py` and `performances_nano.py` can also be run on condor.

For the 2022 setup: 
```
cd condorsubmission/
sh SubmitToCondor.sh OUTPUTDIR CHANNEL 'list of files'
```

For the 2023 setup: 
```
cd condorsubmission/
sh SubmitToCondor_nano.sh OUTPUTDIR CHANNEL 'list of files'
```

in `condorsubmission/`, you can also find the `submit_all.sh` script, that will 
submit jobs for all of 2022, and all skims,
and `submit_nano.sh` that will submit all jobs for 2023.

### Plotting the results

The code for the last step, computing and plotting efficiencies... etc., is available in the plotting folder: 

```
cd ../plotting
```
Assuming you ran the previous step for the ```MuonJet``` channel and that your histos are saved in ```file.root```, here's an example command to compute and draw the L1 jet efficiency for various thresholds in the barrel:
```
python3 drawplots.py -t efficiency --saveplot True' -i file.root \
--num h_Jet_plots_eta0p0to1p3_l1thrgeq30p0 h_Jet_plots_eta0p0to1p3_l1thrgeq40p0 h_Jet_plots_eta0p0to1p3_l1thrgeq60p0\
h_Jet_plots_eta0p0to1p3_l1thrgeq80p0 h_Jet_plots_eta0p0to1p3_l1thrgeq100p0 h_Jet_plots_eta0p0to1p3_l1thrgeq120p0\ 
h_Jet_plots_eta0p0to1p3_l1thrgeq140p0 h_Jet_plots_eta0p0to1p3_l1thrgeq160p0 h_Jet_plots_eta0p0to1p3_l1thrgeq180p0\
h_Jet_plots_eta0p0to1p3_l1thrgeq200p0\
--den h_Jet_plots_eta0p0to1p3 --xtitle 'p_{T}^{jet}(reco) (GeV)' --ytitle 'L1 Efficiency'\
--legend 'p_{T}^{L1}>30 GeV' 'p_{T}^{L1}>40 GeV' 'p_{T}^{L1}>60 GeV' 'p_{T}^{L1}>80 GeV' 'p_{T}^{L1}>100 GeV'\
'p_{T}^{L1}>120 GeV' 'p_{T}^{L1}>140 GeV' 'p_{T}^{L1}>160 GeV' 'p_{T}^{L1}>180 GeV' 'p_{T}^{L1}>200 GeV'\
--extralabel '#splitline{>=1 tight muon (p_{T}>27 GeV), pass HLT_IsoMu24}{#color[4]{0<|#eta^{jet}(reco)|<1.3}}'\
--plotname L1Jet_FromSingleMuon_TurnOn_barrel
```

You can find more explanations in `MacrosNtuples/plotting/README.md`.

This step is the same for both the 2022 and 2023 setups
 

## Rate studies  ```rate.py``` 
The code does essentially two things: 
- Define various customized L1 menus, starting from an existing menu (that can be empty), enabling/disabling some existing L1 bits, and adding customized seeds. 
- Run over some data files and save into a histogram the PU distribution for all processed events, all events passing a given menu, as well as events passing a reference L1 seed (currently L1_SingleMu22, only relevant for HLTPhysics studies).  


The code can be run using the following command: 

```python3 rate.py -i INPUTFILE -o OUTPUTFILE -m L1MENUCSV -d DATASET --max_events MAX_EVENTS```
 
It can also be run on condor. 

```
cd condorsubmission/
#Adapt scriptrate.sub to your needs and then: 
condor_submit scriptrate.sub 
```

The code for the last step, computing and plotting rates is available in the plotting folder: 

```
cd ../plotting
```
Assuming you ran the previous step for the ```ZeroBias``` dataset and that your histos are saved in ```file.root```, here's an example command to compute and draw the rate of two example menus whose passing event counts are stored in ```HISTONAME_1``` and ```HISTONAME_2```:
```
python3  drawplots_l1rate.py -i file.root  --histos HISTONAME_1 HISTONAME_2 ... --hlumis h_lsprocessed_vs_pu --href  h_allevents_vs_pu  -d ZeroBias
```


## Tests (to run before opening a pull request)
In ```l1macros``` folder: 
```
sh runtests >> log_runtests
```

