# The following comments couldn't be translated into the new config version:

# upload to database 

#string timetype = "timestamp"    

import FWCore.ParameterSet.Config as cms

process = cms.Process("Reader")

# Use this to have also debug info (WARNING: the resulting file is > 200MB.
process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring("*"),
    GainReaderSummary = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    GainReaderDebug = cms.untracked.PSet(
        threshold = cms.untracked.string('DEBUG')
    ),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    destinations = cms.untracked.vstring('GainReaderSummary', 'GainReaderDebug')
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(100000)
)

process.load("CalibTracker.SiStripESProducers.SiStripGainSimESProducer_cfi")

process.poolDBESSource = cms.ESSource("PoolDBESSource",
   BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
   DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(2),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:dbfile.db'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('SiStripApvGainSimRcd'),
        tag = cms.string('SiStripApvGain_Fake_30X')
    ))
)

process.reader = cms.EDFilter("SiStripGainSimDummyPrinter")
                              
process.p1 = cms.Path(process.reader)


