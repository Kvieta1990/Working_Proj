from mantid.simpleapi import *
import numpy as np
import datetime

# Eight packs to compare
ep_tp_compare = []
ep_tp_compare.append([8, 14])

# -------------- w/o collimator --------------

# Sample - diamond
sfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_169417.nxs.h5'
samplename_noc = 'Dia_wo_coll'

# Empty Can
mfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_169403.nxs.h5'
mtname_noc = 'MTC_wo_coll'

# Vrod
vrodfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_169418.nxs.h5'
vrodname_noc = 'Vrod_wo_coll'

# Cal
calfile_noc = '/SNS/NOM/shared/CALIBRATION/Collimator_Test/NOMAD_169417_2022-02-02_cryostat.h5'

# MT cryostat
mtfilename_noc = "/SNS/NOM/IPTS-28922/nexus/NOM_169419.nxs.h5"
mtiname_noc = 'MT_wo_coll'

# -------------- w/ collimator --------------

# Sample - diamond
sfilename_c = '/SNS/NOM/IPTS-30147/nexus/NOM_182703.nxs.h5'
samplename_c = 'Dia_w_coll'

# Empty Can
mfilename_c = '/SNS/NOM/IPTS-30147/nexus/NOM_182706.nxs.h5'
mtname_c = 'MTC_w_coll'

# Vrod
vrodfilename_c = '/SNS/NOM/IPTS-30147/nexus/NOM_182704.nxs.h5'
vrodname_c = 'Vrod_w_coll'

# Cal
calfile_c = '/SNS/NOM/shared/CALIBRATION/Collimator_Test/NOMAD_182703_2022-07-28_cryostat.h5'

# MT cryostat
mtfilename_c = "/SNS/NOM/IPTS-30147/nexus/NOM_182705.nxs.h5"
mtiname_c = 'MT_w_coll'

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

