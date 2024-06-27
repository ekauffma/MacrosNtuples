#ifndef HELPER_FOURVECTOR
#define HELPER_FOURVECTOR

#include <string>

#include "ROOT/RVec.hxx"
#include <Math/Vector4D.h>

inline ROOT::RVec<ROOT::Math::PxPyPzMVector> ConstructP4 (const ROOT::RVecD & Pt, const ROOT::RVecD & Eta, const ROOT::RVecD & Phi, const ROOT::RVecD & M)
{

    return ROOT::VecOps::Construct<ROOT::Math::PxPyPzMVector>(
		ROOT::VecOps::Construct<ROOT::Math::PtEtaPhiMVector>(
			Pt,
			Eta,
			Phi,
			M
		)
	);
}

#endif
