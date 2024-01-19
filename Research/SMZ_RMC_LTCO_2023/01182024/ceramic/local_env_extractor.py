#
# ===================
# local_env_extractor
# ===================
#
# The script was adapted from the original version published by
#
# -----------------------------------------------------------------
# J. K. Sun, et al, with the following article,
# Jun, K., Sun, Y., Xiao, Y. et al. Nat. Mater. 21, 924–931 (2022).
# -----------------------------------------------------------------
#
# Several updates as compared to the original version,
#
# 1. octahedral environment analysis was replaced with the 5-coordinated
#    trigonal bipyramid analysis
# 2. detailed comments provided for tracing the information and making
#    further tweakings of the program for different purposes
# 3. re-formatted to follow the `PEP 8` style
#
# # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Yuanpeng Zhang @ 12/26/2023 12:10:38 EST
# SNS_HFIR, ORNL
# # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os, sys
import numpy as np
import scipy
import argparse
from scipy.spatial import ConvexHull
from itertools import permutations
from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import *
from pymatgen.core.composition import *
from pymatgen.ext.matproj import MPRester
from pymatgen.io.vasp.outputs import *
from pymatgen.analysis.chemenv.coordination_environments. \
    coordination_geometry_finder import LocalGeometryFinder
from pymatgen.analysis.chemenv.coordination_environments. \
    structure_environments import LightStructureEnvironments
from pymatgen.analysis.chemenv.coordination_environments. \
    chemenv_strategies import SimplestChemenvStrategy
from pymatgen.analysis.chemenv.coordination_environments. \
    coordination_geometries import *


class HiddenPrints:
    '''Class to reduce the output lines
    '''
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')


    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def non_elements(struct, keep=['O']):
    '''
    :param struct: structure object from Pymatgen
    :type struct: Pymatgen structure object
    :param keep: the specie to keep in the structure
    :type keep: list

    :return: the structure with all of the species removed except those kept
    :rtype: Pymatgen structure object
    '''

    species = list(set(struct.species))
    for ele in keep:
        species.remove(Element(ele))

    stripped = struct.copy()
    stripped.remove_species(species)
    stripped = stripped.get_sorted_structure(reverse=True)
    return stripped


def site_env(coord, struct, sp="Li", envtype='both'):
    '''
    :param coord: fractional coordinate of the target atom
    :type coord: list
    :param struct: structure object from Pymatgen
    :type struct: Pymatgen structure object
    :param sp: the mobile specie
    :type sp: str
    :param envtype: the reference local environment
    :type envtype: str

    :return: the local environment information
    :rtype: dict
    '''

    stripped = non_elements(struct, keep=['Cl', 'O'])
    with_li = stripped.copy()
    with_li.append(
        sp,
        coord,
        coords_are_cartesian=False,
        validate_proximity=False
    )
    with_li = with_li.get_sorted_structure()

    tet_oct_competition = []
    if envtype == 'both' or envtype == 'tet':
        for dist in np.linspace(1, 4, 601):
            neigh = with_li.get_neighbors(with_li.sites[0], dist)
            if len(neigh) < 4:
                continue
            elif len(neigh) > 4:
                break
            neigh_coords = [i.coords for i in neigh]
            with HiddenPrints():
                # Find out only local tetrahedron environment.
                # Refer to the SI of the following paper for a full
                # list of available local environment symbols,
                #
                # Acta Crystallogr B. 2020 Aug 1; 76(Pt 4): 683–695.
                # doi: 10.1107/S2052520620007994
                #
                lgf = LocalGeometryFinder(only_symbols=['T:4'])
                lgf.setup_structure(structure=with_li)
                lgf.setup_local_geometry(isite=0, coords=neigh_coords)

            try:
                site_volume = ConvexHull(neigh_coords).volume
                tet_env = {
                    'csm': lgf.get_coordination_symmetry_measures()['T:4']['csm'],
                    'vol': site_volume,
                    'type': 'tet'
                }
                tet_oct_competition.append(tet_env)
            except Exception as e:
                print(e)
                print("This site cannot be recognized as tetrahedral site")
            if len(neigh) == 4:
                break

    if envtype == 'both' or envtype == 'tribip':
        for dist in np.linspace(1, 4, 601):
            neigh = with_li.get_neighbors(with_li.sites[0], dist)
            if len(neigh) < 5:
                continue
            elif len(neigh) > 5:
                break
            neigh_coords = [i.coords for i in neigh]
            with HiddenPrints():
                # Find out only local trigonal bipyramid environment.
                # This is one of the three options for the 5-coordinated
                # local environment. Refer to the paper mentioned above
                # for a full list of of available local environment symbols.
                lgf = LocalGeometryFinder(
                    only_symbols=["T:5"],
                    permutations_safe_override=False
                )
                lgf.setup_structure(structure=with_li)
                lgf.setup_local_geometry(isite=0, coords=neigh_coords)
            try:
                site_volume = ConvexHull(neigh_coords).volume
                oct_env = {
                    'csm': lgf.get_coordination_symmetry_measures()['T:5']['csm'],
                    'vol': site_volume,
                    'type': 'tribip'
                }
                tet_oct_competition.append(oct_env)
            except Exception as e:
                print(e)
                print("This site cannot be recognized as octahedral site")

            if len(neigh) == 5:
                break

    if envtype == 'both' or envtype == 'oct':
        for dist in np.linspace(1, 4, 601):
            neigh = with_li.get_neighbors(with_li.sites[0], dist)
            if len(neigh) < 6:
                continue
            elif len(neigh) > 6:
                break
            neigh_coords = [i.coords for i in neigh]
            with HiddenPrints():
                # Find out only local trigonal bipyramid environment.
                # This is one of the three options for the 5-coordinated
                # local environment. Refer to the paper mentioned above
                # for a full list of of available local environment symbols.
                lgf = LocalGeometryFinder(
                    only_symbols=["O:6"],
                    permutations_safe_override=False
                )
                lgf.setup_structure(structure=with_li)
                lgf.setup_local_geometry(isite=0, coords=neigh_coords)
            try:
                site_volume = ConvexHull(neigh_coords).volume
                oct_env = {
                    'csm': lgf.get_coordination_symmetry_measures()['O:6']['csm'],
                    'vol': site_volume,
                    'type': 'oct'
                }
                tet_oct_competition.append(oct_env)
            except Exception as e:
                print(e)
                print("This site cannot be recognized as octahedral site")

            if len(neigh) == 6:
                break

    # Return the local environment information of whichever gives
    # the smaller CSM measurement.
    if len(tet_oct_competition) == 0:
        return {
            'csm': np.nan,
            'vol': np.nan,
            'type': 'Non_' + envtype
        }
    elif len(tet_oct_competition) == 1:
        return tet_oct_competition[0]
    elif len(tet_oct_competition) == 2:
        csm1 = tet_oct_competition[0]
        csm2 = tet_oct_competition[1]
        if csm1['csm'] > csm2['csm']:
            return csm2
        else:
            return csm1
    elif len(tet_oct_competition) == 3:
        csm_all = [
            tet_oct_competition[0]['csm'],
            tet_oct_competition[1]['csm'],
            tet_oct_competition[2]['csm']
        ]

        csm_min = min(csm_all)
        csm_min_i = csm_all.index(csm_min)

        return tet_oct_competition[csm_min_i]


