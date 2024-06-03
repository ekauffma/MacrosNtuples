from ROOT import TFile, TH1F, TH2, TCanvas, gDirectory, gStyle, gROOT, gPad
from ROOT import TAttMarker, TColor
from ROOT import kBlack, kBlue, kRed
from array import array
import os
import sys

gROOT.SetBatch(True)

sys.path.insert(1, '../..') # for importing the binning from another directory
from binning import *

# Input file : TODO Make it an argument
infile = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunC/alpha_exclusive/cor_pt/All.root')

# Get the 2D histograms with the pt balance and create the Y projections
keys = infile.GetListOfKeys()
h_ptBalance = [] # Full list of histos for each eta, alpha and pt bin
h_ptBalance_vs_refpt = [] # Full list of histos for each eta, alpha and pt bin (To be used later for plotting)

# Below we create a dictionary which contains lists
# Each list will correspond to all the different alpha values for each eta and pT bin 
str_binetas_pts = []
for e in str_binetas:
    for p in str_binpts:
        str_binetas_pts.append(e + p) # These will be the keys of the dictionary 
#print('Keys of the dictionary: ', str_binetas_pts)

h_ptBalance_per_eta_per_pt = dict([(k, []) for k in str_binetas_pts])

# Read all the histograms and put them in the lists/dictionary
# TODO : Improve a bit here (unnecessary loops)
for key in keys:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt.append(histo2D.ProfileX())
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     h_ptBalance_per_eta_per_pt[e+p].append(histo2D.ProjectionY())

# Print the lists for checks
#print('Full list of histos: ')
#for h in range(len(h_ptBalance)):
#    print(h_ptBalance[h])
#print('Dictionary with lists: ')
#for etapt, histo in h_ptBalance_per_eta_per_pt.items():
#    print(f'Key: {etapt}')
#    for histoname in histo:
#        print(f'Histogram: {histoname}')

