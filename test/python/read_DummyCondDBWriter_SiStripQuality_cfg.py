# The following comments couldn't be translated into the new config version:

# upload to database 

#string timetype = "timestamp"    

import FWCore.ParameterSet.Config as cms

process = cms.Process("Reader")

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring(''),
    QualityReader = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    destinations = cms.untracked.vstring('QualityReader.log')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(1)
)

process.poolDBESSource = cms.ESSource("PoolDBESSource",
   BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
   DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(2),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:dbfile.db'),
    toGet = cms.VPSet(
    cms.PSet(record = cms.string('SiStripModuleHVRcd'),tag = cms.string('SiStripModuleHVOff_Ideal_31X')),
    cms.PSet(record = cms.string('SiStripModuleLVRcd'),tag = cms.string('SiStripModuleLVOff_Ideal_31X')),
    cms.PSet(record = cms.string('SiStripBadModuleRcd'),tag = cms.string('SiStripBadModule_Ideal_31X')),
    cms.PSet(record = cms.string('SiStripBadFiberRcd'),tag = cms.string('SiStripBadFiber_Ideal_31X')),
    cms.PSet(record = cms.string('SiStripBadChannelRcd'),tag = cms.string('SiStripBadChannel_Ideal_31X'))
    )
)

process.load("CalibTracker.SiStripESProducers.SiStripQualityESProducer_cfi")
process.siStripQualityESProducer.ListOfRecordToMerge = cms.VPSet(
     cms.PSet( record = cms.string("SiStripModuleHVRcd"), tag    = cms.string("") ),
     cms.PSet( record = cms.string("SiStripModuleLVRcd"), tag    = cms.string("") ),
     cms.PSet( record = cms.string("SiStripBadChannelRcd"), tag    = cms.string("") ),
     cms.PSet( record = cms.string("SiStripBadFiberRcd"),   tag    = cms.string("") ),
     cms.PSet( record = cms.string("SiStripBadModuleRcd"),  tag    = cms.string("") ),
     )


process.reader = cms.EDAnalyzer("SiStripQualityStatistics",
                              dataLabel = cms.untracked.string(""),
                              TkMapFileName = cms.untracked.string("")
                              )

process.p1 = cms.Path(process.reader)


