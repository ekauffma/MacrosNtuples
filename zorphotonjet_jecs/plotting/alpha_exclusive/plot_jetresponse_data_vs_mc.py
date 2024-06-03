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

# Data input
infile_dt = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/RunCDEFG_unprescaled.root')
# MC input
infile_MC = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/G-4Jets/Unprescaled/G-4Jets.root')

# Get the 2D histograms with the pt balance and create the Y projections
keys_dt = infile_dt.GetListOfKeys() # Data
keys_MC = infile_MC.GetListOfKeys() # MC

# Below we create a dictionary which contains lists
# Each list will correspond to all the different alpha values for each eta and pT bin 
str_binetas_pts = []
for e in str_binetas:
    for p in str_binpts:
        str_binetas_pts.append(e + p) # These will be the keys of the dictionary 
#print('Keys of the dictionary: ', str_binetas_pts)

# Data
h_ptBalance_dt = []          # Full list of histos for each eta, alpha and pt bin
h_ptBalance_vs_refpt_dt = [] # Full list of histos for each eta, alpha and pt bin (To be used later for plotting)
# MC
h_ptBalance_MC = []          # Full list of histos for each eta, alpha and pt bin
h_ptBalance_vs_refpt_MC = [] # Full list of histos for each eta, alpha and pt bin (To be used later for plotting)

# Data
h_ptBalance_per_eta_per_pt_dt = dict([(k, []) for k in str_binetas_pts])
# Read all the histograms and put them in the lists/dictionary
for key in keys_dt:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance_dt.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt_dt.append(histo2D.ProfileX())
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     h_ptBalance_per_eta_per_pt_dt[e+p].append(histo2D.ProjectionY())

# MC
h_ptBalance_per_eta_per_pt_MC = dict([(k, []) for k in str_binetas_pts])
for key in keys_MC:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       h_ptBalance_MC.append(histo2D.ProjectionY())
       h_ptBalance_vs_refpt_MC.append(histo2D.ProfileX())
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     h_ptBalance_per_eta_per_pt_MC[e+p].append(histo2D.ProjectionY())

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
dir0 = 'jet_response_alpha_exclusive'
os.makedirs(dir0, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for a in range(NalphaBins):
        str2='[' + str("{:.2f}".format(alphaBins[a])) + ',' + str("{:.2f}".format(alphaBins[a+1])) +')'
        for p in range(NptBins):
            str3 = '[' + str(jetptBins[p]) + ',' + str(jetptBins[p+1]) + ')'

            c = TCanvas(str1 + ',' + str2 + ',' + str3, str1 + ',' + str2 + ',' + str3, 1000, 1000)
            h_ptBalance_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2 + ', ' + 'p_{T}^{#gamma}=' + str3)
            h_ptBalance_dt[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma} (GeV)')
            h_ptBalance_dt[index].GetXaxis().SetTitleOffset(1.2)
            h_ptBalance_dt[index].GetYaxis().SetTitle('Events')
            h_ptBalance_dt[index].GetYaxis().SetLabelSize(0.03)
            h_ptBalance_dt[index].GetYaxis().SetTitleOffset(1.5)
            h_ptBalance_dt[index].SetLineColor(kBlue+1)
            h_ptBalance_MC[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2 + ', ' + 'p_{T}^{#gamma}=' + str3)
            h_ptBalance_MC[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma} (GeV)')
            h_ptBalance_MC[index].GetXaxis().SetTitleOffset(1.2)
            h_ptBalance_MC[index].GetYaxis().SetTitle('Events')
            h_ptBalance_MC[index].GetYaxis().SetLabelSize(0.03)
            h_ptBalance_MC[index].GetYaxis().SetTitleOffset(1.5)
            h_ptBalance_MC[index].SetLineColor(kRed+1)

            m_MC = h_ptBalance_MC[index].GetMaximum()
            m_dt = h_ptBalance_dt[index].GetMaximum()
        
            m = 0.
            if ( m_MC > m_dt):
               m = m_MC
               h_ptBalance_MC[index].Draw('HIST')
               h_ptBalance_dt[index].Draw('same HIST')
            else:
               m = m_dt
               h_ptBalance_dt[index].Draw('HIST')
               h_ptBalance_MC[index].Draw('same HIST')
             
            leg = TLegend(0.62,0.75,0.92,0.90)
            leg.AddEntry(h_ptBalance_MC[index], "MC (G-4Jets)", "l")
            leg.AddEntry(h_ptBalance_dt[index], "Data (EGamma)", "l")
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)
            leg.Draw()

            l = TLine(1.0,0.0,1.0,m)
            l.SetLineStyle(2)
            l.Draw()

            gPad.RedrawAxis()
            #c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.png')
            c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p] + '.pdf')
            c.Update()
            index += 1