# First create canvases with all the pt balance plots for all eta and alpha bins
dir0 = 'jet_response'
os.makedirs(dir0, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for a in range(NalphaBins):
        str2='[' + str("{:.2f}".format(alphaBins[a])) + ',' + str("{:.2f}".format(alphaBins[a+1])) +')'
        for p in range(NptBins):
            str3 = '[' + str(jetptBins[p]) + ',' + str(jetptBins[p+1]) + ')'

            c = TCanvas(str1 + ',' + str2 + ',' + str3, str1 + ',' + str2 + ',' + str3, 1000, 1000)
            h_ptBalance[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2 + ', ' + 'p_{T}^{#gamma}=' + str3)
            h_ptBalance[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
            h_ptBalance[index].GetXaxis().SetTitleOffset(1.2)
            h_ptBalance[index].GetYaxis().SetTitle('Events')
            h_ptBalance[index].GetYaxis().SetLabelSize(0.03)
            h_ptBalance[index].GetYaxis().SetTitleOffset(1.5)
            h_ptBalance[index].Draw()

            c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.png')
##            #c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.pdf')
            index += 1

# Then create canvases with all the pt balance plots vs pt_ref for all eta and alpha bins
dir1 = 'jet_response_vs_refpt'
os.makedirs(dir1, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for a in range(NalphaBins):
        str2='[' + str("{:.2f}".format(alphaBins[a])) + ',' + str("{:.2f}".format(alphaBins[a+1])) +')'

        #print('Adding histograms to: ', h_ptBalance_vs_refpt[index].GetName())
        # Here we add all the different pt histograms such that we have one histogram per eta and alpha bin
        for p in range(NptBins-1):
            h_ptBalance_vs_refpt[index].Add(h_ptBalance_vs_refpt[index+p+1])
            #print(' adding: ', h_ptBalance_vs_refpt[index+p+1].GetName())

        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        gStyle.SetOptStat(0)
        gPad.SetLogx()
        h_ptBalance_vs_refpt[index].GetXaxis().SetMoreLogLabels()
        h_ptBalance_vs_refpt[index].GetXaxis().SetNoExponent()
        h_ptBalance_vs_refpt[index].SetMaximum(1.15)
        h_ptBalance_vs_refpt[index].SetMinimum(0.75)
        h_ptBalance_vs_refpt[index].SetMarkerStyle(8)
        h_ptBalance_vs_refpt[index].SetMarkerSize(1.4)
        h_ptBalance_vs_refpt[index].SetMarkerColor(kBlue+1)
        h_ptBalance_vs_refpt[index].SetLineColor(kBlue+1)
        h_ptBalance_vs_refpt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2)
        h_ptBalance_vs_refpt[index].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')
        h_ptBalance_vs_refpt[index].GetXaxis().SetTitleOffset(1.3)
        h_ptBalance_vs_refpt[index].GetYaxis().SetTitle('p_{T} balance')
        h_ptBalance_vs_refpt[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_vs_refpt[index].GetYaxis().SetTitleOffset(1.4)
        h_ptBalance_vs_refpt[index].Draw()

        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
        index += NptBins

# Then for each eta and each pt bin we take the mean (pt balance) and draw it as a function of alpha
# Here we use the dictionary with the lists of histograms
dir2 = 'jet_response_vs_alpha'
os.makedirs(dir2, exist_ok = True)

h_means = {}  #Dictionary with the mean values
h_errors = {} #Dictionary with the mean value errors

for etapt, histo in h_ptBalance_per_eta_per_pt.items():
    mean_values = []
    mean_errors = []
    # Create the lists with means and errors 
    for histogram in histo:
        mean_values.append(histogram.GetMean())     
        mean_errors.append(histogram.GetMeanError())     
    # Store the lists in the dictionaries using the same keys
    h_means[etapt] = mean_values
    h_errors[etapt] = mean_errors

# Print mean values for tests
#for k,v in h_means.items():
#    print(f'Key: {k}')
#    for value in v:
#        print(f'Mean: {value}')

# Create a list with the final histograms jet response vs alpha for each eta, pt bin
h_jetresponse = []
for (etapt1,mean), (etapt2,error) in zip(h_means.items(), h_errors.items()):
    h = TH1F(etapt1, etapt1, NalphaBins, alphaBins)
    ibin = 1
    for m,e in zip(mean,error):
        h.SetBinContent(ibin, m)
        h.SetBinError(ibin, e)
        ibin +=1 
    h_jetresponse.append(h)

# Print the lists for checks
#print('List of histos with pt balance vs alpha: ')
#for h in range(len(h_jetresponse)):
#    print(h_jetresponse[h])

# Draw of the above histograms
index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for p in range(NptBins):
        str2 = '[' + str(jetptBins[p]) + ',' + str(jetptBins[p+1]) + ')'

        c = TCanvas(str1+str2, str1+str2, 1000, 1000)
        gStyle.SetOptStat(0)
        h_jetresponse[index].SetMarkerStyle(8)
        h_jetresponse[index].SetMarkerSize(1.4)
        h_jetresponse[index].SetMarkerColor(kBlue+1)
        h_jetresponse[index].SetLineColor(kBlue+1)
        h_jetresponse[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + 'p_{T}^{#gamma}=' + str2)
        h_jetresponse[index].GetXaxis().SetTitle('#alpha')
        h_jetresponse[index].GetXaxis().SetTitleSize(0.045)
        h_jetresponse[index].GetXaxis().SetTitleOffset(1.0)
        h_jetresponse[index].GetYaxis().SetTitle('p_{T} balance')
        h_jetresponse[index].GetYaxis().SetTitleSize(0.045)
        h_jetresponse[index].GetYaxis().SetLabelSize(0.035)
        h_jetresponse[index].GetYaxis().SetTitleOffset(1.0)
        h_jetresponse[index].Draw()

        c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.png')
        #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.pdf')
        index += 1
