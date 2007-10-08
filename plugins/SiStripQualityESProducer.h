#ifndef CalibTracker_SiStripESProducers_SiStripQualityESProducer
#define CalibTracker_SiStripESProducers_SiStripQualityESProducer

// system include files
#include <memory>
#include "boost/shared_ptr.hpp"

// user include files
#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/ESProducer.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/SiStripCommon/interface/SiStripConstants.h"
#include "CalibFormats/SiStripObjects/interface/SiStripQuality.h"
#include "CalibTracker/Records/interface/SiStripQualityRcd.h"
#include "CondFormats/DataRecord/interface/SiStripBadStripRcd.h"
#include "CondFormats/DataRecord/interface/SiStripBadModuleRcd.h"
#include "CondFormats/DataRecord/interface/SiStripBadFiberRcd.h"
#include "CondFormats/DataRecord/interface/SiStripBadChannelRcd.h"


class SiStripQualityESProducer : public edm::ESProducer {
 public:
  SiStripQualityESProducer(const edm::ParameterSet&);
  ~SiStripQualityESProducer(){};
  
  boost::shared_ptr<SiStripQuality> produce(const SiStripQualityRcd&);
   
 private:

  /*
  void SiStripBadChannelCallback(const SiStripBadFiberRcd&  iRec);
  void SiStripBadFiberCallback  (const SiStripBadFiberRcd&  iRec);
  void SiStripBadModuleCallback (const SiStripBadModuleRcd& iRec);
  */
  
  edm::ParameterSet pset_; 
  edm::FileInPath fp_;
  bool MergeList_; 

   typedef std::vector< edm::ParameterSet > Parameters;
  Parameters toGet;

};

#endif
