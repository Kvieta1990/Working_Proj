import matplotlib.pyplot as plt

for i in range(6):
    # w/o collimator
    x = list()
    y_smc_n_vmt = list()
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
            y_mtc.append(float(line.split()[2]))
            y_mti.append(float(line.split()[3]))
            y_mtc_m_mti.append(float(line.split()[4]))
            y_mtc_m_mti_norm.append(float(line.split()[5]))
    file_in.close()

    fig, axs = plt.subplots(2, 2, figsize=(18, 11))
        
    axs[0, 0].plot(x, y_smc_n_vmt, label="w/o collimator => (Dia - MTC) / (V - MT)")
    axs[0, 1].plot(x, y_mtc_m_mti_norm, label="w/o collimator => (MTC - MT) / (V - MT)")
    axs[1, 0].plot(x, y_mtc, label="w/o collimator => MTC")
    axs[1, 0].plot(x, y_mti, label="w/o collimator => MT")
    axs[1, 1].plot(x, y_mtc_m_mti, label="w/o collimator => MTC - MT")

    x = list()
    y_smc_n_vmt = list()
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
            y_mtc.append(float(line.split()[2]))
            y_mti.append(float(line.split()[3]))
            y_mtc_m_mti.append(float(line.split()[4]))
            y_mtc_m_mti_norm.append(float(line.split()[5]))
    file_in.close()
    
    axs[0, 0].plot(x, y_smc_n_vmt, label="w/ collimator => (Dia - MTC) / (V - MT)")
    axs[0, 1].plot(x, y_mtc_m_mti_norm, label="w/ collimator => (MTC - MT) / (V - MT)")
    axs[1, 0].plot(x, y_mtc, label="w/ collimator => MTC")
    axs[1, 0].plot(x, y_mti, label="w/ collimator => MT")
    axs[1, 1].plot(x, y_mtc_m_mti, label="w/ collimator => MTC - MT")

    if i != 1:
        if i == 0:
            axs[0, 0].set_xlim([1.9, 2.3])
            axs[0, 0].set_ylim([0., 35])
            axs[0, 1].set_xlim([0.5, 3.5])
            axs[1, 1].set_xlim([0.5, 3.5])
            axs[0, 1].set_ylim([0., 0.3])
        if i == 2:
            axs[0, 0].set_xlim([1.9, 2.3])
            axs[0, 0].set_ylim([0., 12])
        if i == 3:
            axs[0, 0].set_xlim([1.9, 2.3])
            axs[0, 0].set_ylim([0, 4.5])
            axs[0, 1].set_xlim([0.5, 7.])
            axs[0, 1].set_ylim([-0.6, 0.8])
        if i == 4:
            axs[0, 0].set_xlim([1.9, 2.3])
            axs[0, 0].set_ylim([-1.5, 17.])
            axs[0, 1].set_xlim([0.5, 7.])
            axs[0, 1].set_ylim([-0.1, 0.5])
        if i == 5:
            axs[0, 0].set_xlim([1.9, 2.3])
    else:
        axs[0, 0].set_xlim([1.225, 1.325])
        axs[0, 0].set_ylim([-3., 47.])
        axs[0, 1].set_xlim([0.5, 2.])
        axs[0, 1].set_ylim([-0.3, 0.6])

    for ax in axs:
        for ax_ax in ax:
            ax_ax.legend(loc="best")

    plt.tight_layout()
    fig.savefig(str(i + 1) + '.png', dpi=300)
