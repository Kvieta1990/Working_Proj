from mantid.simpleapi import *
import numpy as np
import datetime

# Sample - diamond
sfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_172183.nxs.h5'
samplename_noc = 'Dia_wo_coll'

# Empty Can
mfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_172214.nxs.h5'
mtname_noc = 'MTC_wo_coll'

# Vrod
vrodfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_172215.nxs.h5'
vrodname_noc = 'Vrod_wo_coll'

# MT Shifter
mtfilename_noc = "/SNS/NOM/IPTS-28922/nexus/NOM_172226.nxs.h5"
mtiname_noc = 'MT_wo_coll'

# Cal
calfile_noc = '/SNS/NOM/shared/Mantid_total_Scattering_Jue/NOMAD_172183_2022-05-19_shifter.h5'

now = datetime.datetime.now()
print('Information collected, now heading to work...')
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Mask
mask_wo_coll = range(0, 7168)
mask_w_coll = range(7168,14336)
mask_wo_coll_used = list()
mask_w_coll_used = list()

Load(Filename=sfilename_noc, OutputWorkspace=samplename_noc)
Load(Filename=mfilename_noc, OutputWorkspace=mtname_noc)
Load(Filename=vrodfilename_noc, OutputWorkspace=vrodname_noc)
Load(Filename=mtfilename_noc, OutputWorkspace=mtiname_noc)

info = mtd[samplename_noc].detectorInfo()
det_ids = info.detectorIDs()
for detid in det_ids[2:]:
    if detid not in mask_wo_coll:
        mask_wo_coll_used.append(int(detid))
for detid in det_ids[2:]:
    if detid not in mask_w_coll:
        mask_w_coll_used.append(int(detid))
MaskDetectors(samplename_noc, DetectorList=mask_wo_coll_used)
MaskDetectors(mtname_noc, DetectorList=mask_wo_coll_used)
MaskDetectors(vrodname_noc, DetectorList=mask_wo_coll_used)
MaskDetectors(mtiname_noc, DetectorList=mask_wo_coll_used)

LoadDiffCal(InputWorkspace=samplename_noc, Filename=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=samplename_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=mtname_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=vrodname_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=mtiname_noc, CalibrationFile=calfile_noc)

group_all = CreateGroupingWorkspace(InputWorkspace=samplename_noc,
                                    GroupDetectorsBy="All")
