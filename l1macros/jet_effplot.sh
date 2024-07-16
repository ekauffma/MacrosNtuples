for eta in  eta0p0to1p3 eta1p3to2p5 eta2p5to3p0 eta3p0to3p5 eta3p5to4p0 eta4p0to5p0 eta3p0to5p0; do

#for threshold in l1thrgeq30p0 l1thrgeq60p0 l1thrgeq120p0 l1thrgeq180p0; do
#for threshold in l1thrgeq30p0 l1thrgeq60p0 ; do
#for threshold in l1thrgeq120p0 l1thrgeq180p0; do

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

  TFile *f1 = TFile::Open("/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ekauffma/NANOAOD/240712/Run2024E_withHCALTP_L1EmulJet.root");
  TH1F *h1 = (TH1F*)f1->Get("h_Jet_plots_${eta}");
  h1->GetYaxis()->SetTitle("Efficiency");
  h1->GetYaxis()->SetTitleOffset(1.1);
  h1->GetYaxis()->SetRangeUser(0., 1.5);
  h1->GetXaxis()->SetRangeUser(0., 700.);
  h1->GetXaxis()->SetTitle("Offline p_{T} [GeV]");

  TH1F *h2 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq30p0");

  TEfficiency* pEff1 = 0;
 
  if(TEfficiency::CheckConsistency(*h2,*h1))
  { 
    pEff1 = new TEfficiency(*h2,*h1);
    pEff1->SetLineWidth(2.);
  }


  TH1F *h3 = (TH1F*)f1->Get("h_Jet_plots_${eta}");

  TH1F *h4 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq60p0");

  TEfficiency* pEff2 = 0;
 
  if(TEfficiency::CheckConsistency(*h4,*h3))
  { 
    pEff2 = new TEfficiency(*h4,*h3);
    pEff2->SetLineWidth(2.);
  }


  TH1F *h5 = (TH1F*)f1->Get("h_Jet_plots_${eta}");

  TH1F *h6 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq120p0");

  TEfficiency* pEff3 = 0;
 
  if(TEfficiency::CheckConsistency(*h6,*h5))
  { 
    pEff3 = new TEfficiency(*h6,*h5);
    pEff3->SetLineWidth(2.);
  }

  TH1F *h7 = (TH1F*)f1->Get("h_Jet_plots_${eta}");

  TH1F *h8 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq180p0");

  TEfficiency* pEff4 = 0;

  if(TEfficiency::CheckConsistency(*h8,*h7))
  {
    pEff4 = new TEfficiency(*h8,*h7);
    pEff4->SetLineWidth(2.);
  }

  pEff1->SetLineColor(kBlack);
  pEff2->SetLineColor(kRed);
  pEff3->SetLineColor(kBlue);
  pEff4->SetLineColor(kGreen);

  h1->SetLineColorAlpha(kWhite, 0);
  h1->Draw();
  pEff1->Draw("same");
  pEff2->Draw("same");
  pEff3->Draw("same");
  pEff4->Draw("same");

  TLegend *legend1 = new TLegend(0.3, 0.68, 0.8, 0.88);
  legend1->SetTextFont(42);
  legend1->SetLineColor(0);
  legend1->SetTextSize(0.03);
  legend1->SetFillColor(0);
  legend1->AddEntry(pEff1, "L1 jet E_{T} > 30", "l");
  legend1->AddEntry(pEff2, "L1 jet E_{T} > 60", "l");
  legend1->AddEntry(pEff3, "L1 jet E_{T} > 120", "l");
  legend1->AddEntry(pEff4, "L1 jet E_{T} > 180", "l");
  legend1->Draw();

  TLatex *t2a = new TLatex(0.5,0.9," #bf{CMS} #it{Preliminary}         X fb^{-1} (2024E, 13.6 TeV) ");
  t2a->SetNDC();
  t2a->SetTextFont(42);
  t2a->SetTextSize(0.04);
  t2a->SetTextAlign(20);
  t2a->Draw("same");

  c1->SaveAs("jet_${eta}_2024E.pdf");
  
  TCanvas *c2 =new TCanvas("c2", " ", 0, 0, 700, 800);
  
  c2->Range(0, 0, 1, 1);
  c2->SetFillColor(0);
  c2->SetBorderMode(0);
  c2->SetBorderSize(2);
  c2->SetFrameBorderMode(0);
  c2->SetGrid();
  c2->Draw();
  gStyle->SetOptStat(0);
 
  TH1F *h10 = (TH1F*)f1->Get("h_MuonJet_${eta}_mass");
  h10->GetYaxis()->SetTitle("Counts");
  h10->GetYaxis()->SetTitleOffset(1.1);
  h10->GetXaxis()->SetRangeUser(0., 700.);
  h10->GetXaxis()->SetTitle("Jet + Muon Invariant Mass [GeV]");
  h10->Draw("ep");
  
  TLatex *t3a = new TLatex(0.5,0.9," #bf{CMS} #it{Preliminary}         X fb^{-1} (2024E, 13.6 TeV) ");
  t3a->SetNDC();
  t3a->SetTextFont(42);
  t3a->SetTextSize(0.04);
  t3a->SetTextAlign(20);
  t3a->Draw("same");

  c2->SaveAs("muonjet_mass_2024E_${eta}.pdf");
  
  TCanvas *c3 =new TCanvas("c3", " ", 0, 0, 700, 800);
  
  c3->Range(0, 0, 1, 1);
  c3->SetFillColor(0);
  c3->SetBorderMode(0);
  c3->SetBorderSize(2);
  c3->SetFrameBorderMode(0);
  c3->SetGrid();
  c3->Draw();
  gStyle->SetOptStat(0);
 
  TH1F *h11 = (TH1F*)f1->Get("h_Dimuon_${eta}_mass");
  h11->GetYaxis()->SetTitle("Counts");
  h11->GetYaxis()->SetTitleOffset(1.1);
  h11->GetXaxis()->SetRangeUser(0., 700.);
  h11->GetXaxis()->SetTitle("Dimuon Invariant Mass [GeV]");
  h11->Draw("ep");
  
  TLatex *t4a = new TLatex(0.5,0.9," #bf{CMS} #it{Preliminary}         X fb^{-1} (2024E, 13.6 TeV) ");
  t4a->SetNDC();
  t4a->SetTextFont(42);
  t4a->SetTextSize(0.04);
  t4a->SetTextAlign(20);
  t4a->Draw("same");

  c3->SaveAs("dimuon_mass_2024E_${eta}.pdf");
}

EOF

root -l -b -q test.C

rm test.C

done
