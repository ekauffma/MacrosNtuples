import ROOT

## Importing stuff from other python files 
from trigger import *
from binning import *
from corrections import *
from jecs import *

# C++ function to find the index of the leading pt jet
ROOT.gInterpreter.Declare('''
inline int FindLeadingIndex(const ROOT::VecOps::RVec<float> &pt){

    int index = 0;
    double max = pt[0];
    for(unsigned int i=0; i<pt.size(); i++){
       if(pt[i] > max){
          max = pt[i];
          index = i;
       }
    }

    return index;

}
''')

## C++ function for alpha calculation
ROOT.gInterpreter.Declare('''
inline float Alpha_func(ROOT::VecOps::RVec<float> &pt_jet, const float pt_ref){

    // Sort jets in decreasing order of pT
    std::sort(pt_jet.begin(), pt_jet.end(), std::greater<>());
    return pt_jet.size()>1 ? pt_jet[1]/pt_ref : 0.0;

}
''')

def SinglePhotonSelection(df, triggers):
    '''
    Select events with exactly one photon with pT>115 GeV.
    The event must pass a photon trigger (for now 110 GeV unprescaled trigger only)
    '''
    df = df.Filter(TriggerFired(triggers),'trigger single photon')

    df = df.Define('photonsptgt115','Photon_pt>115&&Photon_pfChargedIsoPFPV<0.2')
    df = df.Filter('Sum(photonsptgt115)==1','=1 photon with p_{T}>115 GeV')

    df = df.Define('isRefPhoton','Photon_mvaID_WP80&&Photon_electronVeto&&Photon_pfChargedIsoPFPV<0.03&&Photon_pfRelIso03_all_quadratic<0.05&&abs(Photon_eta)<1.479&&'+TriggerSelect(triggers))
    
    df = df.Filter('Sum(isRefPhoton)==1','Photon passes tight ID and is in EB')
    
    df = df.Define('cleanPh_Pt','Photon_pt[isRefPhoton]')
    df = df.Define('cleanPh_Eta','Photon_eta[isRefPhoton]')
    df = df.Define('cleanPh_Phi','Photon_phi[isRefPhoton]')
    
    df = df.Define('ref_Pt','cleanPh_Pt[0]')
    df = df.Define('ref_Phi','cleanPh_Phi[0]')
    
    return df


def CleanJets(df, JEC, year, era, isData):
    # List of cleaned jets (noise cleaning + lepton/photon overlap removal)
    df = df.Define('_jetPassID', 'Jet_jetId>=6')

    # Apply (or not) the newest Jet Energy Corrections: Note Jet_pt is the corrected pt but not with the latest JECs
    # Based on the JEC flag we have the raw jet pT (JEC=False) or the re-corrected jet pT (JEC=True)
    # After refinition of the column, jets are not yet ordered in pt
    df = df.Redefine('Jet_pt', 'JetRawPt(Jet_pt, Jet_rawFactor)')
    if JEC:
       JECfile, corrfile = JECsInit(year, era, isData)
       df = df.Define('JECfile', '"{}"'.format(JECfile))
       df = df.Define('corrfile', '"{}"'.format(corrfile))
       # Apply the JECs
       df = df.Redefine('Jet_pt', 'JetCorPt(Jet_area, Jet_eta, Jet_pt, Jet_rawFactor, Rho_fixedGridRhoFastjetAll, JECfile, corrfile)')
 
    # Next line to make sure we remove the leptons/the photon
    df = df.Define('isCleanJet','_jetPassID&&(Jet_pt>30||(Jet_pt>20&&abs(Jet_eta)<2.4))&&Jet_muEF<0.5&&Jet_chEmEF<0.5&&Jet_neEmEF<0.8')

    # Get the jet variables
    df = df.Define('cleanJet_Pt','Jet_pt[isCleanJet]')
    df = df.Define('cleanJet_Eta','Jet_eta[isCleanJet]')
    df = df.Define('cleanJet_Phi','Jet_phi[isCleanJet]')
    df = df.Filter('Sum(isCleanJet)>=1','>=1 clean jet with p_{T}>20/30 GeV')

    # Next line to find the leading pt jet in the jet list
    # Note: we do not use sort, since we use Pt, Eta and Phi from the leading jet
    df = df.Define('leading_jet', 'FindLeadingIndex(cleanJet_Pt)')

    # For the subleading jet (alpha calculation) we do not apply any pt cut
    df = df.Define('isCleanJet_noPtcut','_jetPassID&&Jet_muEF<0.5&&Jet_chEmEF<0.5&&Jet_neEmEF<0.8')
    df = df.Define('cleanJet_Pt_noPtcut','Jet_pt[isCleanJet_noPtcut]')

    return df

    
def PtBalanceSelection(df):
    '''
    Compute pt balance = pt(jet)/pt(ref) and alpha=pt(subleading_jet)/pt(ref)
    ref can be a photon or a Z.
    '''
    # Back to back condition
    df = df.Filter('abs(acos(cos(ref_Phi-cleanJet_Phi[leading_jet])))>2.9','DeltaPhi(ph,jet)>2.9')

    # Compute Pt balance = pt(jet)/pt(ref)    
    df = df.Define('ptbalance','cleanJet_Pt[leading_jet]/ref_Pt')
    df = df.Define('probe_Eta','cleanJet_Eta[leading_jet]')
    df = df.Define('probe_Phi','cleanJet_Phi[leading_jet]')

    # Compute alpha=pt(subleading_jet)/pt(ref) using the Alpha_func
    # Sort the jet pts (for sub_leading jet we only need the pt) and take the sub-leading
    df = df.Define('alpha','Alpha_func(cleanJet_Pt_noPtcut,ref_Pt)')

    return df


def AnalyzePtBalance(df, JEC, isData):
    histos = {}                                 # Dictionary for histograms (one histo per eta, alpha and ref_Pt)
    df_ptBalanceBinnedInEtaAndAlphaPerPt = {}   # RDataFrame for filtering on eta, alpha and ref_Pt bins

    suffix = '_rawPt'
    if JEC:
       suffix = '_corPt'

    if isData: suffix += '_Data'
    else: suffix += '_MC'

    # Loop over eta bins
    for e in range(NetaBins):
        # Loop over alpha bins
        for a in range(NalphaBins):
            # Loop over pt bins
            for p in range(NptBins):
                # Filtering on eta, alpha and pt bins
                key = '_' + str_binetas[e] + '_' + str_binalphas[a] + '_' + str_binpts[p]
                df_ptBalanceBinnedInEtaAndAlphaPerPt[key] = df.Filter('abs(cleanJet_Eta[leading_jet])>={}&&abs(cleanJet_Eta[leading_jet])<{}'.format(jetetaBins[e], jetetaBins[e+1]))\
                                                              .Filter('alpha>={}&&alpha<{}'.format(alphaBins[a], alphaBins[a+1]))\
                                                              .Filter('ref_Pt>={}&&ref_Pt<{}'.format(jetptBins[p], jetptBins[p+1]))

                # One histogram per eta, alpha, ref_Pt bin
                histos['balancevsrefpt' + key + suffix] = df_ptBalanceBinnedInEtaAndAlphaPerPt[key]\
                                                          .Histo2D(ROOT.RDF.TH2DModel('h_BalanceVsRefPt{}'.format(key)+suffix,'ptbalance',\
                                                          NptBins, jetptBins, NptbalanceBins, ptbalanceBins), 'ref_Pt', 'ptbalance', 'LHEWeight_originalXWGTUP')

    return df, histos