def extract_sites(struct, sp="Li", envtype='both'):
    '''
    :param struct: structure object from Pymatgen
    :type struct: Pymatgen structure object
    :param sp: the mobile specie
    :type sp: str
    :param envtype: the reference local environment
    :type envtype: str
    
    :return: the local environment information
    :rtype: dict
    '''
    envlist = []
    for i in range(len(struct.sites)):
        if struct.sites[i].specie != Element(sp):
            continue
        site = struct.sites[i]
        singleenv = site_env(site.frac_coords, struct, sp, envtype)
        envlist.append(
            {
                'frac_coords': site.frac_coords,
                'type': singleenv['type'],
                'csm':singleenv['csm'],
                'volume':singleenv['vol']
            }
        )

    return envlist


def export_envs(envlist, fname, sp='Li', envtype='both'):
    '''
    :param envlist: list of dictionaries of environment information
    :type envlist: list
    :param fname: structure file name
    :type fname: str
    :param sp: the mobile specie
    :type sp: str
    :param envtype: the reference local environment
    :type envtype: str
    '''
    out_fn = fname.split(".")[0] + ".dat"

    with open(out_fn, 'w') as f:
        f.write('Structure file path : ' + fname + '\n')
        f.write('List of environment information\n')
        f.write('Species : ' + sp + "\n")
        f.write('Envtype : ' + envtype + "\n")
        for index, i in enumerate(envlist):
            f.write("Site index " + str(index) + ": " + str(i) + '\n')


if __name__ == "__main__":
    struct_file = "ceramic.cif"

    # Type of local environment to analyze. Options are,
    # 'tet', 'tribip', or 'both', representing tetrahedron,
    # trigonal bipyramid, or both, respectively. If 'both'
    # is specified, for each single analyzed atom (e.g., 'Li'),
    # the program will output the local env information of
    # whichever gives a smaller CSM measurement.
    envtype = "both"

    # Optionally, one could specify the type of elment to analyze
    # the local environment for. By default, the type to focus is
    # 'Li', and to specify a different atom type, uncomment the
    # following line and pass in the 'sp=sp' parameter to both
    # the `extract_sites` and `export_envs` call down below.
    # sp = 'Li'  # replace 'Li' with the type of element to analyze

    struct = Structure.from_file(struct_file)
    site_info = extract_sites(struct, sp="Ta", envtype="both")
    export_envs(site_info, struct_file, sp="Ta", envtype="both")
