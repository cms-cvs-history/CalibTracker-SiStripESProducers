# Template used by the UploadAll.py scripts to generate the cfgs for the DummyPrinter
# The only templated value is SiStripLorentzAngle (e.g TAGNAME -> SiStripApvGain).
# To generate manually a cfg from this file please do for example:
# cat DummyCondDBReaderTemplate_cfg.py | sed -e "s@SiStripLorentzAngle@SiStripApvGain@" > DummyCondDBReader_SiStripApvGain_cfg.py
import FWCore.ParameterSet.Config as cms

process = cms.Process("Reader")

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring(''),
    SiStripLorentzAngleReader = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    ),
    destinations = cms.untracked.vstring('SiStripLorentzAngleReader_Ideal.log')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(100354)
)

process.poolDBESSource = cms.ESSource("PoolDBESSource",
   BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
   DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(2),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('oracle://cms_orcoff_prod/CMS_COND_31X_STRIP'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('SiStripLorentzAngleRcd'),
        tag = cms.string('SiStripLorentzAngle_GR09_31X_v3_hlt')
    ))
)

process.reader = cms.EDFilter("SiStripLorentzAngleDummyPrinter")


process.p1 = cms.Path(process.reader)


