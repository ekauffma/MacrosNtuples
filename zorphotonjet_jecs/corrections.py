import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

# C++ function to get the raw pT from the corrected pT
ROOT.gInterpreter.Declare('''
ROOT::VecOps::RVec<float> JetRawPt(const ROOT::VecOps::RVec<float> &pt,
                                   const ROOT::VecOps::RVec<float> &rawf){

    ROOT::VecOps::RVec<float> Jet_rawPt;

    for(unsigned int i=0; i<pt.size(); i++){
       double rawPt = pt[i] * (1 - rawf[i]);
       Jet_rawPt.push_back(rawPt);
    }

    return Jet_rawPt;

}
''')

# json file with Jet Energy Corrections
# TODO: make it generic and read the files that corresponds to the year provided when submitting the jobs
ROOT.gInterpreter.Declare('auto cset = correction::CorrectionSet::from_file("JEC/2022_Summer22/jet_jerc.json.gz");')

# C++ function to apply the Jet Energy Corrections 
# TODO: Improve and make generic reading of file with the corrections (year, era, correction_name, algo)
ROOT.gInterpreter.Declare('''
ROOT::VecOps::RVec<float> JetCorPt(const ROOT::VecOps::RVec<float> &area, 
                                               const ROOT::VecOps::RVec<float> &eta,
                                               const ROOT::VecOps::RVec<float> &pt,
                                               const ROOT::VecOps::RVec<float> &rawf,
                                               const float &rho){

    ROOT::VecOps::RVec<float> Jet_corPt;

    for(unsigned int i=0; i<pt.size(); i++){
       float sf = cset->at("Summer22_22Sep2023_RunCD_V2_DATA_L1FastJet_AK4PFPuppi")->evaluate({area[i], eta[i], pt[i], rho});
       sf *= cset->at("Summer22_22Sep2023_RunCD_V2_DATA_L2Relative_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       sf *= cset->at("Summer22_22Sep2023_RunCD_V2_DATA_L3Absolute_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       Jet_corPt.push_back(sf*pt[i]);
       //std::cout << "Area: " << area[i] << "\t\t" << "Eta: " << eta[i] << "\t\t" << "Pt: " << pt[i] << "\t\t" << "Rho: " << rho << "\t\t" << "Correction: " << sf << endl;
    }

    return Jet_corPt;

}
''')
