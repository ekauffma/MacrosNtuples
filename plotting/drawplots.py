import ROOT
import os
import sys
import argparse
import ctypes

colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kGray+1, ROOT.kCyan+2, ROOT.kYellow+2, ROOT.kOrange+2, ROOT.kCyan]
#dirname = 'plotsL1Run3'


def main():
    parser = argparse.ArgumentParser(
        description='''Plotter''',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("-t", "--type", dest="type", help="Type of plots (hists, eff)", type=str, default='')
    parser.add_argument("-i", "--input", dest="inputFiles", help="Input file", nargs='+', type=str, default='')
    parser.add_argument("--den", dest="den", help="Name(s) of the histo denominator(s). There can be 1 or the same number as numerator histos ", nargs='+', type=str, default='')
    parser.add_argument("--num", dest="num", help="Name(s) of the histo numerator(s)", nargs='+', type=str, default='')
    parser.add_argument("--xtitle", dest="xtitle", help="X axis title", type=str, default='p_{T} (GeV)')
    parser.add_argument("--ytitle", dest="ytitle", help="Y axis title", type=str, default='Number of entries')
    parser.add_argument("--ztitle", dest="ztitle", help="Z axis title", type=str, default='Number of entries')
    parser.add_argument("--legend", dest="legendlabels", help="Legend labels", nargs='+', type=str, default='')
    parser.add_argument("--extralabel", dest="extralabel", help="Extra label", type=str, default='')
    parser.add_argument("--setlogx", dest="setlogx", help="Set log x", type=bool, default=False)
    parser.add_argument("--setlogy", dest="setlogy", help="Set log x", type=bool, default=False)
    parser.add_argument("--plotname", dest="plotname", help="Name of the plot", type=str, default='plot')
    parser.add_argument("--h2d", dest="h2d", help="2D histo (for profile etc)", nargs='+',type=str)
    parser.add_argument("--axisranges", dest="axisranges", help="Axis ranges [xmin, xmax, ymin, ymax, zmin, zmax]", nargs='+', type=float, default=[])
    parser.add_argument("--addnumtoden", dest="addnumtoden", help="Add numerator histo to denominator (because it only contains complementary events e.g. failing probes)",type=bool, default=False)
    parser.add_argument("--saveplot", dest="saveplot", help="Save plots in .png and .pdf format",type=bool, default = False)
    parser.add_argument("--saveroot", dest="saveroot", help="Save plots in .root format",type=bool, default = False)
    parser.add_argument("--interactive", dest="interactive", help="Run in interactive mode (keep plot drawn)", type=bool, default=False)
    parser.add_argument("--suffix_files", dest="suffix_files", help="Input files suffix", nargs='+', type=str, default='')
    parser.add_argument("--toplabel", dest="top_label", help="Label to put on top right of plot (for sqrt(s) and lumi values)", type=str, default="")
    parser.add_argument("--legendpos", dest="legend_pos", help="Position of the legend. String, accepted values: top, bottom. Default: bottom", type=str, default="bottom")
    parser.add_argument("--nvtx_suffix", dest="nvtx_suffix", help="Suffix to append to dirname and histogram names, to make plots in bins of nvtx. Default: None", type=str, default="")
    parser.add_argument("--h1d", dest="h1d", help="1D histo (for simple distribution, etc)", nargs='+',type=str)
    parser.add_argument("--dirname", dest="dirname", help="Directory to store the plots in", type=str, default='plotsL1Run3')
        
    args = parser.parse_args()
        
    if args.type=='efficiency':
        makeeff(inputFiles_list = args.inputFiles, den = args.den, num = args.num, addnumtoden = args.addnumtoden, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle=args.ytitle, ztitle=args.ztitle, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot=args.saveplot, saveroot=args.saveroot, interactive=args.interactive, suffix_files = args.suffix_files, top_label = args.top_label, legend_pos = args.legend_pos, nvtx_suffix = args.nvtx_suffix, dirname = args.dirname)
            
    if args.type=='profilex_fromh2':
        makeprof(inputFiles_list = args.inputFiles, h2d = args.h2d, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle=args.ytitle, ztitle=args.ztitle, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot=args.saveplot, saveroot=args.saveroot, interactive=args.interactive, top_label = args.top_label, legend_pos = args.legend_pos, nvtx_suffix = args.nvtx_suffix, dirname = args.dirname)

    if args.type=='resolvsx':
        makeresol(inputFiles_list = args.inputFiles, h2d = args.h2d, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle='#sigma_{scale corr.}'+args.ytitle, ztitle=args.ztitle, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot=args.saveplot, saveroot=args.saveroot, interactive=args.interactive, top_label = args.top_label, legend_pos = args.legend_pos, nvtx_suffix = args.nvtx_suffix, dirname = args.dirname)

    if args.type=='distribution':
        makedist(inputFiles_list = args.inputFiles, h1d = args.h1d, legendlabels = args.legendlabels, xtitle=args.xtitle, ytitle=args.ytitle, ztitle=args.ztitle, extralabel=args.extralabel, setlogx=args.setlogx, setlogy=args.setlogy, plotname=args.plotname, axisranges=args.axisranges, saveplot=args.saveplot, saveroot=args.saveroot, interactive=args.interactive, top_label = args.top_label, legend_pos = args.legend_pos, nvtx_suffix = args.nvtx_suffix, dirname = args.dirname)

def makeeff(inputFiles_list = [], den=[], num=[], addnumtoden=False, legendlabels=[], xtitle='p_{T} (GeV)', ytitle='Number of entries', ztitle='Number of entries', extralabel='', setlogx=False, setlogy=False, plotname='plot', axisranges=[], saveplot=False, interactive=False, suffix_files='', top_label='', legend_pos='bottom', nvtx_suffix='', dirname = 'plotsL1Run3'):

    if interactive == False:
        ROOT.gROOT.SetBatch(1)

    inputFiles = []
    for i in inputFiles_list:
        inputFiles.append(ROOT.TFile(i,"read"))

    h_dens = [] 
    h_nums = []

    for inputFile in inputFiles:
        print(inputFile.GetName())
        if len(den) !=1 and len(den)!=len(num):
            print("Numerator has {} histos while denominator has {}. Exiting.".format(len(h_nums),len(h_dens)))
            return 
        for i in range(len(num)):
            print(num[i]+nvtx_suffix)
            h_nums.append(inputFile.Get(num[i]+nvtx_suffix).Clone())
            if len(den)==1:
                h_dens.append(inputFile.Get(den[0]+nvtx_suffix).Clone())
            else:
                h_dens.append(inputFile.Get(den[i]+nvtx_suffix).Clone())
            h_nums[i].SetName(h_nums[i].GetName()+"_{}".format(i))
            h_dens[i].SetName(h_dens[i].GetName()+"_{}".format(i))
    effs = compute_eff(h_dens, h_nums, addnumtoden)
    drawplots(effs, legendlabels = legendlabels, xtitle=xtitle, ytitle=ytitle, ztitle=ztitle, extralabel=extralabel, setlogx=setlogx, setlogy=setlogy, plotname=plotname, axisranges=axisranges, saveplot = saveplot, interactive=interactive, suffix_files = suffix_files, top_label = top_label, legend_pos = legend_pos, nvtx_suffix = nvtx_suffix, dirname = dirname)

def makeprof(inputFiles_list = [], h2d=[], legendlabels=[], xtitle='p_{T} (GeV)', ytitle='Number of entries', ztitle='Number of entries', extralabel='', setlogx=False, setlogy=False, plotname='plot', axisranges=[], saveplot=False, interactive=False, suffix_files='', top_label='', legend_pos='bottom', nvtx_suffix='', dirname = 'plotsL1Run3'):

    if interactive == False:
        ROOT.gROOT.SetBatch(1)

    inputFiles = []
    for i in inputFiles_list:
        inputFiles.append(ROOT.TFile(i,"read"))

    h2ds = []
    for i in h2d:
        print(i)
        h2ds.append(inputFiles[0].Get(i+nvtx_suffix).Clone())
    profiles = compute_profilex(h2ds)
    drawplots(profiles, legendlabels = legendlabels, xtitle=xtitle, ytitle=ytitle, ztitle=ztitle, extralabel=extralabel, setlogx=setlogx, setlogy=setlogy, plotname=plotname, axisranges=axisranges, saveplot = saveplot, interactive=interactive, top_label = top_label, legend_pos = legend_pos, nvtx_suffix = nvtx_suffix, dirname = dirname)

def makeresol(inputFiles_list = [], h2d=[], legendlabels=[], xtitle='p_{T} (GeV)', ytitle='Number of entries', ztitle='Number of entries', extralabel='', setlogx=False, setlogy=False, plotname='plot', axisranges=[], saveplot=False, interactive=False, suffix_files='', top_label='', legend_pos='bottom', nvtx_suffix='', dirname = 'plotsL1Run3'):

    if interactive == False:
        ROOT.gROOT.SetBatch(1)

    inputFiles = []
    for i in inputFiles_list:
        inputFiles.append(ROOT.TFile(i,"read"))

    h2ds = []
    for inputFile in inputFiles:
        for i in range(len(h2d)):
            h2ds.append(inputFile.Get(h2d[i]+nvtx_suffix).Clone())
            h2ds[i].SetName(h2ds[i].GetName()+"_{}".format(i))
    hresponse, hresol = compute_ResolutionvsX(h2ds)
    drawplots(hresponse, legendlabels = legendlabels, xtitle=xtitle, ytitle='#mu'+ytitle, ztitle=ztitle, extralabel=extralabel, setlogx=setlogx, setlogy=setlogy, plotname='mu_'+plotname, axisranges=axisranges, saveplot = saveplot, interactive=interactive, suffix_files = suffix_files, top_label = top_label, legend_pos = legend_pos, nvtx_suffix = nvtx_suffix, dirname = dirname)
    axisranges[2] = 0
    axisranges[3] = 0.6
    drawplots(hresol, legendlabels = legendlabels, xtitle=xtitle, ytitle='#sigma_{scale corr.}'+ytitle, ztitle=ztitle, extralabel=extralabel, setlogx=setlogx, setlogy=setlogy, plotname='resol_'+plotname, axisranges=axisranges, saveplot = saveplot, interactive=interactive, top_label = top_label, legend_pos = legend_pos, nvtx_suffix = nvtx_suffix, dirname = dirname)

def makedist(inputFiles_list = [], h1d=[], legendlabels=[], xtitle='p_{T} (GeV)', ytitle='Number of entries', ztitle='Number of entries', extralabel='', setlogx=False, setlogy=False, plotname='plot', axisranges=[], saveplot=False, saveroot=False, interactive=False, suffix_files='', top_label='', legend_pos='bottom', nvtx_suffix='', dirname = 'plotsL1Run3'):

    if interactive == False:
        ROOT.gROOT.SetBatch(1)

    inputFiles = []
    for i in inputFiles_list:
        inputFiles.append(ROOT.TFile(i,"read"))


    h1ds = []
    for inputFile in inputFiles:
        for i in range(len(h1d)):
            h1ds.append(inputFile.Get(h1d[i]+nvtx_suffix).Clone())
            h1ds[i].SetName(h1ds[i].GetName()+"_{}".format(i))
    drawplots(h1ds, legendlabels = legendlabels, xtitle=xtitle, ytitle=ytitle, ztitle=ztitle, extralabel=extralabel, setlogx=setlogx, setlogy=setlogy, plotname=plotname, axisranges=axisranges, saveplot = saveplot, interactive=interactive, top_label = top_label, legend_pos = legend_pos, nvtx_suffix = nvtx_suffix, dirname = dirname)


def canvas(width=700, height=600, lmargin_frac=0.15, rmargin_frac=0.15):
    c = ROOT.TCanvas("c_eff", "c_eff", width, height)
    c.SetLeftMargin(lmargin_frac)
    c.SetRightMargin(rmargin_frac)
    c.SetGrid()
    c.SetFillStyle(4000)
    return c


def drawplots(objs, legendlabels, xtitle='', ytitle='', ztitle='',  extralabel='', setlogx=False, setlogy=False, plotname='plot', axisranges=[], saveplot=False, saveroot=False, interactive=False, suffix_files = [], top_label='', legend_pos = "bottom", nvtx_suffix = "", dirname = 'plotsL1Run3'):
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)

    width, height, lmargin_frac, rmargin_frac = 700, 600, 0.15, 0.15
    c = canvas(width, height, lmargin_frac, rmargin_frac)

    labelsize = len(legendlabels)
    for suffix in suffix_files:
        for j in range(labelsize):
            legendlabels.append(legendlabels[j] + suffix)

    if len(suffix_files)>0:
        del legendlabels[0:labelsize]
    
    if len(legendlabels) != len(objs):
        print("Some histos are missing a legend. ")
        legendlabels=[]
        for i in range(len(objs)):
            legendlabels.append('')

    labelsize = len(legendlabels)
    # get max extent of legend entries
    legend_w, legend_h = 0, 0
    for i in range(labelsize):
        entry = ROOT.TLatex(0, 0, legendlabels[i])
        entry.SetTextSize(0.04)
        entry.SetTextFont(42)
        entry_w = entry.GetXsize()
        entry_h = entry.GetYsize()
        legend_w = max(entry_w, legend_w)
        legend_h = max(entry_h, legend_h)
    if labelsize == 0:
        entry_w, entry_h = 0, 0


    # get size of lumi label (for some reason, this is broken later on)
    label_lumi = ROOT.TLatex(0.5, 0.5, top_label)
    label_lumi.SetTextSize(0.04)
    label_lumi.SetTextFont(42)
    lumi_w = label_lumi.GetXsize()

    # Define position of legend
    legend_margin = 30 
    legend = ROOT.TLegend(
            1 - rmargin_frac - entry_w - 2 * legend_margin/width, 0.12,
            1 - rmargin_frac - legend_margin/width, 0.12 + (legend_h + 5 / height)* labelsize,
            "", "mlNDC")

    #if plotname.find('resol')>=0 or legend_pos == 'top':
    if legend_pos == 'top':
        legend.SetY1(0.88 - (legend_h + 5 / height)* labelsize)
        legend.SetY2(0.88)
        
    ###
    legend.SetTextFont(42)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)
        
    objs[0].SetTitle(";{};{};{}".format(xtitle,ytitle,ztitle))
    if objs[0].GetDimension () == 1:
        objs[0].Draw()
    else:
        objs[0].Draw("zcol")

    if setlogx:
        c.SetLogx()
    if setlogy:
        c.SetLogy()

    c.Update()
    drawnobject = None
    if type(objs[0])==ROOT.TEfficiency and objs[0].GetDimension () == 1:
        drawnobject = objs[0].GetPaintedGraph()
    elif type(objs[0])==ROOT.TEfficiency and objs[0].GetDimension () == 2:
        drawnobject = objs[0].GetPaintedHistogram()
    else:
        drawnobject = objs[0]
        
    drawnobject.GetXaxis().SetMoreLogLabels()
    drawnobject.GetXaxis().SetNoExponent()
    drawnobject.GetXaxis().SetTitleSize(0.04)
    drawnobject.GetYaxis().SetTitleSize(0.04)

    # ticks for run number
    if plotname.find('VsRunNb')>=0:
        drawnobject.GetXaxis().SetLabelSize(0.0275)

    if objs[0].GetDimension() >=2:
        drawnobject.GetZaxis().SetTitleSize(0.04)
    if len(axisranges)>=2:
        drawnobject.GetXaxis().SetRangeUser(axisranges[0],axisranges[1])
    if len(axisranges)>=4:
        drawnobject.GetYaxis().SetRangeUser(axisranges[2],axisranges[3])
    if len(axisranges)>=6:
        drawnobject.GetZaxis().SetRangeUser(axisranges[4],axisranges[5])
    if len(axisranges)<4 and objs[0].GetDimension() == 1 and type(objs[0]) == ROOT.TEfficiency : 
        drawnobject.GetYaxis().SetRangeUser(0., 1.3) 
        
    marker_list = [20, 22, 23, 21, 29, 33, 34, 47, 24, 26, 25, 30, 28, 46]
    for i, h in enumerate(objs):
        if legendlabels[i] != '':
            legend.AddEntry(h,legendlabels[i],"lep")
        if i>0:
            objs[i].SetMarkerStyle(marker_list[i])
            objs[i].Draw("same")


    # CMS label
    label_cms = ROOT.TLatex()
    label_cms.SetTextSize(0.05)
    label_cms.DrawLatexNDC(lmargin_frac, 0.92, "#bf{CMS} #it{Internal}")


    # Lumi label
    # knowing the size, print it flushed with the right margin
    label_lumi.DrawLatexNDC(1 - rmargin_frac - lumi_w, 0.92, top_label)

    label_extra = ROOT.TPaveLabel(lmargin_frac + 0.02,0.75,0.9,0.9,"#color[2]{"+extralabel+"}","brNDC")
    label_extra.SetTextFont(43)
    label_extra.SetTextAlign(12)
    label_extra.SetTextSize(18)
    label_extra.SetFillStyle(0)
    label_extra.SetBorderSize(0)
    label_extra.Draw()

    
    legend.Draw()
    if interactive:
        input()
    if saveplot: 
        c.SaveAs(dirname+nvtx_suffix+'/'+plotname+'.png')
        c.SaveAs(dirname+nvtx_suffix+'/'+plotname+'.pdf')
    if saveroot:
        c.SaveAs(dirname+nvtx_suffix+'/'+plotname+'.root')