# Then create canvases with all the pt balance plots vs pt_ref for all eta and alpha bins
dir1 = 'jet_response_vs_refpt_alpha_exclusive'
os.makedirs(dir1, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for a in range(NalphaBins):
        str2='[' + str("{:.2f}".format(alphaBins[a])) + ',' + str("{:.2f}".format(alphaBins[a+1])) +')'

        #print('Adding histograms to: ', h_ptBalance_vs_refpt[index].GetName())
        # Here we add all the different pt histograms such that we have one histogram per eta and alpha bin
        for p in range(NptBins-1):
            h_ptBalance_vs_refpt_MC[index].Add(h_ptBalance_vs_refpt_MC[index+p+1])
            h_ptBalance_vs_refpt_dt[index].Add(h_ptBalance_vs_refpt_dt[index+p+1])
            #print(' adding: ', h_ptBalance_vs_refpt[index+p+1].GetName())

        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        gStyle.SetOptStat(0)
        gPad.SetLogx()
        h_ptBalance_vs_refpt_dt[index].GetXaxis().SetMoreLogLabels()
        h_ptBalance_vs_refpt_dt[index].GetXaxis().SetNoExponent()
        h_ptBalance_vs_refpt_dt[index].SetMaximum(1.25)
        h_ptBalance_vs_refpt_dt[index].SetMinimum(0.5)
        h_ptBalance_vs_refpt_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + '#alpha=' + str2)
        h_ptBalance_vs_refpt_dt[index].GetXaxis().SetTitle('p_{T}^{#gamma}')
        h_ptBalance_vs_refpt_dt[index].GetXaxis().SetTitleOffset(1.3)
        h_ptBalance_vs_refpt_dt[index].GetYaxis().SetTitle('p_{T} balance')
        h_ptBalance_vs_refpt_dt[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_vs_refpt_dt[index].GetYaxis().SetTitleOffset(1.4)
        h_ptBalance_vs_refpt_dt[index].SetMarkerStyle(8)
        h_ptBalance_vs_refpt_dt[index].SetMarkerSize(1.4)
        h_ptBalance_vs_refpt_dt[index].SetMarkerColor(kBlue+1)
        h_ptBalance_vs_refpt_dt[index].SetLineColor(kBlue+1)
        h_ptBalance_vs_refpt_MC[index].SetMarkerStyle(8)
        h_ptBalance_vs_refpt_MC[index].SetMarkerSize(1.4)
        h_ptBalance_vs_refpt_MC[index].SetMarkerColor(kRed+1)
        h_ptBalance_vs_refpt_MC[index].SetLineColor(kRed+1)
        h_ptBalance_vs_refpt_dt[index].Draw()
        h_ptBalance_vs_refpt_MC[index].Draw('same')
        
        leg = TLegend(0.62,0.75,0.92,0.90)
        leg.AddEntry(h_ptBalance_vs_refpt_MC[index], "MC (G-4Jets)", "l")
        leg.AddEntry(h_ptBalance_vs_refpt_dt[index], "Data (EGamma)", "l")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw()

        l = TLine(0.0,1.0,1000,1.0)
        l.SetLineStyle(2)
        l.Draw()

        gPad.RedrawAxis()
        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.png')
        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + '_' + str_binalphas[a] + '.pdf')
        index += NptBins

# Then for each eta and each pt bin we take the mean (pt balance) and draw it as a function of alpha
# Here we use the dictionary with the lists of histograms
dir2 = 'jet_response_vs_alpha'
os.makedirs(dir2, exist_ok = True)

