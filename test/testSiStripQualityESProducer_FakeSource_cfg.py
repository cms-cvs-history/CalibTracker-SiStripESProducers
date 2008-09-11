import FWCore.ParameterSet.Config as cms

process = cms.Process("CALIB")
process.load("CalibTracker.SiStripESProducers.SiStripQualityFakeESSource_cfi")

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('*'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    destinations = cms.untracked.vstring('cout')
)

process.source = cms.Source("EmptyIOVSource",
    lastRun = cms.untracked.uint32(100),
    timetype = cms.string('runnumber'),
    firstRun = cms.untracked.uint32(1),
    interval = cms.uint32(90)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.thistest = cms.EDProducer("testSiStripQualityESProducer",
    printDebug = cms.untracked.bool(True),
    twoRecordComparison = cms.untracked.bool(False),
    dataLabelTwo = cms.untracked.string('test2'),
    dataLabel = cms.untracked.string('')
)

process.printp = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path(process.thistest)
process.ep = cms.EndPath(process.printp)

