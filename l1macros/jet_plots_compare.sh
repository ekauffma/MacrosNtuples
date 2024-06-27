for eta in  eta0p0to1p3 eta1p3to2p5 eta2p5to3p0 eta3p0to3p5 eta3p5to4p0 eta4p0to5p0 eta3p0to5p0; do

#for threshold in l1thrgeq30p0 l1thrgeq60p0 l1thrgeq120p0 l1thrgeq180p0; do
#for threshold in l1thrgeq30p0 l1thrgeq60p0 ; do
#for threshold in l1thrgeq120p0 l1thrgeq180p0; do

cat>test.C<<EOF

#include <iostream>
#include <fstream>
#include <set>
#include <string>
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

void setCanvasOptions(TCanvas* canvas) {
  if (canvas) {
    canvas->Range(0, 0, 1, 1);
    canvas->SetFillColor(0);
    canvas->SetBorderMode(0);
    canvas->SetBorderSize(2);
    canvas->SetFrameBorderMode(0);
    canvas->SetGrid();
  }
}

TH1F* getBackgroundHistforEff(TFile *file, const char* etarange){
  std::string hist_name = std::string("h_Jet_plots_") + etarange;
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Efficiency");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetYaxis()->SetRangeUser(0., 1.5);
  hist->GetXaxis()->SetRangeUser(0., 700.);
  hist->GetXaxis()->SetTitle("Offline p_{T} [GeV]");
  
  return hist;
}

TEfficiency* getTEfficiency(TH1F *hist1, TH1F *hist2){
  TEfficiency* pEff = 0;
 
  if(TEfficiency::CheckConsistency(*hist2, *hist1))
  {
    pEff = new TEfficiency(*hist2,*hist1);
    pEff->SetLineWidth(2.);
  }
  
  return pEff;
}

TLegend* getEfficiencyTLegend(TEfficiency* pEff_f1, TEfficiency* pEff_f2, const char* file1Spec, const char* file2Spec, const char* suffix){
  TLegend *legend = new TLegend(0.3, 0.68, 0.8, 0.88);
  legend->SetTextFont(42);
  legend->SetLineColor(0);
  legend->SetTextSize(0.03);
  legend->SetFillColor(0);
  legend->AddEntry(pEff_f1, (std::string(file1Spec) + std::string(suffix)).c_str(), "l");
  legend->AddEntry(pEff_f2, (std::string(file2Spec) + std::string(suffix)).c_str(), "l");
  return legend;
}

TLatex* getCMSLabel(){
  TLatex *t = new TLatex(0.5,0.9," #bf{CMS} #it{Preliminary}         X fb^{-1} (2024E, 13.6 TeV) ");
  t->SetNDC();
  t->SetTextFont(42);
  t->SetTextSize(0.04);
  t->SetTextAlign(20);
  
  return t;
}

TH1F* getMuonJetMassHist(TFile *file, const char* etarange){
  std::string hist_name = std::string("h_MuonJet_") + etarange + std::string("_mass");
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetRangeUser(0., 700.);
  hist->GetXaxis()->SetTitle("Jet + Muon Invariant Mass [GeV]");
  
  return hist;
}

TH1F* getDimuonMassHist(TFile *file, const char* etarange){
  std::string hist_name = std::string("h_Dimuon_") + etarange + std::string("_mass");
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetRangeUser(0., 700.);
  hist->GetXaxis()->SetTitle("Dimuon Invariant Mass [GeV]");
  
  return hist;
}

