# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python (RMCProfile)
#     language: python
#     name: rmcprofile
# ---

# + tags=[]
import sys
from rmc_tools import rmc6f_stuff
import copy

# + tags=[]
rmc6f_file_name = "glass_ceramic.rmc6f"
lili_ul = 5.0
licl_ul = 2.1

input_rmc_config = rmc6f_stuff.RMC6FReader(rmc6f_file_name)

# + tags=[]
included = dict()
for i in range(input_rmc_config.numAtoms):
    if input_rmc_config.atomsEle[i] == "Li":
        atom_coord_1 = input_rmc_config.atomsCoordInt[i]
        cl_neigh_num = 0
        for j in range(input_rmc_config.numAtoms):
            if input_rmc_config.atomsEle[j] == "Cl":
                atom_coord_2 = input_rmc_config.atomsCoordInt[j]
                dist_temp = rmc6f_stuff.dist_calc_coord(
                    atom_coord_1, atom_coord_2,
                    input_rmc_config.vectors
                )
                if dist_temp <= licl_ul:
                    cl_neigh_num += 1
        if cl_neigh_num > 0:
            included[i] = True
        else:
            included[i] = False

all_neigh = dict()
key_combo_at = dict()
key_combo_coord = dict()

for i in range(input_rmc_config.numAtoms):
    line_s = input_rmc_config.atomsLine[i].strip()
    atom_key_combo = line_s.split()[-3] + "-"
    atom_key_combo += (line_s.split()[-2] + "-")
    atom_key_combo += (line_s.split()[-1] + "-")
    atom_key_combo += (line_s.split()[-4])
    key_combo_at[atom_key_combo] = input_rmc_config.atomsEle[i]
    key_combo_coord[atom_key_combo] = input_rmc_config.atomsCoord[i]
    
    if input_rmc_config.atomsEle[i] == "Li" and included[i]:
        atom_coord_1 = input_rmc_config.atomsCoordInt[i]
        all_neigh[atom_key_combo] = list()
        for j in range(input_rmc_config.numAtoms):
            if input_rmc_config.atomsEle[j] == "Li" and included[j]:
                line_s = input_rmc_config.atomsLine[j].strip()
                atom_key_combo1 = line_s.split()[-3] + "-"
                atom_key_combo1 += (line_s.split()[-2] + "-")
                atom_key_combo1 += (line_s.split()[-1] + "-")
                atom_key_combo1 += (line_s.split()[-4])

                atom_coord_2 = input_rmc_config.atomsCoordInt[j]
                dist_temp = rmc6f_stuff.dist_calc_coord(
                    atom_coord_1, atom_coord_2,
                    input_rmc_config.vectors
                )
                if dist_temp <= lili_ul and dist_temp > 1.E-5:
                    all_neigh[atom_key_combo].append(atom_key_combo1)

# + tags=[]
cluster_num = 0
num_in_cluster = dict()
num_in_cluster[0] = 0
site_cluster = dict()
prop_cluster = dict()
max_cluster = 1E10

# + tags=[]
for key in all_neigh:
    site_cluster[key] = 0

for key, item in all_neigh.items():
    neigh_found = False
    neigh_tmp = list()
    for neigh in item:
        if site_cluster[neigh] != 0:
            neigh_tmp.append(neigh)
            neigh_found = True
            
            r = site_cluster[neigh]
            t = r
            t = -num_in_cluster[t]
            
            if t < 0:
                prop_cluster[neigh] = r
            else:
                r = t
                t = -num_in_cluster[t]
                if t < 0:
                    prop_cluster[neigh] = r
                else:
                    while t > 0:
                        r = t
                        t = -num_in_cluster[t]
                    cluster_temp = site_cluster[neigh]
                    num_in_cluster[cluster_temp] = -r
                    prop_cluster[neigh] = r

    if not neigh_found:
        cluster_num += 1
        site_cluster[key] = cluster_num
        num_in_cluster[cluster_num] = 1
    else:
        min_proper = 1E10
        for item_temp in neigh_tmp:
            if prop_cluster[item_temp] < min_proper:
                min_proper = prop_cluster[item_temp]
        site_cluster[key] = min_proper

        prop_c_uniq = []
        for item_temp in neigh_tmp:
            if prop_cluster[item_temp] not in prop_c_uniq:
                prop_c_uniq.append(prop_cluster[item_temp])

        temp_temp = 0
        for item_temp in prop_c_uniq:
            temp_temp += num_in_cluster[item_temp]

        for item_temp in prop_c_uniq:
            if item_temp == min_proper:
                num_in_cluster[item_temp] = temp_temp + 1
            else:
                num_in_cluster[item_temp] = -min_proper

    site_prop = {}
    for key in all_neigh:
        num_temp = num_in_cluster[site_cluster[key]]
        if num_temp >= 0:
            site_prop[key] = site_cluster[key]
        elif num_temp < 0:
            while num_in_cluster[-num_temp] < 0:
                num_temp = num_in_cluster[-num_temp]
            site_prop[key] = -num_temp

# + tags=[]
num_temp_f = open("cluster.out", "w")
num_temp_f.write("Cluster\t# of Li atoms\n")
for j in range(cluster_num):
    j_temp = j + 1
    if num_in_cluster[j_temp] > 0:
        num_temp_f.write("{0:5d}{1:10d}\n".format(j_temp, num_in_cluster[j_temp]))
num_temp_f.close()

# + tags=[]
max_num = -1E10
for j in range(cluster_num):
    j_temp = j + 1
    if num_in_cluster[j_temp] > max_num:
        max_num = num_in_cluster[j_temp]
        max_cluster = j_temp

li_in_max_cluster = []
for item in all_neigh:
    if site_prop[item] == max_cluster:
        li_in_max_cluster.append(item)

max_cluster_out_f = open("max_cluster.rmc6f", "w")
for item_temp in input_rmc_config.header:
    max_cluster_out_f.write(item_temp)
index = 0
for item_temp in li_in_max_cluster:
    index += 1
    line_temp = str(index) + " " + key_combo_at[item_temp] + " [1] "
    line_temp += "{0:18.15F}{1:18.15F}{2:18.15F} ".format(
        key_combo_coord[item_temp][0],
        key_combo_coord[item_temp][1],
        key_combo_coord[item_temp][2])
    line_temp += (item_temp.split("-")[3] + " ")
    line_temp += (item_temp.split("-")[0] + " ")
    line_temp += (item_temp.split("-")[1] + " ")
    line_temp += (item_temp.split("-")[2])
    max_cluster_out_f.write(line_temp + "\n")
max_cluster_out_f.close()
# -


