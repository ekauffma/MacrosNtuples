from ROOT import TFile, TH1F, TH2, TCanvas, TLegend, gDirectory, gStyle, gROOT, gPad
from ROOT import TAttMarker, TColor, TLine
from ROOT import kBlack, kBlue, kRed
from array import array
import os
import sys

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetLineWidth(2)

sys.path.insert(1, '../..') # for importing the binning from another directory
from binning import *

# Input file : TODO Make it an argument
infile_cor = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunC/alpha_exclusive/cor_pt/All.root')
infile_raw = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunC/alpha_exclusive/raw_pt/All.root')

# Get the 2D histograms with the pt balance and create the Y projections
# Cor_pt
keys_cor = infile_cor.GetListOfKeys()
h_ptBalance_cor = [] # Full list of histos for each eta, alpha and pt bin
h_ptBalance_vs_refpt_cor = [] # Full list of histos for each eta, alpha and pt bin (To be used later for plotting)
# Raw_pt
keys_raw = infile_raw.GetListOfKeys()
h_ptBalance_raw = [] # Full list of histos for each eta, alpha and pt bin
h_ptBalance_vs_refpt_raw = [] # Full list of histos for each eta, alpha and pt bin (To be used later for plotting)

# Below we create a dictionary which contains lists
# Each list will correspond to all the different alpha values for each eta and pT bin 
str_binetas_pts = []
for e in str_binetas:
    for p in str_binpts:
        str_binetas_pts.append(e + p) # These will be the keys of the dictionary 
#print('Keys of the dictionary: ', str_binetas_pts)

# Cor_pt
h_ptBalance_per_eta_per_pt_cor = dict([(k, []) for k in str_binetas_pts])
# Raw_pt
h_ptBalance_per_eta_per_pt_raw = dict([(k, []) for k in str_binetas_pts])

# Read all the histograms and put them in the lists/dictionary
# TODO : Improve a bit here (unnecessary loops)
# Cor_pt
for key in keys_cor:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance_cor.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt_cor.append(histo2D.ProfileX())
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     h_ptBalance_per_eta_per_pt_cor[e+p].append(histo2D.ProjectionY())