void test(){

  TFile *f1 = TFile::Open("/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ekauffma/NANOAOD/output_jetid4.root");
  TFile *f2 = TFile::Open("/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ekauffma/NANOAOD/output_jetid6.root");
  char file1Spec[] = "JetId = 4";
  char file2Spec[] = "JetId = 6";
  
  
  /* jet efficiency plot for ET> 30 */
  
  TCanvas *c1 =new TCanvas("c1", " ", 0, 0, 700, 800);
  setCanvasOptions(c1);
  c1->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h1_f1 = getBackgroundHistforEff(f1, "${eta}");
  TH1F *h1_f2 = getBackgroundHistforEff(f2, "${eta}");

  TH1F *h2_f1 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq180p0");
  TH1F *h2_f2 = (TH1F*)f2->Get("h_Jet_plots_${eta}_l1thrgeq180p0");

  TEfficiency* pEff1_f1 = getTEfficiency(h1_f1, h2_f1);
  TEfficiency* pEff1_f2 = getTEfficiency(h1_f2, h2_f2);
 
  pEff1_f1->SetLineColor(kCyan+2);
  pEff1_f2->SetLineColor(kMagenta+1);

  h1_f1->SetLineColorAlpha(kWhite, 0);
  h1_f1->Draw();
  pEff1_f1->Draw("same");
  pEff1_f2->Draw("same");
  
  TLegend *legend1 = getEfficiencyTLegend(pEff1_f1, pEff1_f2, file1Spec, file2Spec, ", L1 jet E_{T} > 180");
  legend1->Draw();

  TLatex *t1 = getCMSLabel();
  t1->Draw("same");

  c1->SaveAs("jet_${eta}_ETgt180_2024E.pdf");
  
  
  /* jet efficiency plot for ET> 60 */
  /*
  TCanvas *c2 =new TCanvas("c2", " ", 0, 0, 700, 800);
  setCanvasOptions(c1);
  c2->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h3_f1 = getBackgroundHistforEff(f1, "${eta}");
  TH1F *h3_f2 = getBackgroundHistforEff(f2, "${eta}");
  
  TH1F *h3_f1_b = (TH1F*)f1->Get("h_Jet_plots_${eta}");
  TH1F *h3_f2_b = (TH1F*)f2->Get("h_Jet_plots_${eta}");

  TH1F *h4_f1 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq60p0");
  TH1F *h4_f2 = (TH1F*)f2->Get("h_Jet_plots_${eta}_l1thrgeq60p0");

  TEfficiency* pEff2_f1 = getTEfficiency(h4_f1, h3_f1_b);
  TEfficiency* pEff2_f2 = getTEfficiency(h4_f2, h3_f2_b);
 
  pEff2_f1->SetLineColor(kCyan+2);
  pEff2_f2->SetLineColor(kMagenta+1);
  
  h3_f1->SetLineColorAlpha(kWhite, 0);
  h3_f1->Draw();
  pEff2_f1->Draw("same");
  pEff2_f2->Draw("same");
  
  TLegend *legend2 = getEfficiencyTLegend(pEff2_f1, pEff2_f2, file1Spec, file2Spec, ", L1 jet E_{T} > 60");
  legend2->Draw();

  TLatex *t2 = getCMSLabel();
  t2->Draw("same");

  c2->SaveAs("jet_${eta}_ETgt60_2024E.pdf");
  
  */
  /* jet efficiency plot for ET> 120 */
  /*
  TCanvas *c3 =new TCanvas("c3", " ", 0, 0, 700, 800);
  setCanvasOptions(c1);
  c3->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h5_f1 = getBackgroundHistforEff(f1, "${eta}");
  TH1F *h5_f2 = getBackgroundHistforEff(f2, "${eta}");

  TH1F *h6_f1 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq120p0");
  TH1F *h6_f2 = (TH1F*)f2->Get("h_Jet_plots_${eta}_l1thrgeq120p0");

  TEfficiency* pEff3_f1 = getTEfficiency(h6_f1, h5_f1);
  TEfficiency* pEff3_f2 = getTEfficiency(h6_f2, h5_f2);
 
  pEff3_f1->SetLineColor(kCyan+2);
  pEff3_f2->SetLineColor(kMagenta+1);
  
  h5_f1->SetLineColorAlpha(kWhite, 0);
  h5_f1->Draw();
  pEff3_f1->Draw("same");
  pEff3_f2->Draw("same");
  
  TLegend *legend3 = getEfficiencyTLegend(pEff3_f1, pEff3_f2, file1Spec, file2Spec, ", L1 jet E_{T} > 120");
  legend3->Draw();

  TLatex *t3 = getCMSLabel();
  t3->Draw("same");

  c3->SaveAs("jet_${eta}_ETgt120_2024E.pdf");
  */
  
  /* jet efficiency plot for ET> 180 */
  /*
  TCanvas *c4 =new TCanvas("c4", " ", 0, 0, 700, 800);
  setCanvasOptions(c1);
  c4->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h7_f1 = getBackgroundHistforEff(f1, "${eta}");
  TH1F *h7_f2 = getBackgroundHistforEff(f2, "${eta}");

  TH1F *h8_f1 = (TH1F*)f1->Get("h_Jet_plots_${eta}_l1thrgeq180p0");
  TH1F *h8_f2 = (TH1F*)f2->Get("h_Jet_plots_${eta}_l1thrgeq180p0");

  TEfficiency* pEff4_f1 = getTEfficiency(h8_f1, h7_f1);
  TEfficiency* pEff4_f2 = getTEfficiency(h8_f2, h7_f2);
 
  pEff4_f1->SetLineColor(kCyan+2);
  pEff4_f2->SetLineColor(kMagenta+1);
  
  h7_f1->SetLineColorAlpha(kWhite, 0);
  h7_f1->Draw();
  pEff4_f1->Draw("same");
  pEff4_f2->Draw("same");
  
  TLegend *legend4 = getEfficiencyTLegend(pEff4_f1, pEff4_f2, file1Spec, file2Spec, ", L1 jet E_{T} > 180");
  legend4->Draw();

  TLatex *t4 = getCMSLabel();
  t4->Draw("same");

  c4->SaveAs("jet_${eta}_ETgt180_2024E.pdf");
  */

  /* jet muon invariant mass plot */
  
  TCanvas *c5 =new TCanvas("c5", " ", 0, 0, 700, 800);
  setCanvasOptions(c5);
  c5->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h9_f1 = getMuonJetMassHist(f1, "${eta}");
  TH1F *h9_f2 = getMuonJetMassHist(f2, "${eta}");
  h9_f1->SetLineColor(kCyan+2);
  h9_f2->SetLineColor(kMagenta+1);
  h9_f1->Draw("ep");
  h9_f2->Draw("ep same");
  
  TLegend *legend5 = new TLegend(0.3, 0.68, 0.8, 0.88);
  legend5->SetTextFont(42);
  legend5->SetLineColor(0);
  legend5->SetTextSize(0.03);
  legend5->SetFillColor(0);
  legend5->AddEntry(h9_f1, file1Spec, "l");
  legend5->AddEntry(h9_f2, file2Spec, "l");
  legend5->Draw();
  
  TLatex *t5 = getCMSLabel();
  t5->Draw("same");

  c5->SaveAs("muonjet_mass_compare_2024E_${eta}.pdf");
  
  
  /* dimuon invariant mass plot */
  
  TCanvas *c6 =new TCanvas("c6", " ", 0, 0, 700, 800);
  setCanvasOptions(c6);
  c6->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h10_f1 = getDimuonMassHist(f1, "${eta}");
  TH1F *h10_f2 = getDimuonMassHist(f2, "${eta}");
  h10_f1->SetLineColor(kCyan+2);
  h10_f2->SetLineColor(kMagenta+1);
  h10_f1->Draw("ep");
  h10_f2->Draw("ep same");
 
  TLegend *legend6 = new TLegend(0.3, 0.68, 0.8, 0.88);
  legend6->SetTextFont(42);
  legend6->SetLineColor(0);
  legend6->SetTextSize(0.03);
  legend6->SetFillColor(0);
  legend6->AddEntry(h10_f1, file1Spec, "l");
  legend6->AddEntry(h10_f2, file2Spec, "l");
  legend6->Draw();
  
  TLatex *t6 = getCMSLabel();
  t6->Draw("same");

  c6->SaveAs("dimuon_mass_compare_2024E_${eta}.pdf");
}

EOF

root -l -b -q test.C

rm test.C

done
