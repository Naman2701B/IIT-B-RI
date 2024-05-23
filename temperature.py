from scipy import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import os

# file = io.loadmat("C:\Internship\SPIT_Interns_task\eTPSS\Traction_Power_Supply_System_Modules\HSRIC_00_Projects\Case_2_P0.25B\Case_2_P0.25B_Output\OLFA_110134_20-05-2024_R_T\TEMP_20-05-24_11-04\TEMP.mat")

def D3Plot_TA(outputfolder,selectedtsnapindex,selectedconductor,radioflag):
    ax = plt.figure().add_subplot(projection='3d')
    file1 = io.loadmat(file_name=os.path.join(outputfolder,"data_ntwrk.mat"))
    allfiles = os.listdir(outputfolder)
    for i in range (len(allfiles)):
        finalfolder = os.path.join(outputfolder,allfiles[i])
        if os.path.isdir(finalfolder) and 'TEMP' in allfiles[i]:
            break
    file2 = io.loadmat(file_name=os.path.join(finalfolder,"Temp.mat"))
    tsnap = file1['tsnap']
    # print(file2["Tavg"])
    x_axis =[]
    y_axis =[]
    z_axis =[]
    super_x_axis = []
    super_y_axis = []
    super_z_axis = []
    for i in range(len(selectedtsnapindex)):
        for j in range(len(file2['Tavg'][0])):
            y_axis.append(float(abs(file2['Tavg'][selectedtsnapindex[i]][j][selectedconductor])))
            z_axis.append(tsnap[selectedtsnapindex[i]])
        super_y_axis.append(y_axis)
        super_z_axis.append(z_axis)
    for i in range(len(selectedtsnapindex)):
        x_axis.append(float(0))
        for j in range(0, len(file1["dev_seqn"])):
            if "line_" in str(file1["dev_seqn"][j][0][0]):
                x_axis.append(float(file1["dev_seqn"][j][3][0][0]))
        super_x_axis.append(x_axis)
    super_x_axis = np.array(super_x_axis)
    super_y_axis = np.array(super_y_axis)
    # super_z_axis = np.array(super_z_axis)
    final_z = []
    for i in range (len(super_z_axis)):
        zshow = []
        for j in range(0, len(super_z_axis[i])):
            # zticks[i].append(zvalue[i][j])
            # print(super_z_axis[i][j])
            zshow.append(calculateTime(super_z_axis[i][j]))
        final_z.append(zshow)
    final_z = np.array(final_z)
    # print(super_x_axis,super_y_axis,len(final_z[0]))
    ax.plot_surface(super_x_axis, super_y_axis, final_z,  edgecolor='royalblue')
    plt.show()
    
    # zticks = []
    # for i in range(0, len(zvalue)):
    #         zticks.append([])
    #         for j in range(0, len(zvalue[i])):
    #             zticks[i].append(zvalue[i][j])
    #             zvalue[i][j] = calculateTime(zvalue[i][j])
    #     zvalue = np.array(zvalue)
    #     zticks = np.array(zticks)
    #     super_y_axis = np.array(super_y_axis)
    #     ax.plot_surface(xvalues, zvalue, super_y_axis,  edgecolor='royalblue')
    #     ax.view_init(elev=20, azim=-145, roll=0)
    #     zvaluestoshow=[]
    #     ztickstoshow =[]
    #     for i in range(0, len(zvalue)):
    #         for j in range(0, len(zticks)):
    #             zvaluestoshow.append(zvalue[i][j])
    #             ztickstoshow.append(zticks[i][j])
    #     ax.set_yticks(zvaluestoshow, ztickstoshow)
    #     ax.set(xlabel='Distance (km)',ylabel='Time Snaps', zlabel=conductors[selectedconductors]+" Voltage (kV)" if radioflag == 0 else conductors[selectedconductors]+" Current (kA)")
    #     # plt.legend()
    #     plt.title("Load Flow Analysis 3D")
    
def calculateTime(time):
    hours = datetime.strptime(time, "%H:%M:%S").hour
    mins = datetime.strptime(time, "%H:%M:%S").minute
    seconds = datetime.strptime(time, "%H:%M:%S").second
    return (hours*3600+mins*60+seconds)


# D3Plot_TA("C:\Internship\SPIT_Interns_task\eTPSS\Traction_Power_Supply_System_Modules\HSRIC_00_Projects\Case_2_P0.25B\Case_2_P0.25B_Output\OLFA_110134_20-05-2024_R_T",[0,3,7],0,0)

# file = io.loadmat("C:\Internship\SPIT_Interns_task\eTPSS\Traction_Power_Supply_System_Modules\HSRIC_00_Projects\Case_2_P0.25B\Case_2_P0.25B_Output\OLFA_213159_20-07-2023_R\data_soln.mat")