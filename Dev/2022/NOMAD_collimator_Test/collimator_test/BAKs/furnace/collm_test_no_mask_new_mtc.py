from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Eight packs to compare
ep_to_compare_str = "38-51, 52-57, 8, 14, 27"
ep_tp_compare = []
for item in ep_to_compare_str.split(","):
    if "-" in item:
        tmp_list = list(range(int(item.split("-")[0]), int(item.split("-")[1]) + 1))
        ep_tp_compare.append(tmp_list)
    else:
        ep_tp_compare.append([int(item)])
ep_tp_compare.append([8, 14])

# -------------- w/o collimator --------------

# Sample - diamond
sfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_170226.nxs.h5'
samplename_noc = 'Dia_wo_coll'

# Empty Can
mfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_170228.nxs.h5'
mtname_noc = 'MTC_wo_coll'

# Vrod
vrodfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_170586.nxs.h5'
vrodname_noc = 'Vrod_wo_coll'

# Cal
calfile_noc = '/SNS/NOM/shared/CALIBRATION/Collimator_Test/NOMAD_170226_2022-02-17_furnace.h5'

# -------------- w/ collimator --------------

# Sample - diamond
sfilename_c = '/SNS/NOM/IPTS-28922/nexus/NOM_179845.nxs.h5'
samplename_c = 'Dia_w_coll'

# Empty Can
mfilename_c = '/SNS/NOM/IPTS-28922/nexus/NOM_179846.nxs.h5'
mtname_c = 'MTC_w_coll'

# Vrod
vrodfilename_c = '/SNS/NOM/IPTS-28922/nexus/NOM_179843.nxs.h5'
vrodname_c = 'Vrod_w_coll'

# Cal
calfile_c = '/SNS/NOM/shared/CALIBRATION/Collimator_Test/NOMAD_179845_2022-06-16_furnace.h5'

now = datetime.datetime.now()
print('Information collected, now heading to work...')
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Mask generation
mask_det_ids = []
Load(Filename=sfilename_noc, OutputWorkspace="tmp_mask_gen")
group_by_bank = CreateGroupingWorkspace(InputWorkspace=mtd["tmp_mask_gen"], GroupDetectorsBy="bank")
for count, item in enumerate(ep_tp_compare):
    mask_det_ids.append([])
    for i in range(mtd["group_by_bank"].getNumberHistograms()):
        if mtd["group_by_bank"].readY(i)[0] not in item:
            mask_det_ids[count].append(i)

mask_det = mask_det_ids[1]
fig, axs = plt.subplots(1, 1, figsize=(18, 11))

axs.set(xlabel='d-spacing (angstrom)', ylabel='Int. (a. u.)')

axs.label_outer()

# w/o collimator
Load(Filename=sfilename_noc, OutputWorkspace=samplename_noc)
Load(Filename=mfilename_noc, OutputWorkspace=mtname_noc)
Load(Filename=vrodfilename_noc, OutputWorkspace=vrodname_noc)

MaskDetectors(samplename_noc, DetectorList=mask_det)
MaskDetectors(mtname_noc, DetectorList=mask_det)
MaskDetectors(vrodname_noc, DetectorList=mask_det)

LoadDiffCal(InputWorkspace=samplename_noc, Filename=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=samplename_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=mtname_noc, CalibrationFile=calfile_noc)
ApplyDiffCal(InstrumentWorkspace=vrodname_noc, CalibrationFile=calfile_noc)

