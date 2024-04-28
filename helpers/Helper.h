#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
int EventsToPrint = 0;

ROOT::VecOps::RVec<float> CorrectedDeltaPhi_OfflineMuStation_L1Mu(ROOT::VecOps::RVec<int> recoMu_charge, ROOT::VecOps::RVec<float> recoMu_pt, ROOT::VecOps::RVec<float> recoMu_eta, ROOT::VecOps::RVec<float> recoMu_phi, ROOT::VecOps::RVec<float> MatchedL1Mu_phi) {

  const double etaboundary_EMTF = 1.24;
  const double Bfield = 3.8; //in Tesla
  const double Z_CSC_station2 = 8.2; //in meters

  ROOT::VecOps::RVec<float> result = {}; 
  for(unsigned int i = 0; i < recoMu_eta.size(); i++){
    if (MatchedL1Mu_phi[i] < -999.) {
      result.push_back(-1000.0);
      continue;
    }

    double R_station2 = (abs(recoMu_eta[i]) < etaboundary_EMTF) ? 5 : abs(Z_CSC_station2 * tan(2 * atan(exp(-recoMu_eta[i])))); //in meters
    double corr = asin(0.5 * 0.3 * Bfield * R_station2 / recoMu_pt[i]); 
    double muphi_station2 = (recoMu_charge[i] < 0) ? recoMu_phi[i]+corr : recoMu_phi[i]-corr; 
    double dphi = MatchedL1Mu_phi[i] - muphi_station2; 

    if (dphi > M_PI) dphi -= 2 * M_PI;
    if (dphi < -M_PI) dphi += 2 * M_PI;

    result.push_back(dphi);
  }
  return result;
}  






double deltaphi_offlinemustation2_l1mu(int charge, double mupt, double mueta, double muphi, double l1muphi){
    const double etaboundary_EMTF = 1.24;
    const double Bfield = 3.8; //in Tesla
    const double Z_CSC_station2 = 8.2; //in meters
    const double R_station2 =  (abs(mueta)<etaboundary_EMTF) ? 5 : abs(Z_CSC_station2*tan(2*atan(exp(-mueta)))); //in meters

    double corr = asin(0.5*0.3*Bfield*R_station2/mupt); 
    double muphi_station2 = (charge<0)? muphi+corr : muphi-corr; 
    double dphi = muphi_station2-l1muphi; 

    if(dphi> M_PI) dphi -= 2* M_PI;
    if(dphi<- M_PI) dphi += 2* M_PI;
    return dphi;
}  

