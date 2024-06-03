# 📜 Scripts for JEC studies


## 💻 Running the code
### ❗Prerequisite (for T2B)
```bash
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_103 x86_64-centos7-gcc12-opt
```

### :bulb: Check the available options  
```bash 
python3 analysis.py --help
```

### 🔍 Run locally (1 input root file, eg Photon channel) 
```bash 
python3 analysis.py -o output.root -c Photon --max_events -1 --year 2022 --era C --isData --JEC
```

### 🖱️ Submit jobs with HTCondor
Check the directory ```HTCondor```
