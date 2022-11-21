import numpy as np
from mantid.simpleapi import *

emt_inst_wksp = Load('NOM_183704')
LoadDiffCal(InputWorkspace=emt_inst_wksp,
            Filename="/SNS/NOM/IPTS-30159/shared/mantid/calibration/NOMAD_183699_2022-08-05_shifter.h5",
            WorkspaceName="183699")

ApplyDiffCal(InstrumentWorkspace=emt_inst_wksp, CalibrationWorkspace='183699_cal')
ConvertUnits(InputWorkspace=emt_inst_wksp, OutputWorkspace="emt_inst_wksp_q",
             Target="MomentumTransfer")

Rebin(InputWorkspace="emt_inst_wksp_q", OutputWorkspace="emt_inst_wksp_q", Params="0.1,0.005,40.", PreserveEvents=False)

MaskDetectors(Workspace="emt_inst_wksp_q", MaskedWorkspace="183699_mask")

DiffractionFocussing(InputWorkspace="emt_inst_wksp_q",
                     OutputWorkspace="emt_inst_wksp_q_focus",
                     GroupingWorkspace="183699_group")

Rebin(InputWorkspace="emt_inst_wksp_q_focus", OutputWorkspace="emt_inst_wksp_q_focus", Params="0.1,0.005,40.", PreserveEvents=False)