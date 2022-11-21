import numpy as np
from mantid.simpleapi import *

emt_inst_wksp = Load('NOM_183060')
LoadDiffCal(InputWorkspace=emt_inst_wksp,
            Filename="/SNS/NOM/IPTS-30159/shared/mantid/calibration/NOMAD_183057_2022-08-02_shifter.h5",
            WorkspaceName="183057")

ApplyDiffCal(InstrumentWorkspace=emt_inst_wksp, CalibrationWorkspace='183057_cal')
ConvertUnits(InputWorkspace=emt_inst_wksp, OutputWorkspace="emt_inst_wksp_q",
             Target="MomentumTransfer")

Rebin(InputWorkspace="emt_inst_wksp_q", OutputWorkspace="emt_inst_wksp_q", Params="0.1,0.005,40.", PreserveEvents=False)

MaskDetectors(Workspace="emt_inst_wksp_q", MaskedWorkspace="183057_mask")

DiffractionFocussing(InputWorkspace="emt_inst_wksp_q",
                     OutputWorkspace="emt_inst_wksp_q_focus",
                     GroupingWorkspace="183057_group")

Rebin(InputWorkspace="emt_inst_wksp_q_focus", OutputWorkspace="emt_inst_wksp_q_focus", Params="0.1,0.005,40.", PreserveEvents=False)