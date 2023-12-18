import json
import re
import subprocess
import os

data2config = "/Applications/RMCProfile_package_V6.7.9/exe/data2config"


def contains_number(s):
    """Check string contains number
    """
    return any(char.isdigit() for char in s)


def remove_between_brackets(s):
    """Remove all characters between brackets"
    """
    return re.sub(r'\([^)]*\)', '', s)


def sort_two_lists(list1, list2):
    """Sort two lists simultaneously
    """
    combined_lists = list(zip(list1, list2))
    combined_lists.sort(key=lambda x: x[0])
    sorted_list1, sorted_list2 = zip(*combined_lists)

    return sorted_list1, sorted_list2


def finalize_rmc6f(file_in,
                   site_dict,
                   alt_name,
                   sep_atoms_in,
                   out_name,
                   unique_label_used):
    """Finalizing the RMC6F configuration by replacing those temporary
    elements to the true elements.
    """
    with open(file_in, "r") as f:
        i = 0
        while True:
            line = f.readline()
            if line[:6] == "Atoms:":
                atom_line_start = i + 1
                break
            else:
                i += 1
            if "Atom types present:" in line:
                atom_types_line = i
                atoms_order_init = line.strip().split(":")[1].strip().split()
            if "Number of types of atoms:" in line:
                num_atoms_line = i
            if "Number of each atom type:" in line:
                num_each_type_line = i
                each_type_num_init = line.strip().split(":")[1].strip().split()
                each_type_num_init = [int(item) for item in each_type_num_init]
            if "Atom types present:" in line:
                atoms_order = line.strip().split(":")[1].split()
                atoms_order = " ".join(atoms_order)
    
    subprocess.run([
        data2config,
        "-noannotate",
        f"-order [{atoms_order}]",
        "-supercell [1 1 1]",
        "-cif",
        file_in
    ])
    
    with open(file_in.split(".")[0] + ".cif", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "loop_" in line:
            atom_block = False
            j = i + 1
            while j < len(lines) and "loop_" not in lines[j]:
                if "_atom" in lines[j]:
                    atom_block = True
                j += 1

            if atom_block:
                start_line = i
                stop_line = j - 1
                
    if sep_atoms_in:
        accum_num = atom_line_start
        atom_types_str = "Atom types present:         "
        num_each_type_str = "Number of each atom type:   "
        for i, item in enumerate(atoms_order_init):
            true_name = alt_name[item]
            atom_types_str += f" {true_name}"
            num_each_type_str += f" {each_type_num_init[i]}"

            line_start = accum_num + 1
            line_stop = line_start + each_type_num_init[i] - 1

            accum_num = accum_num + each_type_num_init[i]
            print(line_start, line_stop, accum_num)
            
            sed_cli = ["sed"]
            sed_cli.append("-i")
            sed_cli.append("-e")
            sed_cli.append(f'{line_start},{line_stop}s/{item}/{true_name}/')
            sed_cli.append(file_in)
            _ = subprocess.check_call(sed_cli)
            sed_cli = ["sed"]
            sed_cli.append("-i")
            sed_cli.append("-e")
            sed_cli.append(f'{start_line},$s/{item}/{true_name}/g')
            sed_cli.append(file_in.split(".")[0] + ".cif")
            _ = subprocess.check_call(sed_cli)
                
        sed_cli = ["sed"]
        sed_cli.append("-i")
        sed_cli.append("-e")
        sed_cli.append(f'{atom_types_line}c{atom_types_str}\n')
        sed_cli.append(file_in)
        _ = subprocess.check_call(sed_cli)
        sed_cli = ["sed"]
        sed_cli.append("-i")
        sed_cli.append("-e")
        sed_cli.append(f'{num_each_type_line}c{num_each_type_str}\n')
        sed_cli.append(file_in)
        _ = subprocess.check_call(sed_cli)

        os.rename(file_in, out_name)
        os.rename(file_in.split(".")[0] + ".cif",
                  out_name.split(".")[0] + ".cif")
    else:
        viz_ele = list()
        true_ele = list()
        for key, item in alt_name.items():
            viz_ele.append(key)
            true_ele.append(item)

        true_ele_sorted, viz_ele_sorted = sort_two_lists(
            true_ele, viz_ele
        )
        
        viz_ele_sorted_final = list()
        for i, item in enumerate(true_ele_sorted):
            if item in unique_label_used:
                viz_ele_sorted_final.append(item)
            else:
                viz_ele_sorted_final.append(viz_ele_sorted[i])
        
        data2config_cli = [data2config]
        data2config_cli.append("-noannotate")
        data2config_cli.append("-order")
        atoms_all = " ".join(viz_ele_sorted_final)
        data2config_cli.append(f"[{atoms_all}]")
        data2config_cli.append("-supercell")
        data2config_cli.append("[1 1 1]")
        data2config_cli.append("-rmc6f")
        data2config_cli.append(file_in)
        _ = subprocess.check_call(data2config_cli)
        
        file_to_proc = file_in.split(".")[0] + "_new.rmc6f"
        atom_types_str = "Atom types present:         "
        num_each_type_str = "Number of each atom type:   "
        included = list()
        for item in true_ele_sorted:
            if item not in included:
                included.append(item)
                atom_types_str += f" {item}"
        with open(file_to_proc, "r") as f:
            flines = f.readlines()
        for line in flines:
            type_present_found = False
            each_type_num_found = False
            if "Number of each atom type:" in line:
                line_tmp_eat = line
                each_type_num_found = True
            if "Atom types present:" in line:
                line_tmp_atp = line
                type_present_found = True
            if type_present_found and each_type_num_found:
                break

        at_num = dict()
        for i, at in enumerate(line_tmp_atp.split(":")[1].split()):
            at_num[alt_name[at]] = line_tmp_eat.split(":")[1].split()[i]
        
        for item in included:
            num_each_type_str += (" " + at_num[item])
        num_each_type_str += "\n"
        
        sed_cli = ["sed"]
        sed_cli.append("-i")
        sed_cli.append("-e")
        sed_cli.append(f'{atom_types_line}c{atom_types_str}\n')
        sed_cli.append(file_to_proc)
        _ = subprocess.check_call(sed_cli)
        sed_cli = ["sed"]
        sed_cli.append("-i")
        sed_cli.append("-e")
        sed_cli.append(f'{num_each_type_line}c{num_each_type_str}\n')
        sed_cli.append(file_to_proc)
        _ = subprocess.check_call(sed_cli)
        num_atoms_str = f"Number of types of atoms:   {len(included)}"
        sed_cli = ["sed"]
        sed_cli.append("-i")
        sed_cli.append("-e")
        sed_cli.append(f'{num_atoms_line}c{num_atoms_str}\n')
        sed_cli.append(file_to_proc)
        _ = subprocess.check_call(sed_cli)
        for key, item in site_dict.items():
            for _, item_e in item.items():
                true_name = alt_name[item_e[1]]
                sed_cli = ["sed"]
                sed_cli.append("-i")
                sed_cli.append("-e")
                sed_cli.append(f'{atom_line_start},$s/{item_e[1]}/{true_name}/')
                sed_cli.append(file_to_proc)
                _ = subprocess.check_call(sed_cli)
                sed_cli = ["sed"]
                sed_cli.append("-i")
                sed_cli.append("-e")
                sed_cli.append(f'{start_line},$s/{item_e[1]}/{true_name}/g')
                sed_cli.append(file_in.split(".")[0] + ".cif")
                _ = subprocess.check_call(sed_cli)
        os.rename(file_to_proc, out_name)
        os.rename(file_in.split(".")[0] + ".cif",
                  out_name.split(".")[0] + ".cif")

        os.remove(file_in)


def proc_super(input_file, super_dim, out_file, out_info_file, sep_atoms):
    with open(input_file, "r") as f:
        lines = f.readlines()

    with open("elements.json", "r") as f:
        all_ele = json.load(f)
    ele_names = list()
    for ele in all_ele:
        if not contains_number(ele):
            ele_names.append(ele)

    atom_loop_labels = list()
    atom_lines = list()
    for i, line in enumerate(lines):
        if "loop_" in line:
            atom_block = False
            j = i + 1
            while j < len(lines) and "loop_" not in lines[j]:
                if "_atom" in lines[j]:
                    atom_block = True
                    atom_loop_labels.append(lines[j].strip().split("_atom_site_")[1])
                else:
                    if atom_block:
                        line_tmp = lines[j].strip()
                        line_tmp = remove_between_brackets(line_tmp)
                        atom_lines.append(line_tmp)
                j += 1

            if atom_block:
                start_line = i
                stop_line = j - 1

    atom_lines = [line_tmp for line_tmp in atom_lines if len(line_tmp) > 0]

    if "occupancy" in atom_loop_labels:
        occ_index = atom_loop_labels.index("occupancy")
    else:
        occ_index = -1
    fracx_index = atom_loop_labels.index("fract_x")
    fracy_index = atom_loop_labels.index("fract_y")
    fracz_index = atom_loop_labels.index("fract_z")
    if "type_symbol" in atom_loop_labels:
        symbol_index = atom_loop_labels.index("type_symbol")
    else:
        symbol_index = atom_loop_labels.index("label")        

    keep_atom_lines = list()
    unique_label_all = list()
    unique_label_used = list()
    site_dict = dict()
    label_reverse_map = dict()

    for atom_line in atom_lines:
        site_key = atom_line.split()[fracx_index]
        site_key += ("_" + atom_line.split()[fracy_index])
        site_key += ("_" + atom_line.split()[fracz_index])

        for ele in ele_names:
            if ele not in unique_label_all:
                bad_ele = False
                for item in unique_label_all:
                    if item[0] == ele[0]:
                        bad_ele = True
                        break
                if not bad_ele:
                    unique_label_all.append(ele)
                    break

        label_reverse_map[ele] = atom_line.split()[symbol_index]

        if site_key not in site_dict:
            keep_atom_lines.append(atom_line)
            if occ_index == -1:
                val_tmp = 1.
            else:
                val_tmp = atom_line.split()[occ_index]
            site_dict[site_key] = {
                atom_line.split()[symbol_index]: [float(val_tmp), ele]
            }
            # unique_label_used.append(atom_line.split()[symbol_index])
            unique_label_used.append(ele)
            # unique_label_all.append(atom_line.split()[symbol_index])
            unique_label_all.append(ele)
        else:
            key_tmp = atom_line.split()[symbol_index]
            if occ_index == -1:
                val_tmp = 1.
            else:
                val_tmp = atom_line.split()[occ_index]
            site_dict[site_key][key_tmp] = [float(val_tmp), ele]
            
    for key, item in site_dict.items():
        occ_val = 0.
        for key_i in item:
            occ_val += item[key_i][0]
        if abs(1. - occ_val) > 1.E-5:
            for ele in ele_names:
                if ele not in unique_label_all:
                    bad_ele = False
                    for item in unique_label_all:
                        if item[0] == ele[0]:
                            bad_ele = True
                            break
                    if not bad_ele:
                        unique_label_all.append(ele)
                        break
            site_dict[key]["Va"] = [1. - occ_val, ele]
            label_reverse_map[ele] = "Va"
            
    if sep_atoms:
        i = 1
        existing_num = 0
        site_corr = dict()
        for site in site_dict:
            key_tmp = f"Site-{i}"
            coord = [float(item) for item in site.split("_")] 
            index_in_rmc6f = [
                existing_num + j + 1 for j in range(len(site_dict[site]))
            ]
            existing_num += len(site_dict[site])
            site_corr[key_tmp] = {
                "FracCoordinate": coord,
                "IndexInRMC6F": index_in_rmc6f
            }
            i += 1

        with open(out_info_file, "w") as f:
            json.dump(site_corr, f, indent=4)

    lines_tmp = list()
    for i, line in enumerate(lines):
        if i < start_line or i > stop_line:
            lines_tmp.append(line)

    atoms_loop = "loop_\n"
    atoms_loop += "_atom_site_label\n"
    atoms_loop += "_atom_site_occupancy\n"
    atoms_loop += "_atom_site_fract_x\n"
    atoms_loop += "_atom_site_fract_y\n"
    atoms_loop += "_atom_site_fract_z\n"
    atoms_loop += "_atom_site_type_symbol\n"
    lines_tmp.append(atoms_loop)

    i = 0
    for key in site_dict:
        line_tmp = "   " + unique_label_used[i]
        line_tmp += " 1.0"
        line_tmp += (" " + key.split("_")[0])
        line_tmp += (" " + key.split("_")[1])
        line_tmp += (" " + key.split("_")[2])
        line_tmp += (" " + unique_label_used[i])
        line_tmp += "\n"
        lines_tmp.append(line_tmp)
        i += 1

    out_cif_file_tmp = input_file.split(".")[0] + "_tmp.cif"
    out_cif_file = input_file.split(".")[0] + "_tmp"
    with open(out_cif_file_tmp, "w") as f:
        for line in lines_tmp:
            f.write(line)

    data2config_cli = [data2config]
    data2config_cli.append("-noannotate")
    data2config_cli.append("-order")
    atoms_all = " ".join(unique_label_used)
    data2config_cli.append(f"[{atoms_all}]")
    data2config_cli.append("-supercell")
    data2config_cli.append(f"[{super_dim}]")
    data2config_cli.append("-rmc6f")
    data2config_cli.append(out_cif_file_tmp)
    _ = subprocess.check_call(data2config_cli)
    
    unique_label_used_final = [item for item in unique_label_used]
    start_pos = 0
    i = 0
    run_times = 0
    for key, entry in site_dict.items():
        pos = start_pos + i
        for item in entry:
            start_pos += 1
            if item != unique_label_used[i]:
                if entry[item][0] < 1. and unique_label_used[i] != entry[item][1]:
                    pos += 1
                    unique_label_used_final.insert(pos, entry[item][1])
                    data2config_cli = [data2config]
                    data2config_cli.append("-noannotate")
                    data2config_cli.append("-order")
                    atoms_all = " ".join(unique_label_used_final)
                    data2config_cli.append(f"[{atoms_all}]")
                    data2config_cli.append("-replace")
                    data2config_cli.append(f"[{unique_label_used[i]} {entry[item][0]} {entry[item][1]}]")
                    data2config_cli.append("-supercell")
                    data2config_cli.append("[1 1 1]")
                    data2config_cli.append("-rmc6f")
                    out_name_append = "_new" * run_times
                    data2config_cli.append(f"{out_cif_file}{out_name_append}.rmc6f")
                    _ = subprocess.check_call(data2config_cli)
                    run_times += 1
        i += 1

    out_name_append = "_new" * run_times
    out_file_stage = f"{out_cif_file}{out_name_append}.rmc6f"
    os.remove(out_cif_file_tmp)
    for i in range(run_times):
        out_name_append = "_new" * i
        os.remove(f"{out_cif_file}{out_name_append}.rmc6f")

    finalize_rmc6f(
        out_file_stage,
        site_dict,
        label_reverse_map,
        sep_atoms,
        out_file,
        unique_label_used
    )


if __name__ == "__main__":
    input_file = "test_3.cif"
    super_dim = "5 5 5"
    out_file = "test_vesta_out.rmc6f"
    out_info_file = out_file.split(".")[0] + ".info"
    sep_atoms = True

    try:
        proc_super(input_file, super_dim, out_file, out_info_file, sep_atoms)
    except subprocess.CalledProcessError:
        print("Error")
