import numpy as np
from mantid.simpleapi import *

emt_cap_wksp = Load('NOM_144880')
LoadDiffCal(InputWorkspace=emt_cap_wksp,
            Filename="/SNS/NOM/shared/CALIBRATION/2020_2_1A_Group_CAL/NOMAD_144974_2020-06-04_shifter.h5",
            WorkspaceName="144974")

ApplyDiffCal(InstrumentWorkspace=emt_cap_wksp, CalibrationWorkspace='144974_cal')
ConvertUnits(InputWorkspace=emt_cap_wksp, OutputWorkspace="emt_cap_wksp_q",
             Target="MomentumTransfer")

Rebin(InputWorkspace="emt_cap_wksp_q", OutputWorkspace="emt_cap_wksp_q", Params="0.1,0.005,40.", PreserveEvents=False)

MaskDetectors(Workspace="emt_cap_wksp_q", MaskedWorkspace="144974_mask")

DiffractionFocussing(InputWorkspace="emt_cap_wksp_q",
                     OutputWorkspace="emt_cap_wksp_q_focus",
                     GroupingWorkspace="144974_group")

Rebin(InputWorkspace="emt_cap_wksp_q_focus", OutputWorkspace="emt_cap_wksp_q_focus", Params="0.1,0.005,40.", PreserveEvents=False)