AlignAndFocusPowder(InputWorkspace=samplename_noc,
                    OutputWorkspace=samplename_noc + '_data_focussed',
                    UnfocussedWorkspace=samplename_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=mtname_noc,
                    OutputWorkspace=mtname_noc + '_data_focussed',
                    UnfocussedWorkspace=mtname_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=vrodname_noc,
                    OutputWorkspace=vrodname_noc + '_data_focussed',
                    UnfocussedWorkspace=vrodname_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=mtiname_noc,
                    OutputWorkspace=mtiname_noc + '_data_focussed',
                    UnfocussedWorkspace=mtiname_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')

NormaliseByCurrent(InputWorkspace=samplename_noc + '_data_focussed',
                   OutputWorkspace=samplename_noc + '_data_focussed',
                   RecalculatePCharge=True)
NormaliseByCurrent(InputWorkspace=mtname_noc + '_data_focussed',
                   OutputWorkspace=mtname_noc + '_data_focussed',
                   RecalculatePCharge=True)
NormaliseByCurrent(InputWorkspace=vrodname_noc + '_data_focussed',
                   OutputWorkspace=vrodname_noc + '_data_focussed',
                   RecalculatePCharge=True)
NormaliseByCurrent(InputWorkspace=mtiname_noc + '_data_focussed',
                   OutputWorkspace=mtiname_noc + '_data_focussed',
                   RecalculatePCharge=True)

ConvertUnits(InputWorkspace=samplename_noc + '_data_focussed',
             OutputWorkspace=samplename_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=mtname_noc + '_data_focussed',
             OutputWorkspace=mtname_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=vrodname_noc + '_data_focussed',
             OutputWorkspace=vrodname_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=mtiname_noc + '_data_focussed',
             OutputWorkspace=mtiname_noc + '_data_focussed_d',
             Target='dSpacing')

Rebin(InputWorkspace=samplename_noc + '_data_focussed_d',
      OutputWorkspace=samplename_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=mtname_noc + '_data_focussed_d',
      OutputWorkspace=mtname_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=vrodname_noc + '_data_focussed_d',
      OutputWorkspace=vrodname_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=mtiname_noc + '_data_focussed_d',
      OutputWorkspace=mtiname_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)

sample_norm = Divide(samplename_noc + '_data_focussed_d_binned',
                     vrodname_noc + '_data_focussed_d_binned')
mtc_norm = Divide(mtname_noc + '_data_focussed_d_binned',
                  vrodname_noc + '_data_focussed_d_binned')
vrod_m_mti = Minus(vrodname_noc + '_data_focussed_d_binned',
                   mtiname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm = Minus(samplename_noc + '_data_focussed_d_binned',
                          mtname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm_1 = Divide(sample_m_mtc_norm,
                             vrodname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm = Divide(sample_m_mtc_norm,
                           vrod_m_mti)
mtc_m_mti = Minus(mtname_noc + '_data_focussed_d_binned',
                  mtiname_noc + '_data_focussed_d_binned')
mtc_m_mti_norm = Divide(mtc_m_mti,
                        vrod_m_mti)

ConvertToPointData(InputWorkspace='vrod_m_mti',
                   OutputWorkspace='vrod_m_mti')
ConvertToPointData(InputWorkspace='sample_norm',
                   OutputWorkspace='sample_norm')
ConvertToPointData(InputWorkspace=mtname_noc + '_data_focussed_d_binned',
                   OutputWorkspace=mtname_noc + '_data_focussed_d_binned')
ConvertToPointData(InputWorkspace=mtiname_noc + '_data_focussed_d_binned',
                   OutputWorkspace=mtiname_noc + '_data_focussed_d_binned')
ConvertToPointData(InputWorkspace='mtc_norm',
                   OutputWorkspace='mtc_norm')
ConvertToPointData(InputWorkspace='sample_m_mtc_norm',
                   OutputWorkspace='sample_m_mtc_norm')
ConvertToPointData(InputWorkspace='sample_m_mtc_norm_1',
                   OutputWorkspace='sample_m_mtc_norm_1')
ConvertToPointData(InputWorkspace='mtc_m_mti',
                   OutputWorkspace='mtc_m_mti')
ConvertToPointData(InputWorkspace='mtc_m_mti_norm',
                   OutputWorkspace='mtc_m_mti_norm')

x_val = mtd['sample_norm'].readX(0)
y_mtc = mtd[mtname_noc + '_data_focussed_d_binned'].readY(0)
y_mti = mtd[mtiname_noc + '_data_focussed_d_binned'].readY(0)
y_mtc_m_mti = mtd['mtc_m_mti'].readY(0)
y_mtc_m_mti_norm = mtd['mtc_m_mti_norm'].readY(0)
y_sample_m_mtc_norm = mtd['sample_m_mtc_norm'].readY(0)
y_sample_m_mtc_norm_1 = mtd['sample_m_mtc_norm_1'].readY(0)
van_out = mtd['vrod_m_mti'].readY(0)

file_out = open("coll_test_wo_coll_matt.out", "w")
for count, item in enumerate(x_val):
    file_out.write("{0:20.5F}{1:20.5F}{2:20.5F}{3:20.5F}{4:20.5F}{5:20.5F}{6:20.5F}\n".format(item,
                                                                                              y_sample_m_mtc_norm[count],
                                                                                              y_mtc[count],
                                                                                              y_mti[count],
                                                                                              y_mtc_m_mti[count],
                                                                                              y_mtc_m_mti_norm[count],
                                                                                              y_sample_m_mtc_norm_1[count]))
file_out.close()

file_out = open('coll_test_wo_coll_van_' + "matt.out", "w")
for count, item in enumerate(x_val):
    file_out.write("{0:20.5F}{1:20.5F}\n".format(item, van_out[count]))

file_out.close()

Load(Filename=sfilename_noc, OutputWorkspace=samplename_noc)
Load(Filename=mfilename_noc, OutputWorkspace=mtname_noc)
Load(Filename=vrodfilename_noc, OutputWorkspace=vrodname_noc)
Load(Filename=mtfilename_noc, OutputWorkspace=mtiname_noc)

MaskDetectors(samplename_noc, DetectorList=mask_w_coll_used)
MaskDetectors(mtname_noc, DetectorList=mask_w_coll_used)
MaskDetectors(vrodname_noc, DetectorList=mask_w_coll_used)
MaskDetectors(mtiname_noc, DetectorList=mask_w_coll_used)

LoadDiffCal(InputWorkspace=samplename_noc, Filename=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=samplename_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=mtname_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=vrodname_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=mtiname_noc, CalibrationFile=calfile_noc)

AlignAndFocusPowder(InputWorkspace=samplename_noc,
                    OutputWorkspace=samplename_noc + '_data_focussed',
                    UnfocussedWorkspace=samplename_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=mtname_noc,
                    OutputWorkspace=mtname_noc + '_data_focussed',
                    UnfocussedWorkspace=mtname_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=vrodname_noc,
                    OutputWorkspace=vrodname_noc + '_data_focussed',
                    UnfocussedWorkspace=vrodname_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=mtiname_noc,
                    OutputWorkspace=mtiname_noc + '_data_focussed',
                    UnfocussedWorkspace=mtiname_noc + '_data_not_foc',
                    CalFileName=calfile_noc,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')

NormaliseByCurrent(InputWorkspace=samplename_noc + '_data_focussed',
                   OutputWorkspace=samplename_noc + '_data_focussed',
                   RecalculatePCharge=True)
NormaliseByCurrent(InputWorkspace=mtname_noc + '_data_focussed',
                   OutputWorkspace=mtname_noc + '_data_focussed',
                   RecalculatePCharge=True)
NormaliseByCurrent(InputWorkspace=vrodname_noc + '_data_focussed',
                   OutputWorkspace=vrodname_noc + '_data_focussed',
                   RecalculatePCharge=True)
NormaliseByCurrent(InputWorkspace=mtiname_noc + '_data_focussed',
                   OutputWorkspace=mtiname_noc + '_data_focussed',
                   RecalculatePCharge=True)

ConvertUnits(InputWorkspace=samplename_noc + '_data_focussed',
             OutputWorkspace=samplename_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=mtname_noc + '_data_focussed',
             OutputWorkspace=mtname_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=vrodname_noc + '_data_focussed',
             OutputWorkspace=vrodname_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=mtiname_noc + '_data_focussed',
             OutputWorkspace=mtiname_noc + '_data_focussed_d',
             Target='dSpacing')

Rebin(InputWorkspace=samplename_noc + '_data_focussed_d',
      OutputWorkspace=samplename_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=mtname_noc + '_data_focussed_d',
      OutputWorkspace=mtname_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=vrodname_noc + '_data_focussed_d',
      OutputWorkspace=vrodname_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=mtiname_noc + '_data_focussed_d',
      OutputWorkspace=mtiname_noc + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)

sample_norm = Divide(samplename_noc + '_data_focussed_d_binned',
                     vrodname_noc + '_data_focussed_d_binned')
mtc_norm = Divide(mtname_noc + '_data_focussed_d_binned',
                  vrodname_noc + '_data_focussed_d_binned')
vrod_m_mti = Minus(vrodname_noc + '_data_focussed_d_binned',
                   mtiname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm = Minus(samplename_noc + '_data_focussed_d_binned',
                          mtname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm_1 = Divide(sample_m_mtc_norm,
                             vrodname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm = Divide(sample_m_mtc_norm,
                           vrod_m_mti)
mtc_m_mti = Minus(mtname_noc + '_data_focussed_d_binned',
                  mtiname_noc + '_data_focussed_d_binned')
mtc_m_mti_norm = Divide(mtc_m_mti,
                        vrod_m_mti)

ConvertToPointData(InputWorkspace='vrod_m_mti',
                   OutputWorkspace='vrod_m_mti')
ConvertToPointData(InputWorkspace='sample_norm',
                   OutputWorkspace='sample_norm')
ConvertToPointData(InputWorkspace=mtname_noc + '_data_focussed_d_binned',
                   OutputWorkspace=mtname_noc + '_data_focussed_d_binned')
ConvertToPointData(InputWorkspace=mtiname_noc + '_data_focussed_d_binned',
                   OutputWorkspace=mtiname_noc + '_data_focussed_d_binned')
ConvertToPointData(InputWorkspace='mtc_norm',
                   OutputWorkspace='mtc_norm')
ConvertToPointData(InputWorkspace='sample_m_mtc_norm',
                   OutputWorkspace='sample_m_mtc_norm')
ConvertToPointData(InputWorkspace='sample_m_mtc_norm_1',
                   OutputWorkspace='sample_m_mtc_norm_1')
ConvertToPointData(InputWorkspace='mtc_m_mti',
                   OutputWorkspace='mtc_m_mti')
ConvertToPointData(InputWorkspace='mtc_m_mti_norm',
                   OutputWorkspace='mtc_m_mti_norm')

x_val = mtd['sample_norm'].readX(0)
y_mtc = mtd[mtname_noc + '_data_focussed_d_binned'].readY(0)
y_mti = mtd[mtiname_noc + '_data_focussed_d_binned'].readY(0)
y_mtc_m_mti = mtd['mtc_m_mti'].readY(0)
y_mtc_m_mti_norm = mtd['mtc_m_mti_norm'].readY(0)
y_sample_m_mtc_norm = mtd['sample_m_mtc_norm'].readY(0)
y_sample_m_mtc_norm_1 = mtd['sample_m_mtc_norm_1'].readY(0)
van_out = mtd['vrod_m_mti'].readY(0)

file_out = open("coll_test_w_coll_matt.out", "w")
for count, item in enumerate(x_val):
    file_out.write("{0:20.5F}{1:20.5F}{2:20.5F}{3:20.5F}{4:20.5F}{5:20.5F}{6:20.5F}\n".format(item,
                                                                                              y_sample_m_mtc_norm[count],
                                                                                              y_mtc[count],
                                                                                              y_mti[count],
                                                                                              y_mtc_m_mti[count],
                                                                                              y_mtc_m_mti_norm[count],
                                                                                              y_sample_m_mtc_norm_1[count]))
file_out.close()

file_out = open('coll_test_w_coll_van_' + "matt.out", "w")
for count, item in enumerate(x_val):
    file_out.write("{0:20.5F}{1:20.5F}\n".format(item, van_out[count]))

file_out.close()

now = datetime.datetime.now()
print('Job done!')
print(now.strftime("%Y-%m-%d %H:%M:%S"))
