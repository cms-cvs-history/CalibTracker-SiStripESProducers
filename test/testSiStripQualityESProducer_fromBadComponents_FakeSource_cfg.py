import FWCore.ParameterSet.Config as cms

process = cms.Process("CALIB")

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

# process.load("CalibTracker.SiStripESProducers.SiStripQualityConfigurableFakeESSource_cfi")
# process.siStripQualityConfigurableFakeESSource.BadComponentList = cms.untracked.VPSet(
#     cms.PSet(
#         SubDet = cms.string('TIB'),  
#         layer = cms.uint32(0),        ## SELECTION: layer = 1..4, 0(ALL)		    
#         bkw_frw = cms.uint32(0),      ## bkw_frw = 1(TIB-), 2(TIB+) 0(ALL)	    
#         detid = cms.uint32(0),        ## int_ext = 1 (internal), 2(external), 0(ALL)  
#         ster = cms.uint32(0),         ## ster = 1(stereo), 2 (nonstereo), 0(ALL)	    
#         string_ = cms.uint32(0),      ## string = 1..N, 0(ALL)			    
#         int_ext = cms.uint32(0)       ## detid number = 0 (ALL),  specific number     
#         )
#     )

process.load("CalibTracker.Configuration.Tracker_FakeConditions_cff")
process.load("CalibTracker.Configuration.Tracker_DependentRecords_forGlobalTag_cff")

process.thistest = cms.EDProducer("testSiStripQualityESProducer",
    printDebug = cms.untracked.bool(True),
    twoRecordComparison = cms.untracked.bool(False),
    dataLabelTwo = cms.untracked.string('test2'),
    dataLabel = cms.untracked.string('')
)

process.printp = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path(process.thistest)
process.ep = cms.EndPath(process.printp)