h_means_MC = {}  #Dictionary with the mean values
h_errors_MC = {} #Dictionary with the mean value errors

for etapt_mc, histo_mc in h_ptBalance_per_eta_per_pt_MC.items():
    mean_values = []
    mean_errors = []
    # Create the lists with means and errors 
    for histogram_mc in histo_mc:
        mean_values.append(histogram_mc.GetMean())     
        mean_errors.append(histogram_mc.GetMeanError())     
    # Store the lists in the dictionaries using the same keys
    h_means_MC[etapt_mc] = mean_values
    h_errors_MC[etapt_mc] = mean_errors

h_means_dt = {}  #Dictionary with the mean values
h_errors_dt = {} #Dictionary with the mean value errors

for etapt_dt, histo_dt in h_ptBalance_per_eta_per_pt_dt.items():
    mean_values = []
    mean_errors = []
    # Create the lists with means and errors 
    for histogram_dt in histo_dt:
        mean_values.append(histogram_dt.GetMean())     
        mean_errors.append(histogram_dt.GetMeanError())     
    # Store the lists in the dictionaries using the same keys
    h_means_dt[etapt_dt] = mean_values
    h_errors_dt[etapt_dt] = mean_errors

# Print mean values for tests
#for k,v in h_means.items():
#    print(f'Key: {k}')
#    for value in v:
#        print(f'Mean: {value}')

# Create a list with the final histograms jet response vs alpha for each eta, pt bin
h_jetresponse_MC = []
for (etapt1,mean), (etapt2,error) in zip(h_means_MC.items(), h_errors_MC.items()):
    h = TH1F(etapt1+'_MC', etapt1+'_MC', NalphaBins, alphaBins)
    ibin = 1
    for m,e in zip(mean,error):
        h.SetBinContent(ibin, m)
        h.SetBinError(ibin, e)
        ibin +=1 
    h_jetresponse_MC.append(h)
    h.Delete

h_jetresponse_dt = []
for (etapt1,mean), (etapt2,error) in zip(h_means_dt.items(), h_errors_dt.items()):
    h = TH1F(etapt1+'_dt', etapt1+'_dt', NalphaBins, alphaBins)
    ibin = 1
    for m,e in zip(mean,error):
        h.SetBinContent(ibin, m)
        h.SetBinError(ibin, e)
        ibin +=1 
    h_jetresponse_dt.append(h)

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
        h_jetresponse_dt[index].GetXaxis().SetRangeUser(0.0,0.3)
        h_jetresponse_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', ' + 'p_{T}^{#gamma}=' + str2)
        h_jetresponse_dt[index].GetXaxis().SetTitle('#alpha')
        h_jetresponse_dt[index].GetXaxis().SetTitleSize(0.045)
        h_jetresponse_dt[index].GetXaxis().SetTitleOffset(1.0)
        h_jetresponse_dt[index].GetYaxis().SetTitle('p_{T} balance')
        h_jetresponse_dt[index].GetYaxis().SetTitleSize(0.045)
        h_jetresponse_dt[index].GetYaxis().SetLabelSize(0.035)
        h_jetresponse_dt[index].GetYaxis().SetTitleOffset(1.0)
        h_jetresponse_dt[index].SetMarkerStyle(8)
        h_jetresponse_dt[index].SetMarkerSize(1.4)
        h_jetresponse_dt[index].SetMarkerColor(kBlue+1)
        h_jetresponse_dt[index].SetLineColor(kBlue+1)
        h_jetresponse_MC[index].SetMarkerStyle(8)
        h_jetresponse_MC[index].SetMarkerSize(1.4)
        h_jetresponse_MC[index].SetMarkerColor(kRed+1)
        h_jetresponse_MC[index].SetLineColor(kRed+1)
        h_jetresponse_dt[index].Draw()
        h_jetresponse_MC[index].Draw('same')

        leg = TLegend(0.62,0.75,0.92,0.90)
        leg.AddEntry(h_jetresponse_MC[index], "MC (G-4Jets)", "l")
        leg.AddEntry(h_jetresponse_dt[index], "Data (EGamma)", "l")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw()

        gPad.RedrawAxis()
        #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.png')
        c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.pdf')
        index += 1
