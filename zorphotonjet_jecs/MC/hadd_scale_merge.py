import ROOT
import os
import sys
import argparse
import numpy as np

from xs_mc import xs_gjets


def main():
    parser = argparse.ArgumentParser(
        description='''Scale all histos in a file to integrated lumi
        ''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    

    parser.add_argument("-d", "--directories", dest="directories", help="Input directories", nargs='+', type=str, default='')
    parser.add_argument("--norm", dest="norm", help="Name of the histo used to find the number of events", type=str, default='h_nvtx')
    parser.add_argument("-l", "--lumi", dest="lumi", help="Integrated lumi (in /pb)", type=str, default='1.0')
    parser.add_argument("-o", "--output", dest="output", help="Ouput file", type=str, default='')

    args = parser.parse_args()

    ## Get the directory containing the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    ## Loop over the directories e.g HT slices 
    str_listdir = ''
    for dr in args.directories:  

        ## Merge all root files in directory (if not yet done)
        merge   = f'cd {dr} && ' \
                  f'if [ -f all.root ]; then ' \
                  f'echo "The file all.root is already present in the directory \'{dr}\'" && cd -; ' \
                  f'else ' \
                  f'echo "Merging files root files in \'{dr}\'" && ' \
                  f'hadd all.root *.root && ' \
                  f'cd -; ' \
                  f'fi'

        os.system(merge)

        xs = 0
        for key in xs_gjets.keys():
            if key in dr:
                xs = xs_gjets[key]
                print(f"Using cross section '{xs}' for '{key}'")

        ## Scale histograms using scale_to_integrated_lumi.py and provided arguments
        os.system('cd ' + dr + '; python3 ' + script_dir + '/scale_to_integrated_lumi.py -i all.root --norm '+ args.norm + ' -l ' + args.lumi + ' --xs ' + format(xs))
        str_listdir = str_listdir + dr + "/all_rescaled.root "
 
   
    ## Merge all files together
    os.system("hadd " + args.output + " " + str_listdir )
    

if __name__ == '__main__':
    main() 
