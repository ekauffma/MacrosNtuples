cat>test.C<<EOF

#include <iostream>
#include <fstream>
#include <set>
#include<TFile.h>
#include<TTree.h>
#include<TH1.h>
#include<TH2.h>
#include<THStack.h>
#include<TGraphErrors.h>
#include<TGraphAsymmErrors.h>
#include<TCanvas.h>
#include<TFrame.h>
#include<TLegend.h>
#include<vector>
#include<iostream>
#include<TMath.h>
#include<TROOT.h>
#include<TInterpreter.h>
#include<TStyle.h>
#include<TChain.h>
#include<TString.h>
#include<TPaveStats.h>
#include<TPad.h>
#include<TLatex.h>
#include "TEfficiency.h"
#include "TAxis.h"

void test(){

  TCanvas *c1 =new TCanvas("c1", " ", 0, 0, 700, 800);
  
  c1->Range(0, 0, 1, 1);
  c1->SetFillColor(0);
  c1->SetBorderMode(0);
  c1->SetBorderSize(2);
  c1->SetFrameBorderMode(0);
  c1->SetGrid();
  c1->Draw();
  gStyle->SetOptStat(0);

  TFile *f1 = TFile::Open("/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ekauffma/NANOAOD/240712/Run2024E_withHCALTP_L1Jet.root");
  TH1F *h1 = (TH1F*)f1->Get("h_offlineJetEta");
  std::cout<<"eta histogram integral = "<<h1->Integral()<<std::endl;
  h1->GetYaxis()->SetTitle("Counts");
  h1->GetYaxis()->SetTitleOffset(1.1);
  h1->GetXaxis()->SetTitle("Offline Jet #eta");
 
  h1->SetMarkerStyle(20); 
  h1->SetLineColor(kCyan+2);
  h1->SetMarkerColor(kCyan+2);
  h1->Draw("ep");

  TLatex *t2a = new TLatex(0.5,0.9," #bf{CMS} #it{Preliminary}         X fb^{-1} (2024E, 13.6 TeV) ");
  t2a->SetNDC();
  t2a->SetTextFont(42);
  t2a->SetTextSize(0.04);
  t2a->SetTextAlign(20);
  t2a->Draw("same");

  c1->SaveAs("jet_unmatched_plateau_eta.pdf");
}

EOF

root -l -b -q test.C

rm test.C
