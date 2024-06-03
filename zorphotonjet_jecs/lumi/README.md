# 💹 Luminosities recorded by the triggers of interest per era/year

- Calculation based on [brilcalc tool](https://twiki.cern.ch/twiki/bin/viewauth/CMS/BrilcalcQuickStart#Getting_started_without_requirin)
- Json files (per-era) from `/eos/user/c/cmsdqm/www/CAF/certification/` 
- Example for photon unprescaled triggers:
```bash
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -u /pb -i Cert_Collisions2022_eraC_355862_357482_Golden.json --hltpath "HLT_Photon110EB_TightID_TightIso*" -o eraC.csv
```

⚠️ Check also recommendations from [PdmV](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis)
