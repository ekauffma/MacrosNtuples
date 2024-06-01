# 📊 Normalization of Monte Carlo samples

- [xs_mc](xs_mc.py) contains the cross sections for the different samples and (H<sub>T</sub>/p<sub>T</sub>/...) slices per sample.
- [scale_to_integrated_lumi](scale_to_integrated_lumi.py) is called from [hadd_scale_merge](hadd_scale_merge.py)
  for normalization to the integrated luminosity of the data.
- [hadd_scale_merge](hadd_scale_merge.py) is the main executable to be run as:
  ```bash 
  python3 hadd_scale_merge.py -d /pnfs/iihe/cms/store/user/gparaske/JEC/2022/G-4Jets/G-4Jets_HT* -l 38000 -o G-4Jets.root
  ```
  ❗Adapt input folder(s) path `(-d)`, luminosity `(-l)` and output filename `(-o)`
  
  1. Merges all the root files in each sub-directory to one file (per sub-directory) `all.root`.
  2. Normalizes each `all.root` file to the cross section from [xs_mc](xs_mc.py) and creates
     the new file (per sub-directory) `all_rescaled.root`.
  4. Normalizes to the integrated luminosity by calling [scale_to_integrated_lumi](scale_to_integrated_lumi.py).
  5. Stores the output to the final output root file.
