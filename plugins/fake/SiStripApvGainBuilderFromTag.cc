#include "CalibTracker/SiStripESProducers/plugins/fake/SiStripApvGainBuilderFromTag.h"
#include "CalibTracker/SiStripCommon/interface/SiStripDetInfoFileReader.h"
#include "CondFormats/DataRecord/interface/SiStripCondDataRecords.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

SiStripApvGainBuilderFromTag::SiStripApvGainBuilderFromTag( const edm::ParameterSet& iConfig ):
  fp_(iConfig.getUntrackedParameter<edm::FileInPath>("file",edm::FileInPath("CalibTracker/SiStripCommon/data/SiStripDetInfo.dat"))),
  printdebug_(iConfig.getUntrackedParameter<uint32_t>("printDebug",1)),
  pset_(iConfig)
{}

void SiStripApvGainBuilderFromTag::analyze(const edm::Event& evt, const edm::EventSetup& iSetup)
{
  //   unsigned int run=evt.id().run();

  std::string genMode = pset_.getParameter<std::string>("genMode");

  double meanGain_=pset_.getParameter<double>("MeanGain");
  double sigmaGain_=pset_.getParameter<double>("SigmaGain");
  double minimumPosValue_=pset_.getParameter<double>("MinPositiveGain");

  uint32_t  printdebug_ = pset_.getUntrackedParameter<uint32_t>("printDebug", 5);

  // Read the gain from the given tag
  edm::ESHandle<SiStripApvGain> inputApvGain;
  iSetup.get<SiStripApvGainRcd>().get( inputApvGain );
  vector<uint32_t> inputDetIds;
  inputApvGain->getDetIds(inputDetIds);

  // Prepare the new object
  SiStripApvGain* obj = new SiStripApvGain();

  SiStripDetInfoFileReader reader(fp_.fullPath());

  uint32_t count = 0;
  const std::map<uint32_t, SiStripDetInfoFileReader::DetInfo > DetInfos = reader.getAllData();
  for(std::map<uint32_t, SiStripDetInfoFileReader::DetInfo >::const_iterator it = DetInfos.begin(); it != DetInfos.end(); it++) {

    // Find if this DetId is in the input tag and if so how many are the Apvs for which it contains information
    SiStripApvGain::Range inputRange;
    size_t inputRangeSize = 0;
    if( find( inputDetIds.begin(), inputDetIds.end(), it->first ) != inputDetIds.end() ) {
      inputRange = inputApvGain->getRange(it->first);
      inputRangeSize = distance(inputRange.first, inputRange.second);
    }

    std::vector<float> theSiStripVector;
    for(unsigned short j=0; j<it->second.nApvs; j++){

      double gainValue = meanGain_;

      if( j < inputRangeSize ) {
        // cout << "Gain from input tag for DetId = " << it->first << " and apv = " << j << endl;
        gainValue = inputApvGain->getApvGain(j, inputRange);
      }
      // else {
      //   cout << "No gain in input tag for DetId = " << it->first << " and apv = " << j << " using value from cfg = " << gainValue << endl;
      // }
  
      if(genMode=="default")
	gainValue=meanGain_;
      else if ("gaussian") {
	gainValue = CLHEP::RandGauss::shoot(meanGain_, sigmaGain_);
	if(gainValue<=minimumPosValue_) gainValue=minimumPosValue_;
      }
      else {
        LogDebug("SiStripApvGain") << "ERROR: wrong genMode specifier : " << genMode << ", please select one of \"default\" or \"gaussian\"" << std::endl;
        exit(1);
      }
	
      if (count<printdebug_) {
	edm::LogInfo("SiStripApvGainGeneratorFromTag") << "detid: " << it->first  << " Apv: " << j <<  " gain: " << gainValue  << std::endl; 	    
      }
      theSiStripVector.push_back(gainValue);
    }
    count++;
    SiStripApvGain::Range range(theSiStripVector.begin(),theSiStripVector.end());
    if ( ! obj->put(it->first,range) )
      edm::LogError("SiStripApvGainGeneratorFromTag")<<" detid already exists"<<std::endl;
  }
  
  //End now write data in DB
  edm::Service<cond::service::PoolDBOutputService> mydbservice;
  
  if( mydbservice.isAvailable() ){
    if( mydbservice->isNewTagRequest("SiStripApvGainRcd2") ){
      mydbservice->createNewIOV<SiStripApvGain>(obj,mydbservice->beginOfTime(),mydbservice->endOfTime(),"SiStripApvGainRcd2");      
    }
    else {
      mydbservice->appendSinceTime<SiStripApvGain>(obj,mydbservice->currentTime(),"SiStripApvGainRcd2");      
    }
  }
  else {
    edm::LogError("SiStripApvGainBuilderFromTag")<<"Service is unavailable"<<std::endl;
  }
}
     