import matplotlib.pyplot as plt

for i in range(1):
    # w/o collimator
    x = list()
    y_smc_n_vmt = list()
    y_smc_n_vmt_1 = list()
    y_mtc = list()
    y_mti = list()
    y_mtc_m_mti = list()
    y_mtc_m_mti_norm = list()
    
    file_in = open("coll_test_wo_coll_" + str(i + 1) + ".out", "r")
    lines = file_in.readlines()
    for line in lines:
        if line and "NAN" not in line and "INF" not in line:
            x.append(float(line.split()[0]))
            y_smc_n_vmt.append(float(line.split()[1]))
            y_smc_n_vmt_1.append(float(line.split()[6]))
            y_mtc.append(float(line.split()[2]))
            y_mti.append(float(line.split()[3]))
            y_mtc_m_mti.append(float(line.split()[4]))
            y_mtc_m_mti_norm.append(float(line.split()[5]))
    file_in.close()

    fig, axs = plt.subplots(2, 2, figsize=(18, 11))
    fig1, axs1 = plt.subplots(2, 1, figsize=(18, 10))
        
    for ax_1 in axs:
        for ax_2 in ax_1:
            ax_2.set_xlabel('d-spacing (angstrom)')
            ax_2.set_ylabel('Int. (a. u.)')

    for ax_1 in axs1:
        ax_1.set_xlabel('d-spacing (angstrom)')
        ax_1.set_ylabel('Int. (a. u.)')

    axs1[0].plot(x, y_smc_n_vmt, label="w/o collimator => (Dia - MTC) / (V - MT)")
    axs1[1].plot(x, y_smc_n_vmt_1, label="w/o collimator => (Dia - MTC) / V")
    axs[0, 0].plot(x, y_smc_n_vmt, label="w/o collimator => (Dia - MTC) / (V - MT)")
    axs[0, 1].plot(x, y_mtc_m_mti_norm, label="w/o collimator => (MTC - MT) / (V - MT)")
    axs[1, 0].plot(x, y_mtc, label="w/o collimator => MTC")
    axs[1, 0].plot(x, y_mti, label="w/o collimator => MT")
    axs[1, 1].plot(x, y_mtc_m_mti, label="w/o collimator => MTC - MT")

    x = list()
    y_smc_n_vmt = list()
    y_smc_n_vmt_1 = list()
    y_mtc = list()
    y_mti = list()
    y_mtc_m_mti = list()
    y_mtc_m_mti_norm = list()

    file_in = open("coll_test_w_coll_" + str(i + 1) + ".out", "r")
    lines = file_in.readlines()
    for line in lines:
        if line and "NAN" not in line and "INF" not in line:
            x.append(float(line.split()[0]))
            y_smc_n_vmt.append(float(line.split()[1]))
            y_smc_n_vmt_1.append(float(line.split()[6]))
            y_mtc.append(float(line.split()[2]))
            y_mti.append(float(line.split()[3]))
            y_mtc_m_mti.append(float(line.split()[4]))
            y_mtc_m_mti_norm.append(float(line.split()[5]))
    file_in.close()
    
    axs1[0].plot(x, y_smc_n_vmt, label="w/ collimator => (Dia - MTC) / (V - MT)")
    axs1[1].plot(x, y_smc_n_vmt_1, label="w/ collimator => (Dia - MTC) / V")
    axs[0, 0].plot(x, y_smc_n_vmt, label="w/ collimator => (Dia - MTC) / (V - MT)")
    axs[0, 1].plot(x, y_mtc_m_mti_norm, label="w/ collimator => (MTC - MT) / (V - MT)")
    axs[1, 0].plot(x, y_mtc, label="w/ collimator => MTC")
    axs[1, 0].plot(x, y_mti, label="w/ collimator => MT")
    axs[1, 1].plot(x, y_mtc_m_mti, label="w/ collimator => MTC - MT")

    if i != 1:
        axs[0, 0].set_xlim([1.9, 2.3])
        axs[0, 0].set_ylim([-0.1, 9.])
        axs[0, 1].set_ylim([-1., 2.])
        axs1[0].set_xlim([1., 2.5])
        axs1[1].set_xlim([1., 2.5])
        axs1[0].set_ylim([-0.1, 9.])
        axs1[1].set_ylim([-0.1, 2.75])
    else:
        axs[0, 0].set_xlim([1.225, 1.325])
        axs[0, 0].set_ylim([-0.5, 45])
        axs[0, 1].set_xlim([0.5, 2.])
        axs[0, 1].set_ylim([0.075, 0.4])
        axs1[0].set_xlim([0.5, 3])
        axs1[0].set_ylim([0.075, 0.4])
        axs1[1].set_xlim([0.5, 3.])
        axs1[1].set_ylim([0.075, 0.4])

    for ax in axs:
        for ax_ax in ax:
            ax_ax.legend(loc="best")
    for ax in axs1:
        ax.legend(loc='best')

    fig.tight_layout()
    fig1.tight_layout()
    # plt.show()
    fig.savefig(str(i + 1) + '_1.png', dpi=300)
    fig1.savefig(str(i + 1) + '_2.png', dpi=300)