def compute_eff(hdens, hnums, addnumtoden):
    effs = []

    for i in range(len(hnums)):
        if addnumtoden:
            hdens[i].Add(hnums[i])
        eff = ROOT.TEfficiency(hnums[i], hdens[i])
        eff.SetFillStyle(0)
        eff.SetLineColor(colors[i])
        eff.SetMarkerStyle(20)
        eff.SetMarkerSize(0.5)
        eff.SetMarkerColor(colors[i])
        effs.append(eff)

    return effs

def setstyle(h, i):
    h.SetFillStyle(0)
    h.SetLineColor(colors[i])
    h.SetMarkerStyle(20)
    h.SetMarkerSize(0.5)
    h.SetMarkerColor(colors[i])
    return h


def compute_profilex(h2d):
    profiles = []
    for i, h in enumerate(h2d):
        profile = h.ProfileX().Clone()
        profile.SetFillStyle(0)
        profile.SetLineColor(colors[i])
        profile.SetMarkerStyle(20)
        profile.SetMarkerSize(0.5)
        profile.SetMarkerColor(colors[i])
        profiles.append(profile)
    
    return profiles

def compute_ResolutionvsX(h2d):
    histos_response, histos_resol = [], []
    for ctr, h in enumerate(h2d):
        h_responsevsX = h.ProjectionX().Clone()
        h_resolvsX = h.ProjectionX().Clone()
        setstyle(h_responsevsX, ctr)
        setstyle(h_resolvsX, ctr)
        for i in range(h.GetNbinsX()+1):
            proj = h.ProjectionY("py",i,i).Clone()
           
            f_gaus = ROOT.TF1("f_gaus","gaus")
            proj.Fit(f_gaus)
            #if f_gaus.GetParameter(1) >0 and f_gaus.GetParError(2)/f_gaus.GetParameter(1)<0.03:
            if f_gaus.GetParameter(1) >0 and f_gaus.GetParError(2)/f_gaus.GetParameter(1)<0.05:
                h_responsevsX.SetBinContent(i,f_gaus.GetParameter(1))
                h_responsevsX.SetBinError(i,f_gaus.GetParError(1))
                h_resolvsX.SetBinContent(i,f_gaus.GetParameter(2)/f_gaus.GetParameter(1))
                h_resolvsX.SetBinError(i,f_gaus.GetParError(2)/f_gaus.GetParameter(1))
            else:
                h_responsevsX.SetBinContent(i,0)
                h_responsevsX.SetBinError(i,0)
                h_resolvsX.SetBinContent(i,0)
                h_resolvsX.SetBinError(i,0)

        histos_resol.append(h_resolvsX)
        histos_response.append(h_responsevsX)
    return histos_response, histos_resol
if __name__ == '__main__':
    main()


