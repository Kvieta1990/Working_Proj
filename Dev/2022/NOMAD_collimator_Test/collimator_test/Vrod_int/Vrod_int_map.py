# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# Eight packs to compare
ep_to_compare_str = "33, 49, 58"
ep_tp_compare = []
for item in ep_to_compare_str.split(","):
    if "-" in item:
        tmp_list = list(range(int(item.split("-")[0]), int(item.split("-")[1]) + 1))
        ep_tp_compare.append(tmp_list)
    else:
        ep_tp_compare.append([int(item)])

sfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_169417.nxs.h5'
# Mask generation
mask_det_ids = []
Load(Filename=sfilename_noc, OutputWorkspace="tmp_mask_gen")
group_by_bank = CreateGroupingWorkspace(InputWorkspace=mtd["tmp_mask_gen"], GroupDetectorsBy="bank")
for count, item in enumerate(ep_tp_compare):
    mask_det_ids.append([])
    for i in range(mtd["group_by_bank"].getNumberHistograms()):
        if mtd["group_by_bank"].readY(i)[0] not in item:
            mask_det_ids[count].append(i)
mask_det = mask_det_ids[0]

# Vrod
vrodfilename_noc = '/SNS/NOM/IPTS-28922/nexus/NOM_169418.nxs.h5'
vrodname_noc = 'Vrod_wo_coll'
vrodfilename_c = '/SNS/NOM/IPTS-30147/nexus/NOM_182704.nxs.h5'
vrodname_c = 'Vrod_w_coll'

Load(Filename=vrodfilename_noc, OutputWorkspace=vrodname_noc)
MaskDetectors(vrodname_noc, DetectorList=mask_det)
Load(Filename=vrodfilename_c, OutputWorkspace=vrodname_c)
MaskDetectors(vrodname_c, DetectorList=mask_det)