vector<int> FindL1ObjIdx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    double drmin = 0.4; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = abs(acos(cos(recoObj_Phi[i]-L1Obj_phi[j]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

vector<int> FindL1MuIdx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, 
			ROOT::VecOps::RVec<float>recoObj_Pt, ROOT::VecOps::RVec<int>charge, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1, float dRminimum = 0.4){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    double drmin = dRminimum; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = deltaphi_offlinemustation2_l1mu(charge[i], recoObj_Pt[i], recoObj_Eta[i], recoObj_Phi[i], L1Obj_phi[j]);
      double dr = sqrt(deta*deta+dphi*dphi);
      
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

// Match objects only in a given bunch crossing
vector<int> FindL1MuIdx_setBx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>L1Obj_bx, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, 
        ROOT::VecOps::RVec<float>recoObj_Pt, ROOT::VecOps::RVec<int>charge, int bx, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    //double drmin = 0.4; 
    double drmin = 0.2; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      if(L1Obj_bx[j] != bx){
          continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      // Delta Phi correction at station 2
      double dphi = deltaphi_offlinemustation2_l1mu(charge[i], recoObj_Pt[i], recoObj_Eta[i], recoObj_Phi[i], L1Obj_phi[j]);
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

int FindL1EtSumIdx_setBx(ROOT::VecOps::RVec<float>L1Obj_etSumType, ROOT::VecOps::RVec<float>L1Obj_bx, int etSumType, int bx, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  int idx = -1;
  for(unsigned int j = 0; j<L1Obj_etSumType.size(); j++){

    if(L1Obj_CutVar.size()==L1Obj_etSumType.size()){
      if(L1Obj_CutVar[j]<CutVar) continue;
    }
    if(L1Obj_bx[j] != bx || L1Obj_etSumType[j] != etSumType) {
      continue;
    }
    idx = j;
    break;
  }
  return idx;
}

vector<int> FindL1ObjIdx_setBx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>L1Obj_bx, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, int bx, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1, float dRminimum=0.2){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){

    double drmin = dRminimum; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      if(L1Obj_bx[j] != bx){
          continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = abs(acos(cos(recoObj_Phi[i]-L1Obj_phi[j]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}

ROOT::VecOps::RVec<float> GetVal(ROOT::VecOps::RVec<int>idxL1Obj, ROOT::VecOps::RVec<float>L1Obj_val){
  ROOT::VecOps::RVec<float> result ={}; 
  for(unsigned int i = 0; i<idxL1Obj.size(); i++){
    if(idxL1Obj[i]<0) result.push_back(-1);
    else result.push_back(L1Obj_val[idxL1Obj[i]]);
  }
  return result;
}



vector<float> HighestMjj_L1(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx){

  vector<float> result;
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<30.)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<30.)continue;
      if(bx[j]!=0)continue;
      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      if(mass>result[0]){
	result[0] = mass;
	result[3] = abs(eta[i]-eta[j]);
	result[4] = abs(acos(cos(phi[i]-phi[j])));
	if(pt[j]> pt[i]){ result[1] = pt[j] ; result[2] = pt[i] ;}
	else {  result[1] = pt[i] ; result[2] = pt[j] ; }
      }
    }
  }
  return result;
}





bool L1SeedDoubleJetEtaMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double detacut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(abs(eta[i]-eta[j]) >= detacut&& dphi< dphicut )return true;
    }      
  }
  return false;
}


bool L1SeedDoubleJetMassMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;

      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(mass >= masscut && dphi< dphicut )return true;
    }      
  }
  return false;
}








vector<float> L1MHTHF(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx){
  vector<float> result;
  TVector2 mhthf(0.,0.);
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<30.)continue;
    if(bx[i]!=0)continue;
    TVector2 jetpt(0.,0.); 
    jetpt.SetMagPhi(pt[i], phi[i]);
    mhthf+=jetpt;
    
  }
  result.push_back(mhthf.Mod());
  result.push_back(mhthf.Phi());
  return result;
}

bool L1SeedDoubleJetMassMinNoOS(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;
      
      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(mass >= masscut && dphi< dphicut )return true;
    }      
  }
  return false;
}







bool L1SeedPtLeadDoubleJetMassMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  
  bool passleading = false;
  for(unsigned int i = 0; i<pt.size(); i++){
    if(bx[i]!=0)continue;
    if(pt[i]<ptlead)continue;
    passleading = true;
  }
  
  if(!passleading) return false;
  
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<pttrail)continue;
        if(bx[i]!=0)continue;
        for(unsigned int j = 0; j<pt.size(); j++){
            if(eta[i]*eta[j]>0) continue;
            if(pt[j]<pttrail)continue;
            if(bx[j]!=0)continue;

		      TLorentzVector jet1, jet2;
            jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
            jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
            float mass = (jet1+jet2).Mag();
            float dphi = abs(acos(cos(phi[i]-phi[j])));
            if(mass >= masscut && dphi< dphicut )return true;
          }      
      }
    return false;
  }

