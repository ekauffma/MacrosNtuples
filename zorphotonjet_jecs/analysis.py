from datetime import datetime
import time
import ROOT
import json
import os
import sys
import argparse


## Importing stuff from other python files
from helper import * 
from trigger import *


def main():


    ## Arguments 
    parser = argparse.ArgumentParser(
        description='''Jet energy correction studies with Z/photon+jets
        ''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--max_events",    dest="max_events", help="Maximum number of events to analyze. Default=-1 i.e. run on all events.", type=int,  default=-1)
    parser.add_argument("--JEC",           dest="JEC",        help="Apply the newest Jet Energy Corrections. When not added the jet raw pt is used", action='store_true')
    parser.add_argument("-i", "--input",   dest="inputFile",  help="Input file", type=str, default='')
    parser.add_argument("-o", "--output",  dest="outputFile", help="Output file", type=str, default='')
    parser.add_argument("-c", "--channel", dest="channel",    help=
                        '''Set channel:
                        -Photon
                        -ZToMuMu
                        -ZToEE
                        ''',
                        type=str, default='Photon')
    args = parser.parse_args() 


    ## Check if the channel is correct    
    if args.channel not in ['Photon','ZToMuMu','ZToEE']:
        print("Channel {} does not exist".format(args.channel))
        return 

    
    ## Define the default input files (JME custom nano) depending on the channel
    inputFile = args.inputFile
    if inputFile == '':
        if args.channel == 'Photon':
            inputFile = '/pnfs/iihe/cms/ph/sc4/store/data/Run2022C/EGamma/NANOAOD/JMENano12p5-v1/60000/7833bda9-26cd-40c6-812e-53ce7f77e99f.root'
        elif args.channel == 'ZToEE':
            inputFile = '/pnfs/iihe/cms/ph/sc4/store/data/Run2022C/EGamma/NANOAOD/JMENano12p5-v1/60000/7833bda9-26cd-40c6-812e-53ce7f77e99f.root'
        elif args.channel == 'ZToMuMu':
            inputFile = '/pnfs/iihe/cms/ph/sc4/store/data/Run2022C/Muon/NANOAOD/JMENano12p5-v1/70000/eb41ead3-897f-4759-926a-4d0366317478.root'


    ## Define the RDataFrame (Events branch) and print information
    df = ROOT.RDataFrame('Events', inputFile)    
    nEvents = df.Count().GetValue()

    if nEvents == 0:
        print('There are no events, exiting...')
        exit()
    
    print('There are {} events'.format(nEvents))
    

    # Max events to run on 
    max_events = min(nEvents, args.max_events) if args.max_events >=0 else nEvents
    df = df.Range(0, max_events)
    # Next line to monitor event loop progress
    df = df.Filter('if(tdfentry_ %100000 == 0) {cout << "Event is: " << tdfentry_ << endl;} return true;')


    ## Output root file definition
    if args.outputFile == '':
        args.outputFile = 'output_'+args.channel+'.root'
    out = ROOT.TFile(args.outputFile, "recreate")

 
    ## Apply the MET filters 
    df = df.Filter('Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadPFMuonDzFilter') 
  
 
    ## Initialize the list of triggers present in the input file
    triggers = TriggerInit(df, args.channel)


    ## Do the analysis depending on the channel
    if args.channel == 'Photon':
           
        df = SinglePhotonSelection(df, triggers) 
        
        df = CleanJets(df, args.JEC)
        
        df = PtBalanceSelection(df)
        
        df, all_histos_balance = AnalyzePtBalance(df, args.JEC)
        
        df_report = df.Report()
        
        for i in all_histos_balance:
            # To do: Create alpha directories and put the corresponding histograms inside
            all_histos_balance[i].GetValue().Write()

        df_report.Print()
        

if __name__ == '__main__':
    #start = time.time()  # Uncomment to check the execution time
    main()
    #end = time.time()    # Uncomment to check the execution time
    #print('The time of execution was: ', '{:.2f}'.format((end-start)/60.), ' min') # Uncomment to check the execution time
