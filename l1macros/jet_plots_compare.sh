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

void setTwoHistMaximum(TH1F *hist1, TH1F *hist2, double maxRatio = 1.5){
  int maxBin1 = hist1->GetMaximumBin();
  int maxBinContent1 = hist1->GetBinContent(maxBin1);
  int maxBin2 = hist2->GetMaximumBin();
  int maxBinContent2 = hist2->GetBinContent(maxBin2);
  int maxBinContent = std::max(maxBinContent1, maxBinContent2);
  hist1->SetMaximum(maxRatio * maxBinContent);
  hist2->SetMaximum(maxRatio * maxBinContent);
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

TLegend* getHistTLegend(TH1F* hist_1, TH1F* hist_2, const char* file1Spec, const char* file2Spec){
  TLegend *legend = new TLegend(0.3, 0.68, 0.8, 0.88);
  legend->SetTextFont(42);
  legend->SetLineColor(0);
  legend->SetTextSize(0.03);
  legend->SetFillColor(0);
  legend->AddEntry(hist_1, file1Spec, "l");
  legend->AddEntry(hist_2, file2Spec, "l");
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

TH1F* getMuonJetMassHist(TFile *file, const char* etarange, int histColor){
  std::string hist_name = std::string("h_MuonJet_") + etarange + std::string("_mass");
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetRangeUser(0., 700.);
  hist->GetXaxis()->SetTitle("Jet + Muon Invariant Mass [GeV]");
  hist->SetLineColor(histColor);
  hist->SetMarkerColor(histColor);
  hist->SetMarkerSize(0.5);
  hist->SetMarkerStyle(8);
  hist->SetLineWidth(2);
  
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

TH1F* getJetPtHist(TFile *file, const char* etarange, int histColor){
  std::string hist_name = std::string("h_LeadingJetPt_") + etarange;
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetRangeUser(0., 700.);
  hist->GetXaxis()->SetTitle("Leading Jet Pt [GeV]");
  hist->SetLineColor(histColor);
  hist->SetMarkerColor(histColor);
  hist->SetMarkerSize(0.5);
  hist->SetMarkerStyle(8);
  hist->SetLineWidth(2);
  
  return hist;
}

TH1F* getUnmatchedJetEtaHist(TFile *file, int histColor){
  std::string hist_name = std::string("h_offlineJetEta");
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetTitle("Unmatched Offline Jet #eta");
  hist->SetLineColor(histColor);
  hist->SetMarkerColor(histColor);
  hist->SetMarkerSize(0.5);
  hist->SetMarkerStyle(8);
  hist->SetLineWidth(2);
  
  return hist;
}

TH1F* getUnmatchedJetPtHist(TFile *file, const char* etarange, int histColor){
  std::string hist_name = std::string("h_unmatchedJetPt_") + etarange;
  std::cout<<hist_name<<std::endl;
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetRangeUser(0., 700.);
  hist->GetXaxis()->SetTitle("Unmatched Offline Jet Pt [GeV]");
  hist->SetLineColor(histColor);
  hist->SetMarkerColor(histColor);
  hist->SetMarkerSize(0.5);
  hist->SetMarkerStyle(8);
  hist->SetLineWidth(2);
  
  return hist;
}

TH1F* getUnmatchedJetRatioHist(TFile *file, const char* etarange, const char* ratioType, int histColor){
  std::string hist_name = std::string("h_unmatchedJet") + ratioType + std::string("_") + etarange;
  std::cout<<"hist name = "<<hist_name<<std::endl;
  TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
  hist->GetYaxis()->SetTitle("Counts");
  hist->GetYaxis()->SetTitleOffset(1.1);
  hist->GetXaxis()->SetRangeUser(0., 1.);
  std::string hist_axis_title = std::string("Unmatched Offline Jet") + ratioType;
  hist->GetXaxis()->SetTitle(hist_axis_title.c_str());
  hist->SetLineColor(histColor);
  hist->SetMarkerColor(histColor);
  hist->SetMarkerSize(0.5);
  hist->SetMarkerStyle(8);
  hist->SetLineWidth(2);
  
  return hist;
}

void test(){

  TFile *f1 = TFile::Open("/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ekauffma/NANOAOD/240909/output.root");
  TFile *f2 = TFile::Open("/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/ekauffma/NANOAOD/240909/output_reemul.root");
  char file1Spec[] = "L1Jet";
  char file2Spec[] = "L1EmulJet";
  
  
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
  
  std::cout<<"Creating jet muon invariant mass plot"<<std::endl;

  TCanvas *c5 =new TCanvas("c5", " ", 0, 0, 700, 800);
  setCanvasOptions(c5);
  c5->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h9_f1 = getMuonJetMassHist(f1, "${eta}", kCyan+2);
  TH1F *h9_f2 = getMuonJetMassHist(f2, "${eta}", kMagenta+1);
  setTwoHistMaximum(h9_f1, h9_f2, 1.3);
  h9_f1->Draw("epc");
  h9_f2->Draw("epc same");
  
  TLegend *legend5 = getHistTLegend(h9_f1, h9_f2, file1Spec, file2Spec);
  legend5->Draw();
  
  TLatex *t5 = getCMSLabel();
  t5->Draw("same");

  c5->SaveAs("muonjet_mass_compare_2024E_${eta}.pdf");
  
  
  /* dimuon invariant mass plot */
 
  std::cout<<"Creating dimuon invariant mass plot"<<std::endl;
 
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
 
  TLegend *legend6 = getHistTLegend(h10_f1, h10_f2, file1Spec, file2Spec);
  legend6->Draw();
  
  TLatex *t6 = getCMSLabel();
  t6->Draw("same");

  c6->SaveAs("dimuon_mass_compare_2024E_${eta}.pdf");
  
  
  /* jet pt plot */
 
  std::cout<<"Creating jet pt plot"<<std::endl;
 
  TCanvas *c7 =new TCanvas("c7", " ", 0, 0, 700, 800);
  setCanvasOptions(c7);
  c7->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h11_f1 = getJetPtHist(f1, "${eta}", kCyan+2);
  TH1F *h11_f2 = getJetPtHist(f2, "${eta}", kMagenta+1);
  setTwoHistMaximum(h11_f1, h11_f2, 1.3);
  h11_f1->Draw("epc");
  h11_f2->Draw("epc same");
 
  TLegend *legend7 = getHistTLegend(h11_f1, h11_f2, file1Spec, file2Spec);
  legend7->Draw();
  
  TLatex *t7 = getCMSLabel();
  t7->Draw("same");

  c7->SaveAs("jet_pt_compare_2024E_${eta}.pdf");
  
  
  /* unmatched l1jet eta plot */
 
  std::cout<<"Creating unmatched l1jet eta plot"<<std::endl;
 
  TCanvas *c8 =new TCanvas("c8", " ", 0, 0, 700, 800);
  setCanvasOptions(c8);
  c8->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h12_f1 = getUnmatchedJetEtaHist(f1, kCyan+2);
  TH1F *h12_f2 = getUnmatchedJetEtaHist(f2, kMagenta+1);
  setTwoHistMaximum(h12_f1, h12_f2, 1.3);
  h12_f1->Draw("h");
  h12_f2->Draw("h same");
 
  TLegend *legend8 = getHistTLegend(h12_f1, h12_f2, file1Spec, file2Spec);
  legend8->Draw();
  
  TLatex *t8 = getCMSLabel();
  t8->Draw("same");

  c8->SaveAs("unmatched_jet_eta_compare_2024E.pdf");
  
  
  /* unmatched l1jet pt plot */
  std::cout<<"Creating unmatched l1jet pt plot"<<std::endl;
 
  TCanvas *c9 =new TCanvas("c9", " ", 0, 0, 700, 800);
  setCanvasOptions(c9);
  c9->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h13_f1 = getUnmatchedJetPtHist(f1, "${eta}", kCyan+2);
  TH1F *h13_f2 = getUnmatchedJetPtHist(f2, "${eta}", kMagenta+1);
  setTwoHistMaximum(h13_f1, h13_f2);
  h13_f1->Draw("h");
  h13_f2->Draw("h same");
 
  TLegend *legend9 = getHistTLegend(h13_f1, h13_f2, file1Spec, file2Spec);
  legend9->Draw();
  
  TLatex *t9 = getCMSLabel();
  t9->Draw("same");

  c9->SaveAs("unmatched_jet_pt_compare_2024E_${eta}.pdf");
  
  
  /* unmatched l1jet NHEF plot */
  std::cout<<"Creating unmatched l1jet NHEF plot"<<std::endl;
 
  TCanvas *c10 =new TCanvas("c10", " ", 0, 0, 700, 800);
  setCanvasOptions(c10);
  c10->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h14_f1 = getUnmatchedJetRatioHist(f1, "${eta}", "NHEF", kCyan+2);
  TH1F *h14_f2 = getUnmatchedJetRatioHist(f2, "${eta}", "NHEF", kMagenta+1);
  setTwoHistMaximum(h14_f1, h14_f2);
  h14_f1->Draw("h");
  h14_f2->Draw("h same");
 
  TLegend *legend10 = getHistTLegend(h14_f1, h14_f2, file1Spec, file2Spec);
  legend10->Draw();
  
  TLatex *t10 = getCMSLabel();
  t10->Draw("same");

  c10->SaveAs("unmatched_jet_NHEF_compare_2024E_${eta}.pdf");
  
  
  /* unmatched l1jet NEEF plot */
  std::cout<<"Creating unmatched l1jet NEEF plot"<<std::endl;
 
  TCanvas *c11 =new TCanvas("c11", " ", 0, 0, 700, 800);
  setCanvasOptions(c11);
  c11->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h15_f1 = getUnmatchedJetRatioHist(f1, "${eta}", "NEEF", kCyan+2);
  TH1F *h15_f2 = getUnmatchedJetRatioHist(f2, "${eta}", "NEEF", kMagenta+1);
  setTwoHistMaximum(h15_f1, h15_f2);
  h15_f1->Draw("h");
  h15_f2->Draw("h same");
 
  TLegend *legend11 = getHistTLegend(h15_f1, h15_f2, file1Spec, file2Spec);
  legend11->Draw();
  
  TLatex *t11 = getCMSLabel();
  t11->Draw("same");

  c11->SaveAs("unmatched_jet_NEEF_compare_2024E_${eta}.pdf");
  
  
  /* unmatched l1jet CHEF plot */
  std::cout<<"Creating unmatched l1jet CHEF plot"<<std::endl;
 
  TCanvas *c12 =new TCanvas("c12", " ", 0, 0, 700, 800);
  setCanvasOptions(c12);
  c12->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h16_f1 = getUnmatchedJetRatioHist(f1, "${eta}", "CHEF", kCyan+2);
  TH1F *h16_f2 = getUnmatchedJetRatioHist(f2, "${eta}", "CHEF", kMagenta+1);
  setTwoHistMaximum(h16_f1, h16_f2);
  h16_f1->Draw("h");
  h16_f2->Draw("h same");
 
  TLegend *legend12 = getHistTLegend(h16_f1, h16_f2, file1Spec, file2Spec);
  legend12->Draw();
  
  TLatex *t12 = getCMSLabel();
  t12->Draw("same");

  c12->SaveAs("unmatched_jet_CHEF_compare_2024E_${eta}.pdf");
  
  
  /* unmatched l1jet CEEF plot */
  std::cout<<"Creating unmatched l1jet CEEF plot"<<std::endl;
 
  TCanvas *c13 =new TCanvas("c13", " ", 0, 0, 700, 800);
  setCanvasOptions(c13);
  c13->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h17_f1 = getUnmatchedJetRatioHist(f1, "${eta}", "CEEF", kCyan+2);
  TH1F *h17_f2 = getUnmatchedJetRatioHist(f2, "${eta}", "CEEF", kMagenta+1);
  setTwoHistMaximum(h17_f1, h17_f2);
  h17_f1->Draw("h");
  h17_f2->Draw("h same");
 
  TLegend *legend13 = getHistTLegend(h17_f1, h17_f2, file1Spec, file2Spec);
  legend13->Draw();
  
  TLatex *t13 = getCMSLabel();
  t13->Draw("same");

  c13->SaveAs("unmatched_jet_CEEF_compare_2024E_${eta}.pdf");

  /* unmatched l1jet MUEF plot */
  std::cout<<"Creating unmatched l1jet MUEF plot"<<std::endl;
                                                                             
  TCanvas *c14 =new TCanvas("c14", " ", 0, 0, 700, 800);
  setCanvasOptions(c14);
  c14->Draw();
  gStyle->SetOptStat(0);
  
  TH1F *h18_f1 = getUnmatchedJetRatioHist(f1, "${eta}", "MUEF", kCyan+2);
  TH1F *h18_f2 = getUnmatchedJetRatioHist(f2, "${eta}", "MUEF", kMagenta+1);
  setTwoHistMaximum(h18_f1, h18_f2);
  h18_f1->Draw("h");
  h18_f2->Draw("h same");
                                                                             
  TLegend *legend14 = getHistTLegend(h18_f1, h18_f2, file1Spec, file2Spec);
  legend14->Draw();
  
  TLatex *t14 = getCMSLabel();
  t14->Draw("same");
                                                                             
  c14->SaveAs("unmatched_jet_MUEF_compare_2024E_${eta}.pdf");


}

EOF

root -l -b -q test.C

rm test.C

done