# Raw_pt
for key in keys_raw:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance_raw.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt_raw.append(histo2D.ProfileX())
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     h_ptBalance_per_eta_per_pt_raw[e+p].append(histo2D.ProjectionY())

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
            h_ptBalance_cor[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2 + ', ' + 'p_{T}^{#gamma}=' + str3)
            h_ptBalance_raw[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2 + ', ' + 'p_{T}^{#gamma}=' + str3)
            h_ptBalance_raw[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma} (GeV)')
            h_ptBalance_raw[index].GetXaxis().SetTitleOffset(1.2)
            h_ptBalance_raw[index].GetYaxis().SetTitle('Events')
            h_ptBalance_raw[index].GetYaxis().SetLabelSize(0.03)
            h_ptBalance_raw[index].GetYaxis().SetTitleOffset(1.5)
            h_ptBalance_cor[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma} (GeV)')
            h_ptBalance_cor[index].GetXaxis().SetTitleOffset(1.2)
            h_ptBalance_cor[index].GetYaxis().SetTitle('Events')
            h_ptBalance_cor[index].GetYaxis().SetLabelSize(0.03)
            h_ptBalance_cor[index].GetYaxis().SetTitleOffset(1.5)
            h_ptBalance_raw[index].SetLineColor(kRed+1)
            h_ptBalance_cor[index].SetLineColor(kBlue+1)

            m_raw = h_ptBalance_raw[index].GetMaximum()
            m_cor = h_ptBalance_cor[index].GetMaximum()
        
            m = 0.
            if ( m_raw > m_cor):
               m = m_raw
               h_ptBalance_raw[index].Draw()
               h_ptBalance_cor[index].Draw('same')
            else:
               m = m_cor
               h_ptBalance_cor[index].Draw()
               h_ptBalance_raw[index].Draw('same')
             
            leg = TLegend(0.65,0.75,0.95,0.90)
            leg.AddEntry(h_ptBalance_raw[index], "raw p_{T}", "l")
            leg.AddEntry(h_ptBalance_cor[index], "cor p_{T}", "l")
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.Draw()

            l = TLine(1.0,0.0,1.0,m)
            l.SetLineStyle(2)
            l.Draw()

            c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.png')
            #c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.pdf')
            c.Update()
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
            h_ptBalance_vs_refpt_raw[index].Add(h_ptBalance_vs_refpt_raw[index+p+1])
            h_ptBalance_vs_refpt_cor[index].Add(h_ptBalance_vs_refpt_cor[index+p+1])
            #print(' adding: ', h_ptBalance_vs_refpt[index+p+1].GetName())

        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        gStyle.SetOptStat(0)
        gPad.SetLogx()
        h_ptBalance_vs_refpt_cor[index].GetXaxis().SetMoreLogLabels()
        h_ptBalance_vs_refpt_cor[index].GetXaxis().SetNoExponent()
        h_ptBalance_vs_refpt_cor[index].SetMaximum(1.25)
        h_ptBalance_vs_refpt_cor[index].SetMinimum(0.5)
        h_ptBalance_vs_refpt_raw[index].SetMarkerStyle(8)
        h_ptBalance_vs_refpt_raw[index].SetMarkerSize(1.4)
        h_ptBalance_vs_refpt_raw[index].SetMarkerColor(kRed+1)
        h_ptBalance_vs_refpt_raw[index].SetLineColor(kRed+1)
        h_ptBalance_vs_refpt_cor[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2)
        h_ptBalance_vs_refpt_cor[index].GetXaxis().SetTitle('p_{T}^{#gamma}')
        h_ptBalance_vs_refpt_cor[index].GetXaxis().SetTitleOffset(1.3)
        h_ptBalance_vs_refpt_cor[index].GetYaxis().SetTitle('p_{T} balance')
        h_ptBalance_vs_refpt_cor[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_vs_refpt_cor[index].GetYaxis().SetTitleOffset(1.4)
        h_ptBalance_vs_refpt_cor[index].SetMarkerStyle(8)
        h_ptBalance_vs_refpt_cor[index].SetMarkerSize(1.4)
        h_ptBalance_vs_refpt_cor[index].SetMarkerColor(kBlue+1)
        h_ptBalance_vs_refpt_cor[index].SetLineColor(kBlue+1)
        h_ptBalance_vs_refpt_cor[index].Draw()
        h_ptBalance_vs_refpt_raw[index].Draw('same')
        
        leg = TLegend(0.65,0.75,0.95,0.90)
        leg.AddEntry(h_ptBalance_vs_refpt_raw[index], "raw p_{T}", "l")
        leg.AddEntry(h_ptBalance_vs_refpt_cor[index], "cor p_{T}", "l")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw()

        l = TLine(0.0,1.0,1000,1.0)
        l.SetLineStyle(2)
        l.Draw()

        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
        index += NptBins

# Then for each eta and each pt bin we take the mean (pt balance) and draw it as a function of alpha
# Here we use the dictionary with the lists of histograms
dir2 = 'jet_response_vs_alpha'
os.makedirs(dir2, exist_ok = True)

h_means_raw = {}  #Dictionary with the mean values
h_errors_raw = {} #Dictionary with the mean value errors

for etapt_r, histo_r in h_ptBalance_per_eta_per_pt_raw.items():
    mean_values = []
    mean_errors = []
    # Create the lists with means and errors 
    for histogram_r in histo_r:
        mean_values.append(histogram_r.GetMean())     
        mean_errors.append(histogram_r.GetMeanError())     
    # Store the lists in the dictionaries using the same keys
    h_means_raw[etapt_r] = mean_values
    h_errors_raw[etapt_r] = mean_errors

h_means_cor = {}  #Dictionary with the mean values
h_errors_cor = {} #Dictionary with the mean value errors

for etapt_c, histo_c in h_ptBalance_per_eta_per_pt_cor.items():
    mean_values = []
    mean_errors = []
    # Create the lists with means and errors 
    for histogram_c in histo_c:
        mean_values.append(histogram_c.GetMean())     
        mean_errors.append(histogram_c.GetMeanError())     
    # Store the lists in the dictionaries using the same keys
    h_means_cor[etapt_c] = mean_values
    h_errors_cor[etapt_c] = mean_errors

# Print mean values for tests
#for k,v in h_means.items():
#    print(f'Key: {k}')
#    for value in v:
#        print(f'Mean: {value}')

# Create a list with the final histograms jet response vs alpha for each eta, pt bin
h_jetresponse_raw = []
for (etapt1,mean), (etapt2,error) in zip(h_means_raw.items(), h_errors_raw.items()):
    h = TH1F(etapt1+'_raw', etapt1+'_raw', NalphaBins, alphaBins)
    ibin = 1
    for m,e in zip(mean,error):
        h.SetBinContent(ibin, m)
        h.SetBinError(ibin, e)
        ibin +=1 
    h_jetresponse_raw.append(h)
    h.Delete

h_jetresponse_cor = []
for (etapt1,mean), (etapt2,error) in zip(h_means_cor.items(), h_errors_cor.items()):
    h = TH1F(etapt1+'_cor', etapt1+'_cor', NalphaBins, alphaBins)
    ibin = 1
    for m,e in zip(mean,error):
        h.SetBinContent(ibin, m)
        h.SetBinError(ibin, e)
        ibin +=1 
    h_jetresponse_cor.append(h)

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
        h_jetresponse_raw[index].SetMarkerStyle(8)
        h_jetresponse_raw[index].SetMarkerSize(1.4)
        h_jetresponse_raw[index].SetMarkerColor(kRed+1)
        h_jetresponse_raw[index].SetLineColor(kRed+1)
        #h_jetresponse_cor[index].GetXaxis().SetRangeUser(0.0,0.3)
        h_jetresponse_cor[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + 'p_{T}^{#gamma}=' + str2)
        h_jetresponse_cor[index].GetXaxis().SetTitle('#alpha')
        h_jetresponse_cor[index].GetXaxis().SetTitleSize(0.045)
        h_jetresponse_cor[index].GetXaxis().SetTitleOffset(1.0)
        h_jetresponse_cor[index].GetYaxis().SetTitle('p_{T} balance')
        h_jetresponse_cor[index].GetYaxis().SetTitleSize(0.045)
        h_jetresponse_cor[index].GetYaxis().SetLabelSize(0.035)
        h_jetresponse_cor[index].GetYaxis().SetTitleOffset(1.0)
        h_jetresponse_cor[index].SetMarkerStyle(8)
        h_jetresponse_cor[index].SetMarkerSize(1.4)
        h_jetresponse_cor[index].SetMarkerColor(kBlue+1)
        h_jetresponse_cor[index].SetLineColor(kBlue+1)
        h_jetresponse_cor[index].Draw()
        h_jetresponse_raw[index].Draw('same')

        leg = TLegend(0.65,0.75,0.95,0.90)
        leg.AddEntry(h_jetresponse_raw[index], "raw p_{T}", "l")
        leg.AddEntry(h_jetresponse_cor[index], "cor p_{T}", "l")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw()

        c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.png')
        #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.pdf')
        index += 1