group_all = CreateGroupingWorkspace(InputWorkspace=mtd["tmp_mask_gen"],
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

ConvertUnits(InputWorkspace=samplename_noc + '_data_focussed',
             OutputWorkspace=samplename_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=mtname_noc + '_data_focussed',
             OutputWorkspace=mtname_noc + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=vrodname_noc + '_data_focussed',
             OutputWorkspace=vrodname_noc + '_data_focussed_d',
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

sample_norm = Divide(samplename_noc + '_data_focussed_d_binned',
                     vrodname_noc + '_data_focussed_d_binned')
mtc_norm = Divide(mtname_noc + '_data_focussed_d_binned',
                  vrodname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm = Minus(samplename_noc + '_data_focussed_d_binned',
                          mtname_noc + '_data_focussed_d_binned')
sample_m_mtc_norm = Divide(sample_m_mtc_norm,
                           vrodname_noc + '_data_focussed_d_binned')

ConvertToPointData(InputWorkspace='sample_norm',
                   OutputWorkspace='sample_norm')
ConvertToPointData(InputWorkspace='mtc_norm',
                   OutputWorkspace='mtc_norm')
ConvertToPointData(InputWorkspace='sample_m_mtc_norm',
                   OutputWorkspace='sample_m_mtc_norm')

x_val = mtd['sample_norm'].readX(0)
y_sample_norm = mtd['sample_norm'].readY(0)
y_mtc_norm = mtd['mtc_norm'].readY(0)
y_sample_m_mtc_norm = mtd['sample_m_mtc_norm'].readY(0)

axs.plot(x_val, y_mtc_norm, label="w/o collimator - bkg_norm")

# w/ collimator
Load(Filename=sfilename_c, OutputWorkspace=samplename_c)
Load(Filename=mfilename_c, OutputWorkspace=mtname_c)
Load(Filename=vrodfilename_c, OutputWorkspace=vrodname_c)

MaskDetectors(samplename_c, DetectorList=mask_det)
MaskDetectors(mtname_c, DetectorList=mask_det)
MaskDetectors(vrodname_c, DetectorList=mask_det)

LoadDiffCal(InputWorkspace=samplename_c, Filename=calfile_c)
ApplyDiffCal(InstrumentWorkspace=samplename_c, CalibrationFile=calfile_c)
ApplyDiffCal(InstrumentWorkspace=mtname_c, CalibrationFile=calfile_c)
ApplyDiffCal(InstrumentWorkspace=vrodname_c, CalibrationFile=calfile_c)

AlignAndFocusPowder(InputWorkspace=samplename_c,
                    OutputWorkspace=samplename_c + '_data_focussed',
                    UnfocussedWorkspace=samplename_c + '_data_not_foc',
                    CalFileName=calfile_c,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=mtname_c,
                    OutputWorkspace=mtname_c + '_data_focussed',
                    UnfocussedWorkspace=mtname_c + '_data_not_foc',
                    CalFileName=calfile_c,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')
AlignAndFocusPowder(InputWorkspace=vrodname_c,
                    OutputWorkspace=vrodname_c + '_data_focussed',
                    UnfocussedWorkspace=vrodname_c + '_data_not_foc',
                    CalFileName=calfile_c,
                    GroupingWorkspace='group_all',
                    Params='0.1,-0.0001,5')

ConvertUnits(InputWorkspace=samplename_c + '_data_focussed',
             OutputWorkspace=samplename_c + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=mtname_c + '_data_focussed',
             OutputWorkspace=mtname_c + '_data_focussed_d',
             Target='dSpacing')
ConvertUnits(InputWorkspace=vrodname_c + '_data_focussed',
             OutputWorkspace=vrodname_c + '_data_focussed_d',
             Target='dSpacing')

Rebin(InputWorkspace=samplename_c + '_data_focussed_d',
      OutputWorkspace=samplename_c + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=mtname_c + '_data_focussed_d',
      OutputWorkspace=mtname_c + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)
Rebin(InputWorkspace=vrodname_c + '_data_focussed_d',
      OutputWorkspace=vrodname_c + '_data_focussed_d_binned',
      Params='0.5,-0.001,8',
      PreserveEvents=False)

sample_norm = Divide(samplename_c + '_data_focussed_d_binned',
                     vrodname_c + '_data_focussed_d_binned')
mtc_norm = Divide(mtname_c + '_data_focussed_d_binned',
                  vrodname_c + '_data_focussed_d_binned')
sample_m_mtc_norm = Minus(samplename_c + '_data_focussed_d_binned',
                          mtname_c + '_data_focussed_d_binned')
sample_m_mtc_norm = Divide(sample_m_mtc_norm,
                           vrodname_c + '_data_focussed_d_binned')

ConvertToPointData(InputWorkspace='sample_norm',
                   OutputWorkspace='sample_norm')
ConvertToPointData(InputWorkspace='mtc_norm',
                   OutputWorkspace='mtc_norm')
ConvertToPointData(InputWorkspace='sample_m_mtc_norm',
                   OutputWorkspace='sample_m_mtc_norm')

x_val = mtd['sample_norm'].readX(0)
y_sample_norm = mtd['sample_norm'].readY(0)
y_mtc_norm = mtd['mtc_norm'].readY(0)
y_sample_m_mtc_norm = mtd['sample_m_mtc_norm'].readY(0)

axs.plot(x_val, y_mtc_norm, label="w/ collimator - bkg_norm")

axs.legend(loc="best")

plt.tight_layout()
plt.show()

now = datetime.datetime.now()
print('Job done!')
print(now.strftime("%Y-%m-%d %H:%M:%S"))
