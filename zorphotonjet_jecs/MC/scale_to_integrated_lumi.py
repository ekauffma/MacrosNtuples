import ROOT
import os
import sys
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser(
        description='''Scale all histos in a file to integrated lumi
        ''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    

    parser.add_argument("-i", "--input", dest="inputFiles", help="Input file", nargs='+', type=str, default='')
    parser.add_argument("--norm", dest="norm", help="Name of the histo used to find the number of events", type=str, default='h_nvtx')
    parser.add_argument("-l", "--lumi", dest="lumi", help="Integrated lumi (in /pb)", type=float, default=1.0)
    parser.add_argument("--xs", dest="xs", help="Cross section (in pb)", type=float, default=1.0)

    args = parser.parse_args()
    
    inputFiles = []
    outputFiles = []
    for i in args.inputFiles:
        inputFiles.append(ROOT.TFile(i,"read"))
        outputname = i.replace(".root","_rescaled.root")
        outputFiles.append(ROOT.TFile(outputname,"recreate"))

    
    for i, inputfile in enumerate(inputFiles):
        h_norm = inputfile.Get(args.norm)
        nentries = h_norm.GetEntries()
        integral = h_norm.Integral()

        for key in inputfile.GetListOfKeys():
            h = key.ReadObj()
            h.Scale(args.lumi/integral*args.xs)
            outputFiles[i].cd()
            h.Write()


if __name__ == '__main__':
    main()    
