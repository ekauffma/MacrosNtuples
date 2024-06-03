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


# C++ function to apply the Jet Energy Corrections 
ROOT.gInterpreter.Declare('''
ROOT::VecOps::RVec<float> JetCorPt(const ROOT::VecOps::RVec<float> &area, 
                                               const ROOT::VecOps::RVec<float> &eta,
                                               const ROOT::VecOps::RVec<float> &pt,
                                               const ROOT::VecOps::RVec<float> &rawf,
                                               const float &rho,
                                               const string &JECfile,
                                               const string &corrfile){

    ROOT::VecOps::RVec<float> Jet_corPt;

    auto cset = correction::CorrectionSet::from_file(JECfile);

    //std::cout << "Reading Jet Energy Corrections from files: " << corrfile << endl;

    for(unsigned int i=0; i<pt.size(); i++){
       //std::cout << "Raw pt is: " << pt[i] << "\t\t";
       float sf = cset->at(corrfile + "L1FastJet_AK4PFPuppi")->evaluate({area[i], eta[i], pt[i], rho});
       sf *= cset->at(corrfile + "L2Relative_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       sf *= cset->at(corrfile + "L3Absolute_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       sf *= cset->at(corrfile + "L2L3Residual_AK4PFPuppi")->evaluate({eta[i], pt[i]});
       Jet_corPt.push_back(sf*pt[i]);
       //std::cout << "Area: " << area[i] << "\t\t" << "Eta: " << eta[i] << "\t\t" << "Pt: " << pt[i] << "\t\t" << "Rho: " << rho << "\t\t" << "Correction: " << sf << endl;
    }

    return Jet_corPt;

}
''')