for ct, mask_det in enumerate(mask_det_ids):
    # w/o collimator
    Load(Filename=sfilename_noc, OutputWorkspace=samplename_noc)
    Load(Filename=mfilename_noc, OutputWorkspace=mtname_noc)
    Load(Filename=vrodfilename_noc, OutputWorkspace=vrodname_noc)
    Load(Filename=mtfilename_noc, OutputWorkspace=mtiname_noc)

    MaskDetectors(samplename_noc, DetectorList=mask_det)
    MaskDetectors(mtname_noc, DetectorList=mask_det)
    MaskDetectors(vrodname_noc, DetectorList=mask_det)
    MaskDetectors(mtiname_noc, DetectorList=mask_det)

    Load(Filename=sfilename_c, OutputWorkspace=samplename_c)
    Load(Filename=mfilename_c, OutputWorkspace=mtname_c)
    Load(Filename=vrodfilename_c, OutputWorkspace=vrodname_c)
    Load(Filename=mtfilename_c, OutputWorkspace=mtiname_c)

    MaskDetectors(samplename_c, DetectorList=mask_det)
    MaskDetectors(mtname_c, DetectorList=mask_det)
    MaskDetectors(vrodname_c, DetectorList=mask_det)
    MaskDetectors(mtiname_c, DetectorList=mask_det)

    LoadDiffCal(InputWorkspace=samplename_noc, Filename=calfile_noc)
    ApplyDiffCal(InstrumentWorkspace=samplename_noc, CalibrationFile=calfile_noc)
    ApplyDiffCal(InstrumentWorkspace=mtname_noc, CalibrationFile=calfile_noc)
    ApplyDiffCal(InstrumentWorkspace=vrodname_noc, CalibrationFile=calfile_noc)
    ApplyDiffCal(InstrumentWorkspace=mtiname_noc, CalibrationFile=calfile_noc)

    MaskDetectors(samplename_c, MaskedWorkspace='_mask')
    MaskDetectors(mtname_c, MaskedWorkspace='_mask')
    MaskDetectors(vrodname_c, MaskedWorkspace='_mask')
    MaskDetectors(mtiname_c, MaskedWorkspace='_mask')

    LoadDiffCal(InputWorkspace=samplename_c, Filename=calfile_c)
    ApplyDiffCal(InstrumentWorkspace=samplename_c, CalibrationFile=calfile_c)
    ApplyDiffCal(InstrumentWorkspace=mtname_c, CalibrationFile=calfile_c)
    ApplyDiffCal(InstrumentWorkspace=vrodname_c, CalibrationFile=calfile_c)
    ApplyDiffCal(InstrumentWorkspace=mtiname_c, CalibrationFile=calfile_c)

    MaskDetectors(samplename_noc, MaskedWorkspace='_mask')
    MaskDetectors(mtname_noc, MaskedWorkspace='_mask')
    MaskDetectors(vrodname_noc, MaskedWorkspace='_mask')
    MaskDetectors(mtiname_noc, MaskedWorkspace='_mask')

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

    file_out = open("coll_test_wo_coll_" + str(ct + 1) + ".out", "w")
    for count, item in enumerate(x_val):
        file_out.write("{0:20.5F}{1:20.5F}{2:20.5F}{3:20.5F}{4:20.5F}{5:20.5F}{6:20.5F}\n".format(item,
                                                                                                  y_sample_m_mtc_norm[count],
                                                                                                  y_mtc[count],
                                                                                                  y_mti[count],
                                                                                                  y_mtc_m_mti[count],
                                                                                                  y_mtc_m_mti_norm[count],
                                                                                                  y_sample_m_mtc_norm_1[count]))
    file_out.close()

    file_out = open('coll_test_wo_coll_van_' + str(i + 1) + ".out", "w")
    for count, item in enumerate(x_val):
        file_out.write("{0:20.5F}{1:20.5F}\n".format(item, van_out[count]))
    
    file_out.close()

    # w/ collimator
    group_all = CreateGroupingWorkspace(InputWorkspace=mtd["tmp_mask_gen"],
                                        GroupDetectorsBy="All")
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
    AlignAndFocusPowder(InputWorkspace=mtiname_c,
                        OutputWorkspace=mtiname_c + '_data_focussed',
                        UnfocussedWorkspace=mtiname_c + '_data_not_foc',
                        CalFileName=calfile_c,
                        GroupingWorkspace='group_all',
                        Params='0.1,-0.0001,5')

    NormaliseByCurrent(InputWorkspace=samplename_c + '_data_focussed',
                       OutputWorkspace=samplename_c + '_data_focussed',
                       RecalculatePCharge=True)
    NormaliseByCurrent(InputWorkspace=mtname_c + '_data_focussed',
                       OutputWorkspace=mtname_c + '_data_focussed',
                       RecalculatePCharge=True)
    NormaliseByCurrent(InputWorkspace=vrodname_c + '_data_focussed',
                       OutputWorkspace=vrodname_c + '_data_focussed',
                       RecalculatePCharge=True)
    NormaliseByCurrent(InputWorkspace=mtiname_c + '_data_focussed',
                       OutputWorkspace=mtiname_c + '_data_focussed',
                       RecalculatePCharge=True)

    ConvertUnits(InputWorkspace=samplename_c + '_data_focussed',
                 OutputWorkspace=samplename_c + '_data_focussed_d',
                 Target='dSpacing')
    ConvertUnits(InputWorkspace=mtname_c + '_data_focussed',
                 OutputWorkspace=mtname_c + '_data_focussed_d',
                 Target='dSpacing')
    ConvertUnits(InputWorkspace=vrodname_c + '_data_focussed',
                 OutputWorkspace=vrodname_c + '_data_focussed_d',
                 Target='dSpacing')
    ConvertUnits(InputWorkspace=mtiname_c + '_data_focussed',
                 OutputWorkspace=mtiname_c + '_data_focussed_d',
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
    Rebin(InputWorkspace=mtiname_c + '_data_focussed_d',
          OutputWorkspace=mtiname_c + '_data_focussed_d_binned',
          Params='0.5,-0.001,8',
          PreserveEvents=False)

    sample_norm = Divide(samplename_c + '_data_focussed_d_binned',
                         vrodname_c + '_data_focussed_d_binned')
    mtc_norm = Divide(mtname_c + '_data_focussed_d_binned',
                      vrodname_c + '_data_focussed_d_binned')
    vrod_m_mti = Minus(vrodname_c + '_data_focussed_d_binned',
                       mtiname_c + '_data_focussed_d_binned')
    sample_m_mtc_norm = Minus(samplename_c + '_data_focussed_d_binned',
                              mtname_c + '_data_focussed_d_binned')
    sample_m_mtc_norm_1 = Divide(sample_m_mtc_norm,
                                 vrodname_c + '_data_focussed_d_binned')
    sample_m_mtc_norm = Divide(sample_m_mtc_norm,
                               vrod_m_mti)
    mtc_m_mti = Minus(mtname_c + '_data_focussed_d_binned',
                      mtiname_c + '_data_focussed_d_binned')
    mtc_m_mti_norm = Divide(mtc_m_mti,
                            vrod_m_mti)

    ConvertToPointData(InputWorkspace='vrod_m_mti',
                       OutputWorkspace='vrod_m_mti')
    ConvertToPointData(InputWorkspace='sample_norm',
                       OutputWorkspace='sample_norm')
    ConvertToPointData(InputWorkspace=mtname_c + '_data_focussed_d_binned',
                       OutputWorkspace=mtname_c + '_data_focussed_d_binned')
    ConvertToPointData(InputWorkspace=mtiname_c + '_data_focussed_d_binned',
                       OutputWorkspace=mtiname_c + '_data_focussed_d_binned')
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
    y_mtc = mtd[mtname_c + '_data_focussed_d_binned'].readY(0)
    y_mti = mtd[mtiname_c + '_data_focussed_d_binned'].readY(0)
    y_mtc_m_mti = mtd['mtc_m_mti'].readY(0)
    y_mtc_m_mti_norm = mtd['mtc_m_mti_norm'].readY(0)
    y_sample_m_mtc_norm = mtd['sample_m_mtc_norm'].readY(0)
    y_sample_m_mtc_norm_1 = mtd['sample_m_mtc_norm_1'].readY(0)
    van_out = mtd['vrod_m_mti'].readY(0)

    file_out = open("coll_test_w_coll_" + str(ct + 1) + ".out", "w")
    for count, item in enumerate(x_val):
        file_out.write("{0:20.5F}{1:20.5F}{2:20.5F}{3:20.5F}{4:20.5F}{5:20.5F}{6:20.5F}\n".format(item,
                                                                                                  y_sample_m_mtc_norm[count],
                                                                                                  y_mtc[count],
                                                                                                  y_mti[count],
                                                                                                  y_mtc_m_mti[count],
                                                                                                  y_mtc_m_mti_norm[count],
                                                                                                  y_sample_m_mtc_norm_1[count]))
    file_out.close()

    file_out = open('coll_test_w_coll_van_' + str(i + 1) + ".out", "w")
    for count, item in enumerate(x_val):
        file_out.write("{0:20.5F}{1:20.5F}\n".format(item, van_out[count]))
    
    file_out.close()

now = datetime.datetime.now()
print('Job done!')
print(now.strftime("%Y-%m-%d %H:%M:%S"))