float mll(ROOT::VecOps::RVec<float>l_pt, ROOT::VecOps::RVec<float>l_eta, ROOT::VecOps::RVec<float>l_phi, ROOT::VecOps::RVec<bool>l_isTag, ROOT::VecOps::RVec<bool>l_isProbe){
  float mll = -1.;
  for(unsigned int i = 0; i < l_pt.size(); i++){
    if(l_pt.size() < 2) continue;
    if(l_isProbe[i] == false) continue;
    for(unsigned int j = 0; j < l_pt.size(); j++){
      if(i == j) continue;
      if(l_isTag[j] == false) continue;

      TLorentzVector lep1;
      TLorentzVector lep2;
      lep1.SetPtEtaPhiE(l_pt[i], l_eta[i], l_phi[i], l_pt[i] * cosh(l_eta[i]));
      lep2.SetPtEtaPhiE(l_pt[j], l_eta[j], l_phi[j], l_pt[j] * cosh(l_eta[j]));

      if(lep1.DeltaR(lep2) > 0.4){
	mll = (lep1+lep2).Mag();
      }
    }
  }
  return mll;
}

vector<vector<vector<float>>> dR_mll(ROOT::VecOps::RVec<float>l_pt, ROOT::VecOps::RVec<float>l_eta, ROOT::VecOps::RVec<float>l_phi, ROOT::VecOps::RVec<bool>l_isTag, ROOT::VecOps::RVec<bool>l_isProbe){
  //float mll = -1.;
  vector<vector<vector<float>>> result = {};
  if(l_pt.size() < 2){
    return result;
  }
  for(unsigned int i = 0; i < l_pt.size(); i++){
    vector<vector<float>> line = {};
    for(unsigned int j = 0; j < l_pt.size(); j++){

      float DeltaR = -1;
      float mll = -1;
      vector<float> pair = {};

      if((l_isProbe[i] == false)||(l_isTag[j] == false)||(i == j)){
	pair.push_back(DeltaR);
	pair.push_back(mll);
	line.push_back(pair);
	continue;
      }

      TLorentzVector lep1;
      TLorentzVector lep2;
      lep1.SetPtEtaPhiE(l_pt[i], l_eta[i], l_phi[i], l_pt[i] * cosh(l_eta[i]));
      lep2.SetPtEtaPhiE(l_pt[j], l_eta[j], l_phi[j], l_pt[j] * cosh(l_eta[j]));

      DeltaR = lep1.DeltaR(lep2);
      mll = (lep1+lep2).Mag();

      pair.push_back(DeltaR);
      pair.push_back(mll);
      line.push_back(pair);

    }
    result.push_back(line);
  }
  return result;
}

// Match offline object to TrigObj

vector<int> MatchObjToTrig(ROOT::VecOps::RVec<float>Obj_eta, ROOT::VecOps::RVec<float>Obj_phi, ROOT::VecOps::RVec<float>TrigObj_pt, ROOT::VecOps::RVec<float>TrigObj_eta, ROOT::VecOps::RVec<float>TrigObj_phi, ROOT::VecOps::RVec<int>TrigObj_id, int Target_id, ROOT::VecOps::RVec<int>filterBits, int filterBitIdx=1, float dRminimum=0.2, float trigObjPtCut = -1.){

  vector <int> result={};
  for(unsigned int i = 0; i<Obj_eta.size(); i++){
    //For HLT-reco matching => can use a small dR cone size. A larger cone size would be needed for L1-reco matching with muons. 
    double drmin = dRminimum; // Default dRmin = 0.2 
    int idx = -1;
    for(unsigned int j = 0; j<TrigObj_eta.size(); j++){
      if (TrigObj_id[j] != Target_id) continue;
      if (TrigObj_pt[j] < trigObjPtCut) continue;
      double deta = abs(TrigObj_eta[j]-Obj_eta[i]);
      //double dphi = deltaphi_offlinemustation2_l1mu(Muon_charge[i], TrigObj_pt[j], TrigObj_eta[j], TrigObj_phi[j], Muon_phi[i]);
      double dphi = abs(acos(cos(TrigObj_phi[j]-Obj_phi[i]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	
	if((filterBits[j]>>filterBitIdx&1) == 1){  // Default FilterBitIdx = 1
	  drmin = dr; 
	  idx = j;
	}

      }
    }
    result.push_back(idx);
  }
  return result;
}

// Recover triger decision from filterbit
ROOT::VecOps::RVec <Bool_t> trig_is_filterbit1_set(ROOT::VecOps::RVec<int>Trig_idx, ROOT::VecOps::RVec<int>filterBits, int filterBitIdx=1){
    vector <bool> result = {};
    for( unsigned int i = 0; i <Trig_idx.size(); i++){
        if (Trig_idx[i] == -1) result.push_back(false);
        else {
            int idx = Trig_idx[i];
	    if((filterBits[idx]>>filterBitIdx&1) == 1) result.push_back(true);
            else result.push_back(false);
        }
    }
    return result;
}


ROOT::VecOps::RVec <Bool_t> IsCleanJet(ROOT::VecOps::RVec<float>Obj_pt,  ROOT::VecOps::RVec<float>Obj_eta, ROOT::VecOps::RVec<float>Obj_phi, 
				       ROOT::VecOps::RVec<float>Lepton_pt, ROOT::VecOps::RVec<float>Lepton_eta, ROOT::VecOps::RVec<float>Lepton_phi, ROOT::VecOps::RVec<int>Lepton_passid,
				       ROOT::VecOps::RVec<float>Photon_pt, ROOT::VecOps::RVec<float>Photon_eta, ROOT::VecOps::RVec<float>Photon_phi, ROOT::VecOps::RVec<int>Photon_passid ){

  vector <bool> result={};
  for(unsigned int i = 0; i<Obj_eta.size(); i++){
    result.push_back(true);
    double drmin = 0.4; 
  
    for(unsigned int j = 0; j<Lepton_eta.size(); j++){
      if (! Lepton_passid[j] || Lepton_pt[j]<10  ) continue;
      double deta = abs(Lepton_eta[j]-Obj_eta[i]);
      double dphi = abs(acos(cos(Lepton_phi[j]-Obj_phi[i]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){
	result[i] =false;
	break;
      }
    }

    for(unsigned int j = 0; j<Photon_eta.size(); j++){
      if (! Photon_passid[j] || Photon_pt[j]<20  ) continue;
      double deta = abs(Photon_eta[j]-Obj_eta[i]);
      double dphi = abs(acos(cos(Photon_phi[j]-Obj_phi[i]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){
	result[i] =false;
	break;
      }
    }
  }

  return result;
}

vector<float> RecoHTTandMHT(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  float recoHTTMaxEta, float recoMHTMaxEta){
  vector<float> result;
  TVector2 mht(0., 0.);
  float htt = 0.;
  for(unsigned int i = 0; i<pt.size(); i++){
    if (pt[i] > 30. && abs(eta[i]) < recoMHTMaxEta) {
      TVector2 jetpt(0., 0.); 
      jetpt.SetMagPhi(pt[i], phi[i]);
      mht -= jetpt;
    }
    if (pt[i] > 30. && abs(eta[i]) < recoHTTMaxEta) {
      htt += pt[i];
    }
  }
  result.push_back(htt);
  result.push_back(mht.Mod());
  result.push_back(TVector2::Phi_mpi_pi(mht.Phi()));
  return result;
}

// Get the index of first tag Muon
int first_tagmuon_idx(ROOT::VecOps::RVec < bool > isTag) {
  int idx = -1;
  for (unsigned int i = 0; i < isTag.size(); i++) {
    if (isTag[i] == true) {
      idx = i;
      break;
    }
  }
  return idx;
  std::cout << idx << std::endl;
}


// M_{mu, MET} < 30 GeV
ROOT::VecOps::RVec < Bool_t > pass_muon_met_mass_belowX(ROOT::VecOps::RVec < float > Obj_pt, ROOT::VecOps::RVec < float > Obj_phi, float met_pt, float met_phi, float MassCut = 30) {
  vector < bool > result = {};
  for (unsigned int i = 0; i < Obj_pt.size(); i++) {
    float pt = Obj_pt[i];
    float phi = Obj_phi[i];
    float px = pt * cos(phi);
    float py = pt * sin(phi);
    float met_px = met_pt * cos(met_phi);
    float met_py = met_pt * sin(met_phi);
    float mass = sqrt((pt + met_pt) * (pt + met_pt) - (px + met_px) * (px + met_px) - (py + met_py) * (py + met_py));
    if (mass < MassCut) result.push_back(true);
    else result.push_back(false);
  }
  return result;
}


ROOT::VecOps::RVec < Bool_t > pass_probeTau(ROOT::VecOps::RVec < float > Tau_pt, ROOT::VecOps::RVec < float > Tau_eta, ROOT::VecOps::RVec < float > Tau_phi, ROOT::VecOps::RVec < float > Tau_mass, ROOT::VecOps::RVec < int > Tau_charge,
					    float tag_pt, float tag_eta, float tag_phi, float tag_mass, int tag_charge) {

  vector < bool > result = {};
  for (unsigned int i = 0; i < Tau_pt.size(); i++) {
    if (Tau_pt[i] < 20 || fabs(Tau_eta[i]) >= 2.1 || fabs(Tau_charge[i]) != 1) {
      result.push_back(false);
      continue;
    }
    TLorentzVector probe;
    TLorentzVector tag;
    probe.SetPtEtaPhiM(Tau_pt[i], Tau_eta[i], Tau_phi[i], Tau_mass[i]);
    tag.SetPtEtaPhiM(tag_pt, tag_eta, tag_phi, tag_mass);

    double dR = tag.DeltaR(probe);
    double m_tp = (tag + probe).M();
    if (dR <= 0.5 || m_tp <= 40 || m_tp >= 80 || (Tau_charge[i] * tag_charge >= 0)) {
      result.push_back(false);
      continue;
    }
    result.push_back(true);
  }
  return result;
}

ROOT::VecOps::RVec < Int_t > GetProbeNvtxArray(ROOT::VecOps::RVec < float > probe_Pt, int PV_npvs) {

  vector <int> result = {};
  for (unsigned int i = 0; i < probe_Pt.size(); i++) {
    result.push_back(PV_npvs);
  }
  return result;
}

// convert hwCharge (0 / +1) to charge (-1 / +1)
ROOT::VecOps::RVec < int > charge_conversion(ROOT::VecOps::RVec < int > hwCharge) {
  vector < int > result = {};
  for (unsigned int i = 0; i < hwCharge.size(); i++) {
    if (hwCharge[i] == 0) result.push_back(+1);
    else result.push_back(-1);
  }
  return result;
}

ROOT::VecOps::RVec<float> GetReducedDeltaphi(ROOT::VecOps::RVec<float> L1Obj_phi, ROOT::VecOps::RVec<float>probe_Phi){
  ROOT::VecOps::RVec<float> result = {}; 
  for(unsigned int i = 0; i < L1Obj_phi.size(); i++){
    float dphi = L1Obj_phi[i] - probe_Phi[i];
    float alpha = 1. / (2. * M_PI);
    if (abs(dphi) <= M_PI) {
      result.push_back(dphi);
    } else {
      float n = round(dphi * alpha);
      float dphi_reduced = dphi - n * (2. * M_PI);
      result.push_back(dphi_reduced);
    }
  }
  return result;
}

ROOT::VecOps::RVec <Bool_t> isLeadJet (ROOT::VecOps::RVec<float> Jet_pt, ROOT::VecOps::RVec<bool> isGoodJet) {
  vector <bool> result = {};
  float tempPt = 0.;
  if (Jet_pt.size() != isGoodJet.size()){
    std::cout << "Error: Size of inputs are different" << std::endl;
    return result;
  }

  bool goodJetFound = false;
  for (unsigned int i = 0; i < Jet_pt.size(); i++) {
    if (isGoodJet[i] && !goodJetFound) {
      goodJetFound = true;
      result.push_back(true);
    } else {
      result.push_back(false);
    }
  }
  return result;
